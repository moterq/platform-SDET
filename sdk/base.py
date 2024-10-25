import logging
import requests

from typing import Optional
from sdk.logger import logger


class BaseHttpRequester:
    session = requests.Session()

    def __init__(self, base_url, uri_prefix, base_url_int=None):
        if base_url is None:
            raise ValueError("`base_url` is None")
        if uri_prefix is None:
            raise ValueError("`uri_prefix` is None")

        self.base_url = base_url.rstrip("/")

        if base_url_int is not None:
            self.base_url_int = base_url_int.rstrip("/")

        self.uri_prefix = "/" + uri_prefix.lstrip("/")
        self.logger = logging.getLogger(type(self).__name__)

    def _do_get(
        self,
        uri: str,
        params: Optional[dict] = None,
    ):
        return self._do_request(
            uri=uri,
            method="GET",
            params=params,
        )

    def _do_post(
        self,
        uri: str,
        json: Optional[dict] = None,
    ):
        return self._do_request(
            uri=uri,
            method="POST",
            json=json,
        )

    def _do_delete(
        self,
        uri: str,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        cookies: Optional[dict] = None,
        headers: Optional[dict] = None,
    ):
        return self._do_request(
            uri=uri,
            method="DELETE",
            json=json,
            params=params,
            cookies=cookies,
            headers=headers,
        )

    def _do_request(  # noqa: C901
        self,
        uri: str,
        method: str,
        json: Optional[dict] = None,
        data: Optional[dict] = None,
        params: Optional[dict] = None,
        cookies: Optional[dict] = None,
        headers: Optional[dict] = None,
        files: Optional[dict] = None,
    ) -> requests.Response:
        base_url = self.base_url
        url = base_url + self.uri_prefix + uri

        request_params = {
            "url": url,
            "json": json,
            "data": data,
            "params": params,
            "headers": headers,
            "cookies": cookies,
            "files": None if files is None else files
        }

        if method == "GET":
            logger.add_request(url, params, headers, cookies, method, files)
        else:
            logger.add_request(url, json, headers, cookies, method, files)

        response = self.session.request(method=method, allow_redirects=True, timeout=20, **request_params)
        logger.add_response(response)

        return response
