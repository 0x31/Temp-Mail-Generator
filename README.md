# Temporary Email Generator

This Python script generates a temporary email address and checks the inbox of the generated email. It uses the TempMail API and includes a retry mechanism for handling HTTP request errors.

## Features

- Generates a temporary email address.
- Checks the inbox of the generated email.
- Includes a retry mechanism for handling HTTP request errors.

## Classes

- `Retry`: A decorator for retrying a function that raises an exception.
- `EnhancedHTTPClient`: A HTTP client with a retry mechanism for handling HTTP request errors.
- `EmailGenerator`: A class for generating a temporary email address and checking its inbox.

## Usage
```python
if __name__ == "__main__":
    # Create an instance of EmailGenerator
    emailGenerator = EmailGenerator()

    # Generate a new email address
    address, token = emailGenerator.generateEmail()
    print(f"[*] Generated Email Address: {address}")

    # Check the inbox of the generated email
    inbox = emailGenerator.returnInbox(token)

    # If there are new emails, print them
    if inbox:
        print(f"[*] New email(s) in inbox:")
        for email in inbox:
            print(f"    - {email}")
    else:
        print("[!] No new emails in inbox...")
```
In this example, an `EmailGenerator` object is created. The `generateEmail` method is called to generate a temporary email address. The `returnInbox` method is called to check the inbox of the generated email. If there are any new emails in the inbox, they are printed to the console.

## Dependencies

- Python 3.6+
- `requests` library
- `json` library
- `logging` library
- `time` library
- `functools.wraps` decorator

## Installation

1. Ensure that you have Python 3.6 or later installed.
2. Install the `requests` library using pip: ```pip install requests```
3. Download the script and run it with Python: ```python generator.py```


## Note

This script uses the TempMail API, which is a free service for generating temporary email addresses. Please use this script responsibly and in accordance with the TempMail API's terms of service.
