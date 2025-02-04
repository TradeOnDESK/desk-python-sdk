from eth_account import Account
from web3 import Web3
from eth_keys import keys
from eth_account.messages import  encode_defunct

from desk.api import Api
from desk.utils.utils import generate_nonce, get_sub_account

class Auth(Api):
    """Authentication class for DESK. Is needed if want to use "Exchange" class.

    Args:
        chain_id (int): chain id (8453 for base mainnet) other can be found on https://chainlist.org/
        rpc_url (str): rpc url can be found on https://chainlist.org/
        account (str): evm account address
        sub_account_id (int): sub account id (max 255 but in web only display up to 5 (0 - 4))
        private_key (str): private key
        jwt (str): jwt (if provided, skip generating)

    """
    def __init__(self, chain_id: int, rpc_url: str, account: str, sub_account_id: int, private_key: str, jwt: str = None):
        if not chain_id or not rpc_url or not sub_account_id or not private_key or not account:
                raise ValueError("chain_id, rpc_url, sub_account_id, and private_key are required")
        super().__init__()
        self.chain_id = chain_id
        self.rpc_url = rpc_url
        self.sub_account_id = str(sub_account_id)

        self.eth_provider = self.__get_provider()
        self.eth_signer = Account.from_key(private_key)
        self.account = account

        self.sub_account = get_sub_account(account, sub_account_id)
        
        if jwt:
            print('JWT provided, skip generating...')
            self.jwt = jwt
        else:

            self.nonce = str(generate_nonce())
            self.signature = self.__sign_msg()

            self.jwt = self.__generate_jwt()


    def __get_provider(self) -> Web3:
        return Web3(Web3.HTTPProvider(self.rpc_url, request_kwargs={'timeout': 60}))


    def __sign_msg(self) -> str:
        msg = f"generate jwt for {self.account.lower()} and subaccount id {self.sub_account_id} to trade on happytrading.global with nonce: {self.nonce}"

        encoded_msg = encode_defunct(text=msg)
        pk = keys.PrivateKey(self.eth_signer.key)
        signed_data = Account.sign_message(encoded_msg, pk)

        return signed_data.signature.hex()
    
    def __generate_jwt(self) -> str:
        jwt = self.__api_generate_jwt(self.account, self.sub_account_id, self.nonce, self.signature)

        return jwt
    
    def __api_generate_jwt(self, account: str, sub_account_id: str, nonce: str, signature: str) -> str:
        resp = self.post(f"/v2/auth/evm", payload={
            "account": account,
            "subaccount_id": sub_account_id,
            "nonce": nonce,
            "signature": signature
        })

        return resp["jwt"]