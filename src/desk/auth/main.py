from eth_account import Account
from web3 import Web3
from eth_keys import keys
from eth_account.messages import  encode_defunct

from desk.api import api_generate_jwt
from desk.utils import generate_nonce

class Auth:
    def __init__(self, chain_id: int = None, rpc_url: str = None, sub_account_id: str = None, private_key: str = None, jwt: str = None):
        if jwt:
            self.jwt = jwt
        else:
            if not chain_id or not rpc_url or not sub_account_id or not private_key:
                raise ValueError("chain_id, rpc_url, sub_account_id, and private_key are required if jwt is not provided")

            self.chain_id = chain_id
            self.rpc_url = rpc_url
            self.sub_account_id = sub_account_id
            self.provider = self.__get_provider()

            self.eth_signer = Account.from_key(private_key)
            self.account = self.eth_signer.address

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
        jwt = api_generate_jwt(self.account, self.sub_account_id, self.nonce, self.signature)

        return jwt
    