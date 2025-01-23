import requests as r
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

def api_generate_jwt(account: str, sub_account_id: str, nonce: str, signature: str) -> str:
    resp = r.post(f"{API_URL}/v2/auth/evm", json={
        "account": account,
        "subaccount_id": sub_account_id,
        "nonce": nonce,
        "signature": signature
    })

    if resp.status_code != 200:
        raise Exception(f"Failed to generate JWT: {resp.text}")

    return resp.json()["data"]["jwt"]
