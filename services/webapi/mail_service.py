from config.constants import PROXY_MAIL, MAIL_PASSWORD, SUCCESS
from services.action_result import ActionResult
import gmail


class MailService:
    def __init__(self, mail_account=PROXY_MAIL, mail_password=MAIL_PASSWORD):
        self.__api = gmail.GMail(mail_account, mail_password)

    def send_mail(self, receiver, subject, content):
        new_message = gmail.Message(subject, to=receiver, text=content)
        try:
            status = self.__api.send(new_message)
            if status is None:
                return ActionResult("Email was sent successfully!", SUCCESS)
        except Exception as e:
            #TODO:handle situation with problem
            print(e)
