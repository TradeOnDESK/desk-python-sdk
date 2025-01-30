import os
from dotenv import load_dotenv
from web3 import Web3
from desk.api import Api
from desk.auth import Auth
from desk.types import CancelOrderFn, CancelOrderRequestV2, CreatePlaceOrderFn, OrderRequestV2
from desk.constant.contract import VAULT_CONTRACT_ABI, ERC20_ABI_PATH
from desk.utils import (
    load_contract, 
    get_contract_address, 
    map_token_profile,
    generate_nonce
)

load_dotenv()

WS_URL = os.getenv("WS_URL")
API_URL = os.getenv("API_URL")
BROKER = os.getenv("BROKER")


class Exchange:
    def __init__(self, api_url: str = API_URL, broker: str = BROKER, auth: Auth = None):
        self.jwt = auth.jwt
        self.auth = auth

        if not auth or not auth.jwt:
            raise Exception("Auth is required")

        self.api = Api(api_url=api_url, headers={
                       "Authorization": f"Bearer {self.jwt}"})
        self.api_url = api_url
        self.broker = broker

        self.contract_address = get_contract_address(self.auth.chain_id)

        self.vault_contract = load_contract(
            self.auth.eth_provider, self.contract_address["peripherals"]["vault"], VAULT_CONTRACT_ABI)

        self.token_profile = self.__get_token_profile()

    def __get_token_profile(self):
        resp = self.api.get("/v2/collaterals")
        if resp["code"] != 200:
            raise Exception("Failed to get token profile")
        return map_token_profile(resp["data"], self.auth.chain_id)

    def __create_place_order_payload(self, order: CreatePlaceOrderFn):
        nonce = generate_nonce()

        payload: OrderRequestV2 = {
            "nonce": str(nonce),
            "amount": order["amount"],
            "price": order["price"],
            "side": order["side"],
            "symbol": order["symbol"],

            "order_type": order["orderType"],

            "broker_id": self.broker,
            "subaccount": self.auth.sub_account,
        }

        if "reduceOnly" in order:
            payload["reduce_only"] = order["reduceOnly"]

        if "triggerPrice" in order:
            payload["trigger_price"] = order["triggerPrice"]

        if order["orderType"] == "Limit" or "Stop":
            payload["time_in_force"] = order["timeInForce"]

        return payload

    def place_order(self, order: CreatePlaceOrderFn):
        payload = self.__create_place_order_payload(order)
        return self.api.post("/v2/place-order", payload=payload)

    def __create_cancel_order_payload(self, order: CancelOrderFn) -> CancelOrderRequestV2:
        nonce = generate_nonce()

        payload: CancelOrderRequestV2 = {
            "nonce": str(nonce),
            "subaccount": self.auth.sub_account,
            "symbol": order["symbol"],
            "order_digest": order["orderDigest"],
            "is_conditional_order": order["isConditionalOrder"],
            "wait_for_reply": False
        }

        return payload

    def cancel_order(self, order: CancelOrderFn):
        payload = self.__create_cancel_order_payload(order)
        return self.api.post("/v2/cancel-order", payload=payload)

    def deposit_collateral(self, asset: str, amount: float):
        collateral = self.token_profile[asset]
        collateral_address = collateral["address"]

        vault_address = Web3.to_checksum_address(
            self.contract_address["peripherals"]["vault"])

        if not collateral_address:
            raise Exception("Collateral address not found")

        checksum_collateral_address = Web3.to_checksum_address(
            collateral_address)
        
        token_instance = load_contract(
            self.auth.eth_provider, checksum_collateral_address, ERC20_ABI_PATH)
        
        token_decimal = token_instance.functions.decimals().call()
        amount_wei = int(
            amount * 10 ** token_decimal)
        
        min_deposit = self.vault_contract.functions.minDeposits(checksum_collateral_address).call()
        if amount_wei < min_deposit:
            raise Exception(f"Amount is less than minimum deposit {float(min_deposit) / 10 ** token_decimal} {collateral['asset']}")

        signer_address = Web3.to_checksum_address(self.auth.eth_signer.address)

        allowance = token_instance.functions.allowance(
            signer_address, vault_address).call()

        if allowance < amount_wei:
            self.__send_transaction(token_instance.functions.approve(vault_address, amount_wei))
            
        return self.__send_transaction(self.vault_contract.functions.deposit(checksum_collateral_address, self.auth.sub_account, amount_wei))


    def withdraw_collateral(self, asset: str, amount: float):
        collateral = self.token_profile[asset]
        collateral_address = collateral["address"]

        if not collateral_address:
            raise Exception("Collateral address not found")
        
        checksum_collateral_address = Web3.to_checksum_address(
            collateral_address)
        
        is_withdrawable = self.vault_contract.functions.withdrawableTokens(checksum_collateral_address).call()
        if not is_withdrawable:
            raise Exception(f"Collateral {asset} is not withdrawable")

        token_instance = load_contract(
            self.auth.eth_provider, checksum_collateral_address, ERC20_ABI_PATH)
        
        token_decimal = token_instance.functions.decimals().call()
        amount_wei = int(
            amount * 10 ** token_decimal)
        
        return self.__send_transaction(self.vault_contract.functions.withdraw(checksum_collateral_address, self.auth.sub_account, amount_wei))
    

    def __send_transaction(self, function):
        txn = function.build_transaction({
            "from": self.auth.eth_signer.address,
            "nonce": self.auth.eth_provider.eth.get_transaction_count(self.auth.eth_signer.address),
            "gas": 1000000,
            "gasPrice": self.auth.eth_provider.eth.gas_price
        })

        signed_txn = self.auth.eth_signer.sign_transaction(txn)
        txn_hash = self.auth.eth_provider.eth.send_raw_transaction(signed_txn.rawTransaction)
        if self.auth.eth_provider.eth.wait_for_transaction_receipt(txn_hash) == 0:
            raise Exception(f"Failed to send transaction {function} {txn_hash.hex()}")
        return txn_hash.hex()
