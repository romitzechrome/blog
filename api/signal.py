from .models import *
from django.db.models.signals import post_save,pre_save,pre_delete
from  django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail,EmailMultiAlternatives


@receiver(post_save,sender=BlogPOST)
def save_post(sender,instance,created,**kwargs):
    data = instance
    contex={
        "Title":data.title,
        "Body":data.body,
        "Author":data.auther.username
    }
    html_page = render_to_string("post.html", contex)
    text_contant = strip_tags(html_page)
    fail_silently = True
    from_email = 'romit.zechrom@gmail.com'
    to = data.auther.email
    msg = EmailMultiAlternatives("Post creation", text_contant, from_email, [to])
    msg.attach_alternative(html_page, "text/html")
    try:
        msg.send()
    except Exception as ex:
        print("not success",ex)
    

















