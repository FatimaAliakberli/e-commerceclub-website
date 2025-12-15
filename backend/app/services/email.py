import os
from datetime import datetime

import resend

# REQUIRED in Railway variables
resend.api_key = os.environ["RESEND_API_KEY"]

# Optional in Railway variables (these defaults are your real production values)
EMAIL_FROM = os.getenv("EMAIL_FROM", "E-Commerce Club <no-reply@e-commerceclubada.xyz>")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://www.e-commerceclubada.xyz")


def _send(to_email: str, subject: str, html: str):
    # Don’t crash your endpoint if Resend has an issue
    try:
        return resend.Emails.send(
            {
                "from": EMAIL_FROM,
                "to": [to_email],
                "subject": subject,
                "html": html,
            }
        )
    except Exception as e:
        print(f"[EMAIL] Resend error: {e}")
        return None


def send_registration_confirmation(email: str, full_name: str):
    login_link = f"{FRONTEND_URL}/login"
    html = f"""
        <h2>Welcome to E-Commerce Club 🎉</h2>
        <p>Hello {full_name},</p>
        <p>Your account has been created successfully.</p>
        <p><a href="{login_link}">Log in</a></p>
    """
    return _send(email, "Welcome to E-Commerce Club!", html)


def send_event_registration_confirmation(
    email: str,
    full_name: str,
    event_title: str,
    event_date: datetime,
    event_time: str | None,
    location: str,
):
    date_str = event_date.strftime("%Y-%m-%d %H:%M")
    time_str = event_time if event_time else "TBA"

    html = f"""
        <h2>Registration confirmed ✅</h2>
        <p>Hello {full_name},</p>
        <p>You have registered for:</p>
        <ul>
          <li><b>Event:</b> {event_title}</li>
          <li><b>Date:</b> {date_str}</li>
          <li><b>Time:</b> {time_str}</li>
          <li><b>Location:</b> {location}</li>
        </ul>
        <p>See you there!</p>
    """
    return _send(email, f"You're registered: {event_title}", html)

async def send_verification_email(
    email: str,
    verification_token: str,
    user_name: str
):
    verification_link = f"{FRONTEND_URL}/verify-email?token={verification_token}"

    html = f"""
        <h2>Email Verification</h2>
        <p>Hello {user_name},</p>
        <p>Please confirm your new email address by clicking the link below:</p>
        <p>
            <a href="{verification_link}">
                Verify Email
            </a>
        </p>
        <p>If you did not request this change, please ignore this email.</p>
    """

    # call sync sender inside async function (this is OK)
    _send(email, "Verify your email address", html)
