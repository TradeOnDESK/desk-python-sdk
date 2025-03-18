from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root)+'/src')

from desk import auth
from desk.exchange import Exchange
from desk.enum import CollateralSymbol
from constants import RPC_URL, ACCOUNT, PRIVATE_KEY, SUB_ACCOUNT_ID, NETWORK

def deposit():
    jwt = auth.Auth(network=NETWORK, private_key=PRIVATE_KEY, rpc_url=RPC_URL, account=ACCOUNT, sub_account_id=SUB_ACCOUNT_ID)
    exchange = Exchange(network=NETWORK, auth=jwt)
    tx_hash = exchange.deposit_collateral(CollateralSymbol.USDC, 10)
    print(tx_hash)

def withdraw():
    jwt = auth.Auth(network=NETWORK, private_key=PRIVATE_KEY, rpc_url=RPC_URL, account=ACCOUNT, sub_account_id=SUB_ACCOUNT_ID)
    exchange = Exchange(network=NETWORK, auth=jwt)
    tx_hash = exchange.withdraw_collateral(CollateralSymbol.USDC, 10)
    print(tx_hash)

def main():
    deposit()
    withdraw()

if __name__ == "__main__":
    main()