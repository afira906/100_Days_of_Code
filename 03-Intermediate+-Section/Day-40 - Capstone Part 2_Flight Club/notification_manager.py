import os
import smtplib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class NotificationManager:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"  # Default: Gmail
        self.smtp_port = 587  # Default: 587 (TLS)
        self.sender_email = os.environ["SENDER_EMAIL"]
        self.sender_password = os.environ["SENDER_PASSWORD"]
        self.receiver_email = os.environ["RECEIVER_EMAIL"]
        self.connection = smtplib.SMTP(self.smtp_server, self.smtp_port)

    def send_emails(self, email_list, email_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(self.sender_email, self.sender_password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.sender_email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )
            print("Email sent successfully!")
