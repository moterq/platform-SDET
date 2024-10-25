import datetime
import os
import traceback

import allure
from requests import Response

from sdk.on_failure_printer import on_failure_printer


class Logger:
    logs_path = os.path.join("logs")
    timestamp_dir_path = (
        logs_path
        if "CI" in os.environ
        else os.path.join(logs_path, str(datetime.datetime.now()).replace(":", "_").replace(" ", "_"))
    )
    requests_counter = 0

    def add_request(self, url: str, data: dict, headers: dict, cookies: dict, method: str, files: dict):
        testname = os.environ.get("PYTEST_CURRENT_TEST")
        files_list_of_paths = []
        if files:
            for k in files:
                if len(files[k]) == 3 and files[k][1]:
                    files_list_of_paths.append(files[k][1].name)

        self.requests_counter += 1
        data_to_add = "\n--------\n"
        data_to_add += f"Request №{self.requests_counter}\n"

        data_to_add += f"Test: {testname}\n"
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n"
        data_to_add += f"Request headers: {headers}\n"
        data_to_add += f"Request cookies: {cookies}\n"
        if len(files_list_of_paths) > 0:
            data_to_add += "Files: " + "; ".join(files_list_of_paths) + "\n"

        trace_list = traceback.extract_stack()
        trace_counter = 0
        data_to_add += "\nTrace:\n"
        for frame in trace_list:
            if "/api-tests/" in frame.filename:
                trace_counter += 1
                filename = frame.filename.split("/api-tests/")[1]
                data_to_add += f"#{trace_counter}: {filename}:{frame.lineno}\n"

        data_to_add += "\nCurl:\n"
        curl_data = self._log_curl(
            url=url, data=data, headers=headers, cookies=cookies, method=method, files_list=files_list_of_paths
        )
        data_to_add += curl_data
        data_to_add += "\n\n"

        self._write_log_to_file(data_to_add)
        allure.attach(curl_data, name="Request", attachment_type=allure.attachment_type.TEXT)

    def add_response(self, response: Response):
        cookies_as_dict = dict(response.cookies)
        headers_as_dict = dict(response.headers)

        data_to_add = f"Response code: {response.status_code}\n"
        data_to_add += f"Response elapsed: {response.elapsed}\n"
        data_to_add += f"Response text: {response.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}"
        data_to_add += "\n--------\n"

        self._write_log_to_file(data_to_add)
        allure.attach(data_to_add, name="Response", attachment_type=allure.attachment_type.TEXT)

    def move_log_to_status_dir(self, status_dir_name: str):
        if not status_dir_name.startswith("/"):
            status_dir_name = "/" + status_dir_name

        status_dir_path = self.timestamp_dir_path + status_dir_name
        if not os.path.exists(status_dir_path):
            os.makedirs(status_dir_path)

        file_name = self._get_current_log_file_name(base_dir=self.timestamp_dir_path)
        new_file_name = self._get_current_log_file_name(base_dir=status_dir_path)

        if os.path.exists(file_name):
            os.rename(file_name, new_file_name)

        # print logfile name if a test failed
        on_failure_printer.set_current_logger_file(new_file_name.replace(self.logs_path, "logs/failed"))

    def _write_log_to_file(self, data: str):
        if not os.path.exists(self.timestamp_dir_path):
            os.makedirs(self.timestamp_dir_path)

        file_name = self._get_current_log_file_name(base_dir=self.timestamp_dir_path)

        with open(file_name, "a", encoding="utf-8") as logger_file:
            logger_file.write(data)

    def _get_current_log_file_name(self, base_dir=None):
        if os.environ.get("PYTEST_CURRENT_TEST"):
            log_file_name = str(os.environ.get("PYTEST_CURRENT_TEST"))
            log_file_name = log_file_name.split(" ")[0].replace("/", "_").replace(":", "_").replace("tests_", "")
            log_file_name += ".log"
        else:
            log_file_name = "default_logs_name.log"

        if base_dir is not None:
            log_file_name = os.path.join(
                base_dir,
                log_file_name,
            )

        return log_file_name

    def _log_curl(self, method: str, url: str, headers: dict, cookies: dict, data: dict, files_list: list) -> str:
        headers_str = ""
        if headers:
            headers_str = " ".join([f"-H '{key}: {value}'" for key, value in headers.items()])

        cookies_str = ""
        if cookies:
            cookies_as_pair_str = "; ".join([f"{key}: {value}" for key, value in cookies.items()])
            cookies_str = f'-H "cookies: {cookies_as_pair_str}"'

        data_str = ""
        if data:
            if method == "GET":
                url = f"{url}?" + "&".join([f"{key}={value}" for key, value in data.items()])
            else:
                data_str = str(data).replace("'", '"')
                data_str = data_str.replace("True", "true").replace("False", "false")
                data_str = f"-d '{data_str}'"
        data_str = data_str.replace("None", "null")

        files_str = ""
        if files_list:
            for file_path in files_list:
                files_str += f'-F "file=@{file_path}"'

        return f"curl -X {method} -L '{url}' {headers_str} {cookies_str} {data_str} {files_str}"


logger = Logger()
