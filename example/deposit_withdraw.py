from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root)+'/src')

from desk import auth
from desk.exchange import Exchange

from constants import API_URL, RPC_URL, CHAIN_ID, ACCOUNT, PRIVATE_KEY, SUB_ACCOUNT_ID, CRM_URL

def deposit():
    jwt = auth.Auth(api_url=API_URL, crm_url=CRM_URL, private_key=PRIVATE_KEY, rpc_url=RPC_URL, chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=SUB_ACCOUNT_ID)
    exchange = Exchange(api_url=API_URL, crm_url=CRM_URL, auth=jwt)
    tx_hash = exchange.deposit_collateral('USDC', 10)
    print(tx_hash)

def withdraw():
    jwt = auth.Auth(api_url=API_URL, crm_url=CRM_URL, private_key=PRIVATE_KEY, rpc_url=RPC_URL, chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=SUB_ACCOUNT_ID)
    exchange = Exchange(api_url=API_URL, crm_url=CRM_URL, auth=jwt)
    tx_hash = exchange.withdraw_collateral('USDC', 10)
    print(tx_hash)

def main():
    deposit()
    withdraw()

if __name__ == "__main__":
    main()