from django.urls import path
from . import views
from .views import UserInboxView

urlpatterns=[
    path('inbox/', UserInboxView.as_view(),name='inbox'),
    path('send/',views.send_message,name='send-message'),
    path('reply/<int:message_id>/',views.reply_to_message,name='reply-to-message'),
]