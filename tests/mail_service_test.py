import sys
sys.path.append("..")
from services.webapi.mail_service import MailService

ms = MailService()
ms.send_email("564.2015@fink.rs", "test subject", "test message")
ms.send_email("564.2015@fink.rs", "test tema", "test poruka")
#https://pypi.org/project/gmail/
