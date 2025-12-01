import os
import resend
from dotenv import load_dotenv

# Load variables from backend/.env
load_dotenv()

# Read the API key from the environment
resend.api_key = os.getenv("RESEND_API_KEY")

if not resend.api_key:
    raise ValueError("RESEND_API_KEY is missing from .env file")

def send_test_email(to_email: str):
    params = {
        "from": "onboarding@resend.dev",   # testing domain
        "to": [to_email],
        "subject": "Test Email",
        "html": "<strong>It works!</strong>"
    }
    return resend.Emails.send(params)

if __name__ == "__main__":
    # IMPORTANT:
    # In Resend Test Mode, only your own email works.
    result = send_test_email("gmmm3890@gmail.com")
    print(result)
