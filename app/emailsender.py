import aiosmtplib

from email.mime.text import MIMEText
from email.header import Header

from config import EMAIL_LOGIN, EMAIL_PASSWORD

async def async_send_mail(recipients_emails: list, header: str, msg: str) -> None:
    login = EMAIL_LOGIN
    password = EMAIL_PASSWORD

    msg = MIMEText(f'{msg}', 'plain', 'utf-8')
    msg['Subject'] = Header(header, 'utf-8')
    msg['From'] = login
    msg['To'] = ', '.join(recipients_emails)

    smtp = aiosmtplib.SMTP('smtp.yandex.ru', 587, timeout=10)
    await smtp.connect()
    try:
        await smtp.starttls()
        await smtp.login(login, password)
        await smtp.sendmail(msg['From'], recipients_emails, msg.as_string())
    except Exception as ex:
        print(ex)
    finally:
        await smtp.quit()