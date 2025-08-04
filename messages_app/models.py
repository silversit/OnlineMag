from django.db import models
from django.conf import settings
# Create your models here.
class Message(models.Model):
    REASON_CHOICES = [
        ('promotion','Promotion'),
        ('product','Product'),
        ('other','Other'),

    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='received_messages')
    subject=models.CharField(max_length=255)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    reasons=models.ManyToManyField('MessageReason')
    status=models.CharField(max_length=20,choices=[("new", "New"), ("answered", "Answered"), ("updated", "Updated")],default="new")
    answered = models.BooleanField(default=False)
    updated = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} - {self.subject}"


class MessageReason(models.Model):
    code = models.CharField(max_length=20,unique=True)
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class MessageReply(models.Model):
    message=models.ForeignKey('Message',on_delete=models.CASCADE,related_name='replies')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.sender.username} at {self.sent_at}"
