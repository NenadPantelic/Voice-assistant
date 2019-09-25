from config.constants import PROXY_MAIL, MAIL_PASSWORD, SUCCESS, FAIL
from services.action_result import ActionResult
import gmail


class MailService:
    def __init__(self, mail_account=PROXY_MAIL, mail_password=MAIL_PASSWORD):
        self._api = gmail.GMail(mail_account, mail_password)

    def send_mail(self, recipient, subject, content):
        """
        Send an email to recipient. Returns empty action result with status.
        :param recipient (str): recipient email address
        :param subject (str): subject of an email
        :param content (str): content of an email
        :return:
        """
        #TODO:add some regex validator for [to] email address
        new_message = gmail.Message(subject, to=recipient, text=content)
        status = self._api.send(new_message)
        status_code = SUCCESS if status is None else FAIL
        return ActionResult("", status=status_code)
        #mostly, errors are caused by smtp
