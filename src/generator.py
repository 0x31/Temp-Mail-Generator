import time
import requests
import json
import logging
from typing import Tuple, Optional
from requests.exceptions import HTTPError, ConnectionError, Timeout
from functools import wraps

class Retry:
    def __init__(self, retries=5, delay=1, backoff=2, exceptions=(Exception,)):
        self.retries = retries
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(self.retries):
                try:
                    return func(*args, **kwargs)
                except self.exceptions as e:
                    time.sleep(self.delay)
                    self.delay *= self.backoff
                    if _ == self.retries - 1:
                        logging.error(f"[!] Hit max retries to request... {e}")
                        raise
        return wrapper

class EnhancedHTTPClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "TempMailPythonAPI/1.0",
            "Accept": "application/json"
        })

    @Retry(retries=3, delay=1, backoff=2, exceptions=(HTTPError, ConnectionError, Timeout))
    def _sendHttpRequest(self, endpoint: str) -> str:
        response = self.session.get(endpoint)
        response.raise_for_status()
        return response.text, response.status_code
    
class EmailGenerator(EnhancedHTTPClient):
    def __init__(self):
        super().__init__()
        self.baseUrl = "https://api.tempmail.lol"
        self.emails = []

    def generateEmail(self) -> Tuple[str, str]:
        try:
            apiResponse, statusCode = self._sendHttpRequest(f"{self.baseUrl}/generate")
            data = json.loads(apiResponse)
            if statusCode == 201 and 'address' in data and 'token' in data:
                return data['address'], data['token']
            else:
                logging.error("[!] Invalid email format")
                raise ValueError("[!] Invalid email format")
        except json.JSONDecodeError as e:
            logging.error(f"[!] Error decoding JSON: {e}")
            raise

    def returnInbox(self, token: str) -> Optional[str]:
        initTime = time.time()
        counter = 0

        while True:
            if time.time() - initTime > 20:
                print(f"[!] returnInbox() timed out...")
                break 

            counter += 1
            print(f"[*] Checking inbox... ({counter})")

            try:
                apiResponse, statusCode = self._sendHttpRequest(f"{self.baseUrl}/auth/{token}")
                apiResponse = json.loads(apiResponse)
                if apiResponse['email'] and statusCode == 200:
                    for email in apiResponse['email']:
                        self.emails.append(email)
                    break 
                time.sleep(2)

            except json.JSONDecodeError as e:
                logging.error(f"[!] Error decoding JSON: {e}")
                raise
            except (HTTPError, ConnectionError, Timeout) as e:
                logging.error(f"[!] Error during HTTP request: {e}")

        return self.emails


"""if __name__ == "__main__":
    emailGenerator = EmailGenerator()
    address, token = emailGenerator.generateEmail()
    print(token)
    print(f"[*] Generated Email Address: {address}")

    inbox = emailGenerator.returnInbox(token)

    if inbox:
        print(f"[*] New email(s) in inbox:")
        for email in inbox:
            print(f"    - {email}")
    else:
        print("[!] No new emails in inbox...")"""
