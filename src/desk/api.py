import json
import logging
from typing import Any
import requests as r
from desk.utils.error import ClientError, ServerError


class Api:
    def __init__(self, api_url: str, headers: dict = None):
        if not api_url:
            raise Exception("api_url is required")
        self.api_url = api_url
        self.session = r.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self._logger = logging.getLogger(__name__)

        if headers:
            self.session.headers.update(headers)

    def post(self, url_path: str, payload: Any = None) -> Any:
        payload = payload or {}
        url = self.api_url + url_path
        response = self.session.post(url, json=payload)
        self.__handle_exception(response)

        try:
            return response.json()["data"]
        except ValueError:
            return {"error": f"Could not parse JSON: {response.text}"}
        
    def get(self, url_path: str, params: dict = None):
        url = self.api_url + url_path
        response = self.session.get(url, params=params)
        self.__handle_exception(response)

        try:
            return response.json()["data"]
        except ValueError:
            return {"error": f"Could not parse JSON: {response.text}"}  
        
    def __handle_exception(self, response: r.Response):
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except json.JSONDecodeError:
                raise ClientError(status_code, None, response.text, None, response.headers)
            if err is None:
                raise ClientError(status_code, None, response.text, None, response.headers)
            error_data = err.get("errors")
            raise ClientError(status_code, err["code"], err["message"], response.headers, error_data)
        raise ServerError(status_code, response.text)
