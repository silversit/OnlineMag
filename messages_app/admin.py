from django.contrib import admin
from .models import  Message, MessageReply
# Register your models here.

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'sent_at')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('subject', 'content')

@admin.register(MessageReply)
class MessageReplyAdmin(admin.ModelAdmin):
    list_display = ('message', 'sender', 'sent_at')
    list_filter = ('sender', 'sent_at')
    search_fields = ('content',)