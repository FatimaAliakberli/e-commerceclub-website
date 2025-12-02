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
        "from": "E-Commerce Club <no-reply@e-commerceclubada.xyz>",   # from website's domain
        "to": [to_email],
        "subject": "Test Email",
        "html": "<strong>It works!</strong>"
    }
    return resend.Emails.send(params)

if __name__ == "__main__":
    result = send_test_email("huseynm103@gmail.com") # sample email in the brackets
    print(result)
