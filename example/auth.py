from pathlib import Path
import sys
from constants import RPC_URL, ACCOUNT, PRIVATE_KEY, JWT_KEY, NETWORK

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + '/src')

from desk import auth  # noqa


def main():
    # Generating new JWT
    jwt = auth.Auth(network=NETWORK, private_key=PRIVATE_KEY, rpc_url=RPC_URL, account=ACCOUNT, sub_account_id=2)
    print(jwt.jwt)

    # Injecting existing JWT. This will skip JWT generation process.
    jwt2 = auth.Auth(network=NETWORK, private_key=PRIVATE_KEY, rpc_url=RPC_URL, account=ACCOUNT, sub_account_id=2, jwt=JWT_KEY)
    print(jwt2.jwt)


if __name__ == "__main__":
    main()
