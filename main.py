import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np # Import numpy for np.nan

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

SOURCE_DATA_FILE_PATH = "/home/ubuntu/meme_coin_pattern_recognition_platform/engineered_features/integrated_scores.csv"

@app.route("/api/v1/scores", methods=["GET"])
def get_scores():
    """Endpoint to retrieve all integrated scores."""
    try:
        if not os.path.exists(SOURCE_DATA_FILE_PATH):
            return jsonify({"error": "Source data file not found"}), 404

        df = pd.read_csv(SOURCE_DATA_FILE_PATH)
        if df.empty:
            return jsonify({"scores": []}), 200 
            
        df = df.replace({pd.NA: None, np.nan: None})
        scores = df.to_dict(orient="records")
        return jsonify({"scores": scores}), 200
    except pd.errors.EmptyDataError:
        return jsonify({"scores": []}), 200
    except Exception as e:
        print(f"An error occurred while fetching all scores: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/v1/scores/<string:identifier>", methods=["GET"])
def get_score_by_identifier(identifier):
    """Endpoint to retrieve a specific score by user_screen_name or tweet_id."""
    try:
        if not os.path.exists(SOURCE_DATA_FILE_PATH):
            return jsonify({"error": "Source data file not found"}), 404

        df = pd.read_csv(SOURCE_DATA_FILE_PATH)
        if df.empty:
            return jsonify({"error": "No data available"}), 404

        df = df.replace({pd.NA: None, np.nan: None})
        
        # Try to find by user_screen_name first
        coin_data = df[df["user_screen_name"] == identifier]
        
        if coin_data.empty: # Corrected: .empty is a property, not a method
            # If not found by user_screen_name, try by tweet_id (converting identifier to float if it's a numeric string)
            try:
                tweet_id_identifier = float(identifier)
                coin_data = df[df["tweet_id"] == tweet_id_identifier]
            except ValueError:
                # If identifier cannot be converted to float, it's not a valid tweet_id format we expect
                pass # coin_data remains empty

        if coin_data.empty: # Corrected: .empty is a property, not a method
            return jsonify({"error": "Coin not found"}), 404
        
        # Assuming identifier is unique or we take the first match
        return jsonify(coin_data.iloc[0].to_dict()), 200
    except pd.errors.EmptyDataError:
        return jsonify({"error": "No data available"}), 404 # Should be caught by df.empty earlier
    except Exception as e:
        print(f"An error occurred while fetching score for {identifier}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/")
def health_check():
    return jsonify({"status": "API is running"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

