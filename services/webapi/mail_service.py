from config.constants import PROXY_MAIL, MAIL_PASSWORD, SUCCESS, FAIL, logger
from services.action_result import ActionResult
import gmail


class MailService:
    def __init__(self, mail_account=PROXY_MAIL, mail_password=MAIL_PASSWORD):
        self._api = gmail.GMail(mail_account, mail_password)

    def send_email(self, recipient, subject, content):
        """
        Send an email to recipient. Returns empty action result with status.
        :param recipient: recipient email address (str)
        :param subject: subject of an email (str)
        :param content: content of an email (str)
        :return:
        """
        #TODO:add some regex validator for [to] email address
        logger.debug("Calling send_email with params [subject = {}, recipient = {}, content = {}]".\
                     format(subject, recipient, content))
        new_message = gmail.Message(subject, to=recipient, text=content)
        status = self._api.send(new_message)
        status_code = SUCCESS if status is None else FAIL
        logger.debug("Email sending finished with status = {}".format("success" if status_code == SUCCESS else "fail"))
        return ActionResult("", status=status_code)
        #mostly, errors are caused by smtp
