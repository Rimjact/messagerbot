import aiosmtplib

from os import getenv

from email.mime.text import MIMEText
from email.header import Header


async def async_send_mail(recipients_emails: list, header: str, msg: str) -> None:
    smtp_server = getenv("EMAILSMTP")
    login = getenv("EMAILLOGIN")
    password = getenv("EMAILPASSWORD")

    msg = MIMEText(f'{msg}', 'plain', 'utf-8')
    msg['Subject'] = Header(header, 'utf-8')
    msg['From'] = login
    msg['To'] = ', '.join(recipients_emails)

    smtp = aiosmtplib.SMTP(smtp_server, 587, timeout=10)
    await smtp.connect()
    try:
        await smtp.starttls()
        await smtp.login(login, password)
        await smtp.sendmail(msg['From'], recipients_emails, msg.as_string())
    except Exception as ex:
        print(f"ERROR: Somthing goes wrong:\n{ex}")
    finally:
        await smtp.quit()