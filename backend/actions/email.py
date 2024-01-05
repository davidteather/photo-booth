import smtplib
import logging
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

class SMTPServer:
    def __init__(self, smtp_user, smtp_pass, smtp_server, port):
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.smtp_server = smtp_server
        self.port = port
        self.context = ssl._create_unverified_context() # TODO: I think this is bc flask is using a self-signed cert

    def send_email(self, from_email, to_emails, subject, body, images_data: list[bytes] = None, photos_ext = "jpeg"):
        # Create a multipart email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject

        # Attach the text part
        msg.attach(MIMEText(body, 'plain'))

        # Attach the images, if provided
        if images_data is not None:
            for i, image_data in enumerate(images_data):
                image = MIMEImage(image_data, name=f'photo_{i}.{photos_ext}')
                msg.attach(image)

        try:
            # Initialize and connect to the server
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.ehlo()
            server.starttls(context=self.context)
            server.ehlo()
            server.login(self.smtp_user, self.smtp_pass)

            # Send email
            server.sendmail(from_email, to_emails, msg.as_string())
        except smtplib.SMTPServerDisconnected:
            logging.critical("Failed to connect to the server. Check your SMTP settings.")
        except smtplib.SMTPAuthenticationError:
            logging.critical("SMTP authentication failed. Check your username and password.")
        except Exception as e:
            logging.critical(f"Failed to send email: {e}")
            raise e
        finally:
            try:
                server.quit()
            except Exception as e:
                logging.critical(f"Failed to close the SMTP connection: {e}")
