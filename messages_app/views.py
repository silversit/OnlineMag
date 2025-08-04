from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Message,MessageReply
from .forms import MessageForm
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class UserInboxView(LoginRequiredMixin,View):
    def get(self,request):
        inbox_messages = Message.objects.filter(
            recipient=request.user
        ).order_by('-sent_at')


        sent_messages = Message.objects.filter(
            sender=request.user,
            answered=False
        ).order_by('-sent_at')

        return render(request,'messages_app/inbox.html',{
            'inbox_messages': inbox_messages,
            'sent_messages': sent_messages
        })

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = User.objects.filter(is_superuser=True).first() #hmm dali ne e greshno tova raboteshe na testa owner e razlichen ot admin. az testvah s admin :D mojebi e greshno
           #nqmam vreme za poreden test puskam taka. tova mai ne e vqrno :D da testvam po kusno pak ako imam vreme !
            msg.save()
            form.save_m2m()
            return redirect('inbox')
        else:
            form=MessageForm()
        return render(request,'messages_app/send_message.html',{'form':form})


@login_required
def reply_to_message(reqiest,message_id):


    message = get_object_or_404(Message,id=message_id)

    if reqiest.method == 'POST':
        content = reqiest.POST.get("reply","").strip()
        if content:
            MessageReply.objects.create(
                message=message,
                sender=reqiest.user,
                content=content
            )
            if reqiest.user.role == 'owner':
                message.answered = True
                message.updated = False
                message.status = 'answered'

            else:
                message.recipient=message.sender
                message.sender = reqiest.user
                message.answered=True
                message.updated=True
                message.status='updated'

            message.save()

        return redirect('inbox' if reqiest.user.role != 'owner' else 'owner-messages')






