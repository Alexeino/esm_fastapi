import aiosmtplib
import smtplib


async def send_email_async(subject: str, to_email: str, body: str):
    from_email = "esm@fastapi.xyz"
    message = f"Subject: {subject}\nFrom: {from_email}\nTo: {to_email}\n\n{body}"

    smtp = aiosmtplib.SMTP(hostname="localhost", port=1025)

    try:
        await smtp.connect()
        await smtp.sendmail(from_email, to_email, message)

    finally:
        await smtp.quit()


def send_email_sync(subject: str, to_email: str, body: str):
    from_email = "esm@fastapi.xyz"
    message = f"Subject: {subject}\nFrom: {from_email}\nTo: {to_email}\n\n{body}"

    with smtplib.SMTP("localhost", 1025) as smtp:
        smtp.sendmail(from_email, to_email, message)
