#!/usr/bin/env python3.11
import json
import argparse
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import numpy as np

def calculate_windowed_features(all_transactions: List[Dict[str, Any]], target_address: str, window_hours: int = 24, step_hours: int = 1, period_start_time: Optional[datetime] = None, period_end_time: Optional[datetime] = None) -> pd.DataFrame:
    """
    Calculates features for rolling time windows from a list of transactions for a specific address
    within a given period_start_time and period_end_time.
    """
    if not all_transactions:
        return pd.DataFrame()

    df_all = pd.DataFrame(all_transactions)
    df_all["datetime"] = pd.to_datetime(df_all["timeStamp"], unit="s")
    df_all.sort_values(by="datetime", inplace=True)
    df_all["value_eth"] = df_all["value"].astype(float) / (10**18)
    df_all["gasPrice_gwei"] = df_all["gasPrice"].astype(float) / (10**9)
    df_all["gasUsed"] = df_all["gasUsed"].astype(float)
    df_all["gas_fee_eth"] = (df_all["gasPrice"].astype(float) * df_all["gasUsed"].astype(float)) / (10**18)

    target_address_lower = target_address.lower()
    df_all["transaction_type"] = df_all.apply(
        lambda row: "incoming" if row["to"].lower() == target_address_lower 
        else ("outgoing" if row["from"].lower() == target_address_lower 
              else "internal_or_unrelated"), axis=1
    )
    
    df_address_related = df_all[(df_all["to"].str.lower() == target_address_lower) | (df_all["from"].str.lower() == target_address_lower)].copy()

    if df_address_related.empty:
        return pd.DataFrame()

    # Filter by overall period if specified
    if period_start_time:
        df_address_related = df_address_related[df_address_related["datetime"] >= period_start_time]
    if period_end_time:
        df_address_related = df_address_related[df_address_related["datetime"] < period_end_time]

    if df_address_related.empty:
        return pd.DataFrame()

    window_duration = timedelta(hours=window_hours)
    step_duration = timedelta(hours=step_hours)
    
    min_time_in_period = df_address_related["datetime"].min()
    max_time_in_period = df_address_related["datetime"].max()
    
    windowed_features_list = []
    
    current_window_start_time = min_time_in_period
    while current_window_start_time <= max_time_in_period:
        current_window_end_time = current_window_start_time + window_duration
        
        window_df = df_address_related[
            (df_address_related["datetime"] >= current_window_start_time) & 
            (df_address_related["datetime"] < current_window_end_time)
        ]
        
        # Always create a feature row, even if empty, to represent the window
        features = {"window_start": current_window_start_time, "window_end": current_window_end_time}
        features["address"] = target_address
        
        if not window_df.empty:
            features["total_transactions_in_window"] = len(window_df)
            incoming_tx = window_df[window_df["transaction_type"] == "incoming"]
            outgoing_tx = window_df[window_df["transaction_type"] == "outgoing"]

            features["incoming_tx_count"] = len(incoming_tx)
            features["outgoing_tx_count"] = len(outgoing_tx)
            features["total_eth_volume_in"] = incoming_tx["value_eth"].sum()
            features["total_eth_volume_out"] = outgoing_tx["value_eth"].sum()
            features["avg_eth_tx_value_in"] = incoming_tx["value_eth"].mean() if not incoming_tx.empty else 0
            features["avg_eth_tx_value_out"] = outgoing_tx["value_eth"].mean() if not outgoing_tx.empty else 0
            features["max_eth_tx_value_in"] = incoming_tx["value_eth"].max() if not incoming_tx.empty else 0
            features["max_eth_tx_value_out"] = outgoing_tx["value_eth"].max() if not outgoing_tx.empty else 0
            features["unique_counterparties_in"] = incoming_tx["from"].nunique()
            features["unique_counterparties_out"] = outgoing_tx["to"].nunique()
            features["total_gas_fee_eth_spent_by_address"] = outgoing_tx["gas_fee_eth"].sum()
            features["avg_gas_fee_eth_spent_by_address"] = outgoing_tx["gas_fee_eth"].mean() if not outgoing_tx.empty else 0

            if len(window_df) > 1:
                time_diffs_sec = window_df["datetime"].diff().dt.total_seconds().dropna()
                features["avg_time_between_tx_sec"] = time_diffs_sec.mean() if not time_diffs_sec.empty else 0
                features["std_time_between_tx_sec"] = time_diffs_sec.std() if not time_diffs_sec.empty else 0
            else:
                features["avg_time_between_tx_sec"] = 0
                features["std_time_between_tx_sec"] = 0
            features["incoming_to_outgoing_volume_ratio"] = features["total_eth_volume_in"] / (features["total_eth_volume_out"] + 1e-9)
            features["incoming_to_outgoing_count_ratio"] = features["incoming_tx_count"] / (features["outgoing_tx_count"] + 1e-9)
        else: # Fill with zeros if window is empty
            feature_keys = ["total_transactions_in_window", "incoming_tx_count", "outgoing_tx_count", 
                            "total_eth_volume_in", "total_eth_volume_out", "avg_eth_tx_value_in", 
                            "avg_eth_tx_value_out", "max_eth_tx_value_in", "max_eth_tx_value_out", 
                            "unique_counterparties_in", "unique_counterparties_out", 
                            "total_gas_fee_eth_spent_by_address", "avg_gas_fee_eth_spent_by_address",
                            "avg_time_between_tx_sec", "std_time_between_tx_sec",
                            "incoming_to_outgoing_volume_ratio", "incoming_to_outgoing_count_ratio"]
            for key in feature_keys:
                features[key] = 0
        
        windowed_features_list.append(features)
        
        if current_window_start_time + step_duration > max_time_in_period and current_window_start_time < max_time_in_period:
             if current_window_end_time >= max_time_in_period:
                 break
             current_window_start_time = max_time_in_period - window_duration + timedelta(seconds=1) 
             if current_window_start_time < min_time_in_period: current_window_start_time = min_time_in_period
        elif current_window_start_time + step_duration > max_time_in_period:
            break 
        else:
            current_window_start_time += step_duration
        
    return pd.DataFrame(windowed_features_list)

