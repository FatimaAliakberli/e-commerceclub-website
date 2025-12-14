import resend
import os
from dotenv import load_dotenv


load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

async def send_password_reset_email(email: str, reset_token: str, user_name: str):
    """Send password reset email"""
    reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
    
    params = {
        "from": "E-Commerce Club <noreply@yourdomain.com>",
        "to": [email],
        "subject": "Password Reset Request",
        "html": f"""
        <h2>Password Reset Request</h2>
        <p>Hi {user_name},</p>
        <p>You requested to reset your password. Click the link below:</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>This link expires in 1 hour.</p>
        <p>If you didn't request this, ignore this email.</p>
        """
    }
    
    try:
        email_response = resend.Emails.send(params)
        return email_response
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

async def send_registration_confirmation(email: str, user_name: str):
    """Send registration confirmation email"""
    params = {
        "from": "E-Commerce Club <noreply@yourdomain.com>",
        "to": [email],
        "subject": "Welcome to E-Commerce Club!",
        "html": f"""
        <h2>Welcome!</h2>
        <p>Hi {user_name},</p>
        <p>Your account has been created successfully.</p>
        <p>You can now log in and explore our events.</p>
        """
    }
    
    try:
        email_response = resend.Emails.send(params)
        return email_response
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

async def send_verification_email(email: str, verification_token: str, user_name: str):
    """Send email verification link (for email change or account verification)"""
    verification_link = (
        f"http://localhost:8000/api/profile/verify-email?token={verification_token}"
    )

    params = {
        "from": "E-Commerce Club <noreply@yourdomain.com>",
        "to": [email],
        "subject": "Verify Your Email Address",
        "html": f"""
        <h2>Email Verification</h2>
        <p>Please verify your email address by clicking the link below:</p>
        <p><a href="{verification_link}">Verify Email</a></p>
        <p>If you did not request this, you can safely ignore this email.</p>
        """
    }

    try:
        return resend.Emails.send(params)
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return None