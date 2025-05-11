import smtplib

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

    smtp = smtplib.SMTP('smtp.yandex.ru', 587, timeout=10)
    try:
        smtp.starttls()
        smtp.login(login, password)
        smtp.sendmail(msg['From'], recipients_emails, msg.as_string())
    except Exception as ex:
        print(ex)
    finally:
        smtp.quit()