def detect_anomalies_with_historical_baseline(current_windowed_features_df: pd.DataFrame, historical_baselines: Dict[str, float], std_dev_multiplier: float = 3.0) -> List[Dict[str, Any]]:
    """
    Detects anomalies by comparing current window features to historical baselines.
    """
    anomalies_report = []    
    if current_windowed_features_df.empty:
        return [{"window_start": "N/A", "window_end": "N/A", "anomalies": ["No current windowed features to analyze."]}]
    if not historical_baselines:
        return [{"window_start": "N/A", "window_end": "N/A", "anomalies": ["No historical baselines provided."]}]

    features_to_check = [
        "total_transactions_in_window", "incoming_tx_count", "outgoing_tx_count",
        "total_eth_volume_in", "total_eth_volume_out", "max_eth_tx_value_in", "max_eth_tx_value_out",
        "total_gas_fee_eth_spent_by_address"
    ]

    for i, window_row in current_windowed_features_df.iterrows():
        current_anomalies = []
        window_label = f"Window: {window_row['window_start']} to {window_row['window_end']}"

        for feature_name in features_to_check:
            mean_key = f"{feature_name}_mean"
            std_key = f"{feature_name}_std"
            
            current_value = window_row.get(feature_name, 0)
            mean_val = historical_baselines.get(mean_key)
            std_val = historical_baselines.get(std_key)

            if mean_val is not None and std_val is not None:
                if std_val > 1e-9: # Avoid issues with zero std deviation if activity was constant
                    upper_bound = mean_val + std_dev_multiplier * std_val
                    lower_bound = mean_val - std_dev_multiplier * std_val # Though for counts/volumes, lower bound might be just > 0

                    if current_value > upper_bound:
                        current_anomalies.append(f"High Anomaly for {feature_name}: {current_value:.2f} (Historical Mean: {mean_val:.2f}, Std: {std_val:.2f}, Upper Bound: {upper_bound:.2f})")
                    # Add lower bound check if meaningful for the feature
                    # For counts/volumes, a significant drop from a non-zero mean could also be an anomaly
                    if feature_name not in ["max_eth_tx_value_in", "max_eth_tx_value_out"] and current_value < lower_bound and current_value < mean_val : # e.g. drop in activity
                         if mean_val > 1e-9 : # only if mean was not zero
                            current_anomalies.append(f"Low Anomaly for {feature_name}: {current_value:.2f} (Historical Mean: {mean_val:.2f}, Std: {std_val:.2f}, Lower Bound: {lower_bound:.2f})")
                elif current_value > mean_val: # If std is zero, any deviation from mean is an anomaly
                     current_anomalies.append(f"Deviation from Constant for {feature_name}: {current_value:.2f} (Historical Value: {mean_val:.2f})")
            else:
                # Fallback to simple rules if baseline for this specific feature is missing
                if feature_name == "total_transactions_in_window" and current_value > 50:
                    current_anomalies.append(f"High Transaction Count (fallback rule): {current_value} transactions.")
                if feature_name == "max_eth_tx_value_out" and current_value > 50:
                    current_anomalies.append(f"Large Outgoing Transaction (fallback rule): Max {current_value:.2f} ETH sent.")

        if not current_anomalies:
            current_anomalies.append("No specific anomalies detected in this window based on historical baselines.")
        
        anomalies_report.append({
            "window_start": str(window_row["window_start"]),
            "window_end": str(window_row["window_end"]),
            "features": window_row.to_dict(),
            "anomalies_detected_in_window": current_anomalies
        })
        
    return anomalies_report

