# BitNet API - A client for Microsoft BitNet demo API
# Copyright (C) 2025  Axel Sheire

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
import json
import time


class PollingError(Exception):
    pass


class BitNetClient:
    def __init__(self, device="gpu", user_id="user_default", chat_id="chat_default", verbose=True):
        self.device = device
        self.user_id = user_id
        self.chat_id = chat_id
        self.verbose = verbose
        self.history = []

        self.base_url = "https://bitnet-demo.azurewebsites.net"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "BitNetClient/1.0"
        }

    def send(self, message, stream=False):
        if self.device == "gpu":
            return self._send_gpu(message)
        return self._send_cpu(message) if not stream else self._stream_cpu(message)

    def _send_gpu(self, message):
        payload = {
            "messages": {
                "prompt": message,
                "history": self.history
            },
            "userId": self.user_id,
            "chatId": self.chat_id,
            "device": "gpu"
        }

        try:
            res = requests.post(f"{self.base_url}/completion", headers=self.headers, json=payload)
            res.raise_for_status()
            data = res.json()
            request_id = data.get("request_id")
            if not request_id:
                raise ValueError("No request_id in GPU response.")
        except Exception as e:
            raise RuntimeError(f"Failed to send GPU request: {e}")

        result = self._poll_gpu_result(request_id)
        response = result["data"]["response"]
        self.history = result["data"]["updated_history"]
        return response

    def _poll_gpu_result(self, request_id):
        url = f"{self.base_url}/gpuresult/{request_id}"
        while True:
            try:
                r = requests.get(url, headers=self.headers)
                r.raise_for_status()
                result = r.json()
                if result.get("status") == "complete":
                    return result
                time.sleep(0.25)
            except Exception as e:
                raise PollingError(f"Polling failed for GPU result: {e}")

    def _send_cpu(self, message):
        self.history.append({"role": "user", "content": message})
        payload = {
            "messages": self.history,
            "userId": self.user_id,
            "chatId": self.chat_id,
            "device": "cpu"
        }

        response_text = ""
        try:
            with requests.post(f"{self.base_url}/completion", headers=self.headers, json=payload, stream=True) as r:
                for line in r.iter_lines():
                    if line and line.startswith(b"data: "):
                        data = json.loads(line[6:])
                        if data.get("finished"):
                            break
                        token = data.get("content", "")
                        response_text += token
        except Exception as e:
            raise RuntimeError(f"Failed during CPU response: {e}")

        self.history.append({"role": "assistant", "content": response_text})
        return response_text

    def _stream_cpu(self, message):
        self.history.append({"role": "user", "content": message})
        payload = {
            "messages": self.history,
            "userId": self.user_id,
            "chatId": self.chat_id,
            "device": "cpu"
        }

        response_text = ""

        def generator():
            nonlocal response_text
            try:
                with requests.post(f"{self.base_url}/completion", headers=self.headers, json=payload, stream=True) as r:
                    for line in r.iter_lines():
                        if line and line.startswith(b"data: "):
                            data = json.loads(line[6:])
                            if data.get("finished"):
                                break
                            token = data.get("content", "")
                            response_text += token
                            yield token
            except Exception as e:
                raise RuntimeError(f"Streaming failed: {e}")
            finally:
                self.history.append({"role": "assistant", "content": response_text})

        return generator()
