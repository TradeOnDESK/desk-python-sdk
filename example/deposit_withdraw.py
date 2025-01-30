import os
from pathlib import Path
import sys
from dotenv import load_dotenv

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root)+'/src')

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
ACCOUNT = os.getenv("ACCOUNT")
CHAIN_ID = os.getenv("CHAIN_ID")
WS_URL = os.getenv("WS_URL")

from desk import auth
from desk.exchange import Exchange


def deposit():
    jwt = auth.Auth(private_key=PRIVATE_KEY, rpc_url=RPC_URL, chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=2)
    exchange = Exchange(auth=jwt)
    tx_hash = exchange.deposit_collateral('USDC', 10)
    print(tx_hash)

def withdraw():
    jwt = auth.Auth(private_key=PRIVATE_KEY, rpc_url=RPC_URL, chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=2)
    exchange = Exchange(auth=jwt)
    tx_hash = exchange.withdraw_collateral('USDC', 10)
    print(tx_hash)

def main():
    deposit()
    withdraw()

if __name__ == "__main__":
    main()