def main():
    parser = argparse.ArgumentParser(description="Analyze Etherscan transaction data for anomalies using historical baselining.")
    parser.add_argument("-i", "--input_file", type=str, required=True, help="Path to the input JSON file (cleaned Etherscan transactions for the target address)." )
    parser.add_argument("-o", "--output_file", type=str, required=True, help="Path to the output JSON file with analysis results.")
    parser.add_argument("-a", "--address", type=str, required=True, help="The Ethereum address for which the transactions were fetched (case-insensitive)." )
    parser.add_argument("--window_hours", type=int, default=24, help="Duration of each rolling window in hours for feature calculation.")
    parser.add_argument("--step_hours", type=int, default=6, help="Step size for the rolling window in hours.")
    parser.add_argument("--baseline_days", type=int, default=30, help="Number of initial days of data to use for establishing historical baselines.")
    parser.add_argument("--std_dev_multiplier", type=float, default=3.0, help="Number of standard deviations from the mean to consider an anomaly.")

    args = parser.parse_args()

    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            transactions = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found: {args.input_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from input file: {args.input_file}")
        return

    if not isinstance(transactions, list) or not transactions:
        print(f"No valid transaction data found in {args.input_file}. Nothing to analyze.")
        # Write empty/error result
        results = {"address": args.address, "error": "No transaction data"}
        with open(args.output_file, "w", encoding="utf-8") as f: json.dump(results, f, indent=4)
        return

    df_full_history = pd.DataFrame(transactions)
    df_full_history["datetime"] = pd.to_datetime(df_full_history["timeStamp"], unit="s")
    df_full_history.sort_values(by="datetime", inplace=True)

    if df_full_history.empty:
        print(f"Transaction data for address {args.address} is empty after initial load.")
        results = {"address": args.address, "error": "Empty transaction data after load"}
        with open(args.output_file, "w", encoding="utf-8") as f: json.dump(results, f, indent=4)
        return
        
    first_tx_time = df_full_history["datetime"].min()
    baseline_period_end_time = first_tx_time + timedelta(days=args.baseline_days)
    
    print(f"Establishing historical baseline using data up to: {baseline_period_end_time}")
    historical_windowed_features_df = calculate_windowed_features(
        transactions, args.address, args.window_hours, args.step_hours, 
        period_start_time=None, period_end_time=baseline_period_end_time
    )

    historical_baselines = {}
    if not historical_windowed_features_df.empty:
        print(f"Calculated {len(historical_windowed_features_df)} windows for historical baseline.")
        for col in historical_windowed_features_df.columns:
            if col not in ["window_start", "window_end", "address"] and pd.api.types.is_numeric_dtype(historical_windowed_features_df[col]):
                historical_baselines[f"{col}_mean"] = historical_windowed_features_df[col].mean()
                historical_baselines[f"{col}_std"] = historical_windowed_features_df[col].std()
    else:
        print("No data available for historical baseline period or no features generated.")

    print(f"Analyzing current period data after: {baseline_period_end_time}")
    current_windowed_features_df = calculate_windowed_features(
        transactions, args.address, args.window_hours, args.step_hours,
        period_start_time=baseline_period_end_time, period_end_time=None
    )

    analysis_windows_report = []
    if not current_windowed_features_df.empty:
        print(f"Detecting anomalies across {len(current_windowed_features_df)} current windows...")
        analysis_windows_report = detect_anomalies_with_historical_baseline(current_windowed_features_df, historical_baselines, args.std_dev_multiplier)
    else:
        print("No data available for current period analysis or no features generated.")
        analysis_windows_report.append({
            "window_start": "N/A", "window_end": "N/A", "features": {},
            "anomalies_detected_in_window": ["No current data to analyze after baseline period."]
        })
            
    results = {
        "address": args.address,
        "parameters": {
            "window_hours": args.window_hours, 
            "step_hours": args.step_hours,
            "baseline_days": args.baseline_days,
            "std_dev_multiplier": args.std_dev_multiplier
        },
        "historical_baseline_stats_summary": {k: v for k, v in historical_baselines.items() if pd.notna(v)}, # Store non-NaN baselines
        "analysis_windows": analysis_windows_report
    }

    try:
        with open(args.output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4, default=str) 
        print(f"On-chain analysis results with historical baselining saved to {args.output_file}")
    except Exception as e:
        print(f"Error writing analysis results to {args.output_file}: {e}")

if __name__ == "__main__":
    main()

