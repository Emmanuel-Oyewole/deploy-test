from postmarker.core import PostmarkClient
from .. core.config import settings
from postmarker.exceptions import ClientError, SpamAssassinError

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


def send_password_reset_link(email: str, reset_token: str) -> bool:
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
            HtmlBody=f"""
            <html>
            <head>
            <style>
                body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                }}
                .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                }}
                .footer {{
                margin-top: 20px;
                font-size: 0.9em;
                color: #777;
                }}
            </style>
            </head>
            <body>
            <div class="container">
                <h2>Reset Your Password</h2>
                <p>You are receiving this email because you requested a password reset for your account.</p>
                <p>Please click on the following link to reset your password:</p>
                <p><a href="{settings.RESET_PASSWORD_URL}?token={reset_token}&email={email}">Reset Password</a></p>
                <p>If you did not request a password reset, please ignore this email.</p>
                <div class="footer">
                <p>Thank you,<br>Academly Team</p>
                </div>
            </div>
            </body>
            </html>
            """
        )
        return True  # Email sent successfully
    except ClientError as e:
        # Handle client errors specifically
        print(f"Client error sending reset token to {email}: {e} (Error code: {e.error_code})")
        return False
    except SpamAssassinError as e:
        # Handle SpamAssassin errors specifically
        print(f"SpamAssassin error sending reset token to {email}: {e}")
        return False
    except Exception as e:
        # Handle any other exceptions
        print(f"Unexpected error sending reset token to {email}: {e}")
        return False


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