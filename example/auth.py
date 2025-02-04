import os
from pathlib import Path
import sys
from dotenv import load_dotenv

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + '/src')

from desk import auth  # noqa

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("RPC_URL")
ACCOUNT = os.getenv("ACCOUNT")
CHAIN_ID = os.getenv("CHAIN_ID")
WS_URL = os.getenv("WS_URL")
JWT_KEY = os.getenv("JWT_KEY")

def main():
    # Generating new JWT
    jwt = auth.Auth(private_key=PRIVATE_KEY, rpc_url=RPC_URL,
                    chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=2)
    print(jwt.jwt)

    # Injecting existing JWT. This will skip JWT generation process.
    jwt2 = auth.Auth(private_key=PRIVATE_KEY, rpc_url=RPC_URL,
                    chain_id=CHAIN_ID, account=ACCOUNT, sub_account_id=2, jwt=JWT_KEY)
    print(jwt2.jwt)


if __name__ == "__main__":
    main()
