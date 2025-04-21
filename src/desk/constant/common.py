from typing import Dict
from desk.types import NetworkOption, ChainOption


BROKER = "DESK-SDK"

BASE_URLS: Dict[NetworkOption, str] = {
    "mainnet": "https://api.happytrading.global",
    "mainnetBase": "https://api.happytrading.global",
    "mainnetArbitrum": "https://api.happytrading.global",
    "mainnetBsc": "https://api.happytrading.global",
    "base": "https://api.happytrading.global",
    "arbitrum": "https://api.happytrading.global",
    "bsc": "https://api.happytrading.global",
    "testnet": "https://stg-trade-api.happytrading.global",
    "testnetBase": "https://stg-trade-api.happytrading.global",
    "testnetArbitrum": "https://stg-trade-api.happytrading.global",
    "testnetBsc": "https://stg-trade-api.happytrading.global",
    "baseSepolia": "https://stg-trade-api.happytrading.global",
    "arbitrumSepolia": "https://stg-trade-api.happytrading.global",
    "bscTestnet": "https://stg-trade-api.happytrading.global"
}

CRM_URLS: Dict[NetworkOption, str] = {
    "mainnet": "https://api.desk.exchange",
    "mainnetBase": "https://api.desk.exchange",
    "mainnetArbitrum": "https://api.desk.exchange",
    "mainnetBsc": "https://api.desk.exchange",
    "testnet": "https://dev-api.desk.exchange",
    "testnetBase": "https://dev-api.desk.exchange",
    "testnetArbitrum": "https://dev-api.desk.exchange",
    "testnetBsc": "https://dev-api.desk.exchange",
    "base": "https://api.desk.exchange",
    "arbitrum": "https://api.desk.exchange",
    "bsc": "https://api.desk.exchange",
    "baseSepolia": "https://dev-api.desk.exchange",
    "arbitrumSepolia": "https://dev-api.desk.exchange",
    "bscTestnet": "https://dev-api.desk.exchange"
}

WSS_URLS: Dict[NetworkOption, str] = {
    "mainnet": "wss://ws-api.happytrading.global/ws",
    "mainnetBase": "wss://ws-api.happytrading.global/ws",
    "mainnetArbitrum": "wss://ws-api.happytrading.global/ws",
    "mainnetBsc": "wss://ws-api.happytrading.global/ws",
    "testnet": "wss://stg-trade-ws-api.happytrading.global/ws",
    "testnetBase": "wss://stg-trade-ws-api.happytrading.global/ws",
    "testnetArbitrum": "wss://stg-trade-ws-api.happytrading.global/ws",
    "testnetBsc": "wss://stg-trade-ws-api.happytrading.global/ws",
    "base": "wss://ws-api.happytrading.global/ws",
    "arbitrum": "wss://ws-api.happytrading.global/ws",
    "bsc": "wss://ws-api.happytrading.global/ws",
    "baseSepolia": "wss://stg-trade-ws-api.happytrading.global/ws",
    "arbitrumSepolia": "wss://stg-trade-ws-api.happytrading.global/ws",
    "bscTestnet": "wss://stg-trade-ws-api.happytrading.global/ws"
}

CHAIN_ID: Dict[NetworkOption | ChainOption, int] = {
    "mainnet": 8453,
    "mainnetBase": 8453,
    "mainnetArbitrum": 42161,
    "mainnetBsc": 56,
    # for consistency, 'testnet' key referred to arbitrum sepolia
    "testnet": 421614,
    "testnetBase": 84532,
    "testnetArbitrum": 421614,
    "testnetBsc": 97,
    "base": 8453,
    "arbitrum": 42161,
    "bsc": 56,
    "baseSepolia": 84532,
    "arbitrumSepolia": 421614,
    "bscTestnet": 97
}
