from config import conf
import smtplib

class Email:

    @classmethod
    def send_email(cls, to, subject, msg):
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(conf['email_user_name'], conf['email_password'])
        formatted_msg = '\r\n'.join([
            'From: %s' % conf['email_user_name'],
            'To: %s' % to,
            'Subject: %s' % subject,
            '',
            msg
        ])
        server.sendmail(
            conf['email_user_name'], to, formatted_msg)
        server.quit()
