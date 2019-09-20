from config.constants import PROXY_MAIL, MAIL_PASSWORD
import gmail


class MailService:
    def __init__(self, mail_account=PROXY_MAIL, mail_password=MAIL_PASSWORD):
        self.__api = gmail.GMail(mail_account, mail_password)

        self.__receiver = None
        self.__content = None
        self.__subject = None

    # setters

    def set_receiver_with_input(self, receiver):
        print("Email address: ")
        receiver = input()
        self.set_receiver(receiver)

    def set_receiver(self, receiver):
        self.__receiver = self.convert_email_str_to_address(receiver)

    def set_subject(self, subject):
        self.__subject = subject

    def set_content(self, content):
        self.__content = content

    # getters
    def get_receiver(self):
        return self.__receiver

    def get_subject(self):
        return self.__subject

    def get_content(self):
        return self.__content

    def send_email_with_default_params(self):
        params = dict(
            zip(["receiver", "subject", "content"], [self.get_receiver(), self.get_subject(), self.get_content()]))
        status = self.send_mail(**params)
        return status

    def send_mail(self, receiver, subject, content):
        new_message = gmail.Message(subject, to=receiver, text=content)
        try:
            return self.__api.send(new_message)
        except Exception as e:
            print(e)

    # helper
    # email_str will have _et_ for @ symbol
    def convert_email_str_to_address(self, email_str):
        print(email_str)
        email_str = email_str.replace("_et_", "@")
        username, host_name = email_str.split("@")
        print("".join(username) + "@" + host_name)
        return "".join(username) + "@" + host_name
