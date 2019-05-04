from django.shortcuts import render, get_object_or_404, redirect
from .models import Announcement, Person
from .forms import AnnouncementForm, SignUpForm
from django.utils import timezone
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

'''
def post_list(request):
    return render(request, 'app/post_list.html', {'announcements': Announcement.objects.all()})
'''


def announcement_view(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'app/announcement_view.html', {'announcement': announcement})


class AnnouncementDetailView(generic.DetailView):
    model = Announcement
    context_object_name = 'announcement'
    template_name = 'app/announcement_view.html'


class AnnouncementsListView(generic.ListView):
    model = Announcement
    context_object_name = 'announcements'
    template_name = 'app/post_list.html'
    paginate_by = 3


@login_required
def new_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.owner = request.user
            announcement.date = timezone.now()
            announcement.save()
            return redirect('announcement_view', pk=announcement.pk)
    form = AnnouncementForm()
    return render(request, 'app/announcement_edit.html', {'form': form, 'edit': False})


@login_required
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if announcement.owner != request.user:
        return redirect('announcement_view', pk=announcement.pk)
    if request.method == "POST":
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.owner = request.user
            announcement.date = timezone.now()
            announcement.save()
            return redirect('announcement_view', pk=announcement.pk)
    form = AnnouncementForm(instance=announcement)
    return render(request, 'app/announcement_edit.html', {'form': form, 'edit': True})


def signup(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        people = list(User.objects.filter(email=request.POST['email']))
        was = False
        for human in people:
            if human.is_active:
                was = True
        if form.is_valid() and not was:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            person = Person()
            person.user = user
            person.phone = request.POST['phone']
            person.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('app/activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        elif was:
            return HttpResponse('There is an account on this email address')
    else:
        form = SignUpForm()
    return render(request, 'app/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is None:
        return HttpResponse('Activation link is invalid!')
    people = list(User.objects.filter(email=user.email))
    was = False
    for human in people:
        if human.is_active:
            was = True
    if was:
        user.delete()
        return HttpResponse('There is an account registrated on this email')
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('post_list')
    else:
        return HttpResponse('Activation link is invalid!')
