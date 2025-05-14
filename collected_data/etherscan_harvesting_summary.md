# Data Harvesting Summary (Etherscan Transactions)

Date: 2025-05-14

## Overview
Transaction history was collected for 12 recently launched Ethereum-based meme coin contracts. The data was fetched using the Etherscan API.

## Results

Out of the 12 contracts processed, 10 contracts returned transaction data (up to 100 transactions each as per the script's current limit per address). Two contracts returned a "No transactions found" message from the Etherscan API, which is a valid response indicating no on-chain activity was recorded for them by Etherscan under the query parameters.

### Contracts with Transaction Data:

*   `0x23878914EFE38d27C4D67Ab83ed1b93A74D4086a` (coin_01)
*   `0x4C6dfa353B67832a23d26E17b0737819C624437C` (coin_03)
*   `0x4d5F47FA6A74757f35C14fD3a6Ef8E3C9BC514E8` (coin_04)
*   `0x5959e94661E1203e0c8Ef84095A7846bacc6A94F` (coin_05)
*   `0x666Acd390FA42d5bf86e9C42dc2FA6f6b4B2d8AB` (coin_07)
*   `0x92d3447e956613ee066ad5b4077a8c6e66424d5d` (coin_08)
*   `0xd86830e9c56785e2b703eb0029ae71a943e4d442` (coin_09)
*   `0xdBBE8833C6359CFB287447eD3066e697F9C15E49` (coin_10)
*   `0xe778fd9a8d074e4a808092896b33fe3d3452c125` (coin_11)
*   `0xf816507e690f5aa4e29d164885eb5fa7a5627860` (coin_12)

### Contracts with No Transactions Found (as per Etherscan API response):

*   `0x4C6dD9d463d57C35e3B24437C1A3953929211A5C` (coin_02)
*   `0x666A1B2d8AB8999B3f16551991017C99070cFc32` (coin_06)

## Notes
*   The collection was limited to transaction history due to Etherscan API key limitations (token holder data requires a Pro key).
*   The data for each contract is stored in a separate JSON file in the `/home/ubuntu/project_files/collected_data/etherscan_final_output/` directory.
*   The list of target contracts was generated using the CoinMarketCap API and is stored in `/home/ubuntu/project_files/target_ethereum_meme_coins.txt`.

This initial dataset provides a foundation for further analysis of on-chain activity for these recently launched meme coins.
