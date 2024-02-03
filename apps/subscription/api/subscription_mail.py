import threading
from solo_core import settings
from solo_core.helpers.mail_fuction import SendEmails

def notify_me_subscription_mail_send(request, instance):
    try:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", settings.EMAIL_HOST_USER, instance.subscriber_email)
        # admin_email = settings.EMAIL_HOST_USER
        subject = "🎉 Welcome to the Club! "
        context = {
            
            'subscriber_email':instance.subscriber_email,
            'domain':settings.EMAIL_DOMAIN,
            'protocol': 'http',
            'email':settings.EMAIL_HOST_USER,
        }

        # import pdb;pdb.set_trace()
        # user_mail = instance.subscriber_email
        # print("ddddddddddddddddddusermail",user_mail)
        send_email = SendEmails()
        mail_sending=threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, 'admin/email/subscription/subscription-sucess.html',settings.EMAIL_HOST_USER, instance.subscriber_email))
        mail_sending.start()

    except Exception as es:
        print("eeeeeeeeeeeee",es)
        pass