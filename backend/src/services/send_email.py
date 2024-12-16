from postmarker.core import PostmarkClient
from .. core.config import settings

server_token = settings.POSTMARK_SERVER_TOKEN
sender_email = settings.SENDER_EMAIL
def send_approval_message(email: str,temp_password: str):
    postmark = PostmarkClient(server_token=server_token)
    postmark.emails.send(
        From=sender_email,
        To=email,
        Subject="Verify Your Email with Academly",
        TextBody=f"""Your account has been verified 
        by the admin, You have been provided with a temporary
        password, ensure to chnage your password after login
        Temporary Password: {temp_password}
        """
    )


def send_reset_token(email: str, reset_token: str) -> bool:
    """
    Sends a password reset token to the provided email address.

    Args:
        email (str): The recipient's email address.
        reset_token (str): The password reset token.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        postmark = PostmarkClient(server_token=server_token)
        postmark.emails.send(
            From=sender_email,
            To=email,
            Subject="Reset Your Password from Academly",
            TextBody=f"""
            You are receiving this email because you requested a password reset for your account.
            Please click on the following link to reset your password:
            https://your-domain.com/reset_password/{reset_token}
            If you did not request a password reset, please ignore this email.
            """
        )
        return True  # Email sent successfully
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error sending reset token to {email}: {e}")
        return False  # Email sending failed


def send_enrol_confirm(email: str) -> bool:
    """
    Sends an enrollment confirmation email to the provided email address.

    Args:
        email (str): The recipient's email address.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        postmark = PostmarkClient(server_token=server_token)
        postmark.emails.send(
            From=sender_email,
            To=email,
            Subject="Enrollment Confirmation Email",
            TextBody=f"""
            Your enrollment is under review by the admin.
            You will receive a confirmation email once your account
            has been approved by the admin.
            """
        )
        return True  # Email sent successfully
    except Exception as e:
        # Log the exception for debugging or monitoring
        print(f"Error sending enrollment confirmation to {email}: {e}")
        return False  # Email sending failed

    


def admin_enrol_user_confirm(email: str, temp_pwd: str) -> bool:
    """
    Sends an enrollment confirmation email to the provided email address.

    Args:
        email (str): The recipient's email address.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        postmark = PostmarkClient(server_token=server_token)
        postmark.emails.send(
            From=sender_email,
            To=email,
            Subject="Enrollment Confirmation Email",
            TextBody=f"""
            An account was created on your behalf
            Here are you login credentials,
            Username: {email}
            Temporary Password: {temp_pwd}
            """
        )
        return True  # Email sent successfully
    except Exception as e:
        # Log the exception for debugging or monitoring
        print(f"Error sending enrollment confirmation to {email}: {e}")
        return False  # Email sending failed
    

def send_password_reset_link(email: str, token: str) -> bool:
    """
    Sends reset link email to the provided email address.

    Args:
        email (str): The recipient's email address.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    try:
        postmark = PostmarkClient(server_token=server_token)
        postmark.emails.send(
            From=sender_email,
            To=email,
            Subject="Password Recovery link",
            TextBody=f"""
            You have requested a password reset.
            Please click on the following link to reset your password:
            http://localhost:8000/auth/reset-password?token={token}
            If you did not request a password reset, please ignore this email.
            """
            
        )
        return True  # Email sent successfully
    except Exception as e:
        # Log the exception for debugging or monitoring
        print(f"Error sending enrollment confirmation to {email}: {e}")
        return False