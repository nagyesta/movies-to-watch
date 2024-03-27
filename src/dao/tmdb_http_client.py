import json
from typing import Any

import requests


class TmdbHttpClientException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def _process_response(response) -> Any:
    if response.status_code >= 200 & response.status_code < 300:
        try:
            return response.json()
        except json.decoder.JSONDecodeError as error:
            raise TmdbHttpClientException("Invalid Response: " + error.msg)
    elif response.status_code == 400:
        raise TmdbHttpClientException("Bad Request")
    elif response.status_code == 401:
        raise TmdbHttpClientException("Unauthorized")
    elif response.status_code == 404:
        raise TmdbHttpClientException("Not Found")
    elif response.status_code == 500:
        raise TmdbHttpClientException("Internal Server Error")


class TmdbHttpClient:

    def __init__(self, token: str, base_url: str = "https://api.themoviedb.org/3"):
        self.__base_url = base_url
        self.__token = token

    def get(self, path: str, params: dict, additional_headers: dict) -> Any:
        default_headers = self.__get_default_headers()
        headers = {**default_headers, **additional_headers}

        url = self.__base_url + path
        response = requests.get(url=url, params=params, headers=headers)
        return _process_response(response)

    def post(self, path: str, content_type: str, payload: dict, additional_headers: dict) -> Any:
        content_type_header = {"Content-Type": f"{content_type}"}
        default_headers = self.__get_default_headers()
        headers = {**content_type_header, **default_headers, **additional_headers}

        url = self.__base_url + path
        response = requests.post(url=url, json=payload, headers=headers)
        return _process_response(response)

    def put(self, path: str, content_type: str, payload: dict, additional_headers: dict) -> Any:
        content_type_header = {"Content-Type": f"{content_type}"}
        default_headers = self.__get_default_headers()
        headers = {**content_type_header, **default_headers, **additional_headers}

        url = self.__base_url + path
        response = requests.put(url=url, json=payload, headers=headers)
        return _process_response(response)

    def delete(self, path: str, params: dict, additional_headers: dict) -> Any:
        default_headers = self.__get_default_headers()
        headers = {**default_headers, **additional_headers}

        url = self.__base_url + path
        response = requests.delete(url=url, params=params, headers=headers)
        return _process_response(response)

    def __get_default_headers(self):
        return {
            "accept": "application/json",
            "Authorization": f"Bearer {self.__token}"
        }
