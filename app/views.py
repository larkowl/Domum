from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import AnnouncementForm, SignUpForm
from django.utils import timezone
from django.views import generic
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.db.models import Q
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, authenticate
from .search_module import *
from .prediction_module import *
from .announcement_module import *
from django.utils.decorators import method_decorator
from liqpay.liqpay import LiqPay
from django.views.decorators.csrf import csrf_exempt
from django.views import View

def land(request):
    priorites = [0, 8, 5, 3, 7, 2, 6, 4, 1]
    cnt = 0
    best = []
    fake_appartment = Announcement.objects.get(pk=31)
    init_set = Announcement.objects.filter(real_type=2)
    for j in range(3):
        for i in range(cnt, len(priorites)):
            candidate = init_set.filter(district=priorites[i]).order_by('-date')
            if len(candidate) >= 3:
                best.append(candidate[:3])
                cnt = i + 1
                break
    best.sort(key=lambda x: -len(x))
    best_dict = dict()
    best_dict['fake'] = fake_appartment
    best_dict['len'] = [i for i in range(len(best))]
    for i in range(len(best)):
        best_dict['l' + str(i)] = best[i]
    return render(request, 'app/land.html', best_dict)


def post_list(request, pk=-1):
    predict(STANDART_STR)
    if not request.POST:
        if pk == -1:
            return render(request, 'app/search.html', {'announcements': Announcement.objects
                      .filter(Q(real_type=1)).order_by('-date'), 'sort': '-date', 'options': ' '.join(STANDART_STR)})
        params = deepcopy(LONG_TERM_RENT_STR)
        if pk < 9:
            params[-15 + District.objects.get(pk=pk).pseudo_id] = '1'
            data = list(Announcement.objects.filter(Q(real_type=2) & Q(district=pk)))
            data.sort(key=sort_by_rate)
            return render(request, 'app/search.html', {'announcements': data,
                                                   'sort': 'rate', 'options': ' '.join(params)})
        data = list(Announcement.objects.filter(Q(real_type=2)))
        data.sort(key=sort_by_rate)
        return render(request, 'app/search.html', {'announcements': data,
                                                   'sort': 'rate', 'options': ' '.join(params)})
    try:
        sort_par, ids, pars = request.POST['sort_par'].split(':')
        ids = ids.split()
        pars = pars.split()
        ids = [int(i) for i in ids]
        data = []
        if len(ids) > 0:
            query = Q(id=ids[0])
            for i in range(1, len(ids)):
                query.add(Q(id=ids[i]), Q.OR)
            data = Announcement.objects.filter(query)
            if sort_par == 'rate':
                data = list(data)
                data.sort(key=sort_by_rate)
            else:
                data = data.order_by(sort_par)
        return render(request, 'app/search.html', {'announcements': data, 'sort': sort_par,
                                                  'options': ' '.join(pars)})
    except:
        result, pars = search(request.POST)
        sort_par = request.POST['sort_par']
        if sort_par == 'rate':
            result = list(result)
            result.sort(key=sort_by_rate)
        else:
            result = result.order_by(sort_par)
        return render(request, 'app/search.html', {'announcements': result, 'sort': sort_par,
                                                   'options':  ' '.join(pars)})


def check_value(str):
    if str is None:
        return ''
    return str


def check_str(str):
    if str == '':
        return None
    return str


def announcement_view(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    can_comment = True
    deal = None
    if request.user.is_authenticated:
        deal = Deal.objects.filter(Q(buyer=request.user)&Q(announcement=announcement)).first()
        if deal is None or Feedback.objects.filter(deal=deal).first():
            can_comment = False
    else:
        can_comment = False
    if request.POST and can_comment:
        comment = Feedback()
        comment.rate = float(request.POST['comment_rate_mine'])
        comment.text = request.POST['comment_text']
        comment.deal = deal
        comment.date = timezone.now()
        comment.save()
    can_comment = True
    if request.user.is_authenticated:
        deal = Deal.objects.filter(Q(buyer=request.user) & Q(announcement=announcement)).first()
        if deal is None or Feedback.objects.filter(deal=deal).first():
            can_comment = False
    else:
        can_comment = False
    feedbacks = announcement.find_feedbacks().order_by('-date')
    av_rate = announcement.form_rate(True, True, feedbacks)
    return render(request, 'app/announcement_view.html', {'announcement': announcement, 'feedbacks': feedbacks,
                                                          'av_rate': av_rate, 'can_comment': can_comment})


class AnnouncementDetailView(generic.DetailView):
    model = Announcement
    context_object_name = 'announcement'
    template_name = 'app/announcement_view.html'


class AnnouncementsListView(generic.ListView):
    model = Announcement
    context_object_name = 'announcements'
    template_name = 'app/search.html'
    paginate_by = 3


def profile_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    try:
        person = Person.objects.get(user=user)
    except:
        person = None
    announcements = Announcement.objects.filter(owner=user).order_by('-date')
    feedbacks = Feedback.objects.filter(deal__announcement__owner=user)
    deals = list(Deal.objects.filter(announcement__owner=user))
    limit = len(deals)
    anti_deals = list(Deal.objects.filter(buyer=user))
    deals += anti_deals
    if len(feedbacks) > 0:
        rate = sum([i.rate for i in feedbacks]) / len(feedbacks)
        rate = round(rate, 1)
        if int(rate) == rate:
            rate = int(rate)
    else:
        rate = '—'
    return render(request, 'app/personal_area.html', {'person': person, 'person_user': user,
                                                      'announcements': announcements, 'rate': rate,
                                                      'feedbacks': len(feedbacks), 'deals': deals, 'limit': limit})


@login_required
def profile_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        return redirect('profile', pk=pk)
    info = dict()
    info['username'] = check_value(user.username)
    info['first_name'] = check_value(user.first_name)
    info['last_name'] = check_value(user.last_name)
    person = None
    try:
        person = Person.objects.get(user=user)
        info['phone'] = check_value(person.phone)
    except:
        info['phone'] = ''
    if request.method == "POST":
        if person is None:
            person = Person()
            person.user = user
        user.username = check_str(request.POST['username'])
        user.first_name = check_str(request.POST['first_name'])
        user.last_name = check_str(request.POST['last_name'])
        person.phone = check_str(request.POST['phone'])
        user.save()
        person.save()
        return redirect('profile', pk=pk)
    form = SignUpForm()
    return render(request, 'app/profile_edit.html', {'form': form, 'info': info})


@login_required
def new_announcement(request):
    if request.method == 'POST':
        data, options = announcement_form(request.POST)
        announcement = Announcement()
        fill_announcement(announcement, data, request)
        announcement.save()
        return redirect('announcement_view', pk=announcement.pk)
    return render(request, 'app/announcement_edit.html', {'edit': False,
                                                          'options': ' '.join(ADD_STR)})


@login_required
def announcement_edit(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if announcement.owner != request.user:
        return redirect('announcement_view', pk=announcement.pk)
    if request.method == "POST":
        data, options = announcement_form(request.POST)
        fill_announcement(announcement, data, request)
        announcement.save()
        return redirect('announcement_view', pk=announcement.pk)
    data = dict()
    data['district'] = announcement.district.pseudo_id
    data['type'] = announcement.real_type.pk
    data['term'], data['goal'] = define_real_goal_term(data['type'])
    data['comment'] = announcement.comment
    data['repair'] = announcement.repairs
    data['space'] = announcement.area
    data['metro'] = announcement.distance_to_metro
    data['beds'] = announcement.beds
    data['floor'] = announcement.floor
    data['furniture'] = announcement.furniture
    data['garage'] = announcement.garage
    data['street_type'] = announcement.street_type.pk
    data['street'] = announcement.street
    data['home_number'] = announcement.home_number
    data['rooms'] = announcement.rooms_number
    data['price'] = announcement.price
    data['metro_id'] = str(announcement.metro_id)
    data['photo1'] = announcement.photo1
    data['photo2'] = announcement.photo2
    data['photo3'] = announcement.photo3
    data['photo4'] = announcement.photo4
    data['photo5'] = announcement.photo5
    data['photo6'] = announcement.photo6
    data['photo7'] = announcement.photo7
    data['photo8'] = announcement.photo8
    return render(request, 'app/announcement_edit.html', {'edit': True,
                                                          'options': ' '.join(form_announcement_str(data)),
                                                          'data': data})


@login_required
def change_password(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        return redirect('profile', pk=pk)
    if request.method == 'POST':
        psw = None
        if user.has_usable_password():
            psw = request.POST['old']
        n_first = request.POST['new']
        n_second = request.POST['repeat']
        if (psw is None or check_password(psw, user.password)) and n_first == n_second:
            user.set_password(n_first)
            user.save()
            return redirect('profile_edit', pk=user.pk)
    return render(request, 'app/change_password.html', {'passworded': user.has_usable_password()})


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
        people = list(User.objects.filter(username=request.POST['username']))
        second_was = False
        if len(people) > 0:
            second_was = True
        if form.is_valid() and not was and not second_was:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            person = Person()
            person.user = user
            if request.POST['phone']:
                person.phone = '+38' + request.POST['phone']
            person.ava = request.FILES['ava']
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
            return HttpResponse('На вказану електронну пошту надіслано активаційний лист')
        elif was:
            return render(request, 'app/register.html', {'form': form, 'email_occupied': True,
                                                         'first_name': request.POST['first_name'],
                                                         'last_name': request.POST['last_name'],
                                                         'phone': request.POST['phone'],
                                                         'email': request.POST['email'],
                                                         'username': request.POST['username'],
                                                         'password1': request.POST['password1']})
        elif second_was:
            return render(request, 'app/register.html', {'form': form, 'login_occupied': True,
                                                         'first_name': request.POST['first_name'],
                                                         'last_name': request.POST['last_name'],
                                                         'phone': request.POST['phone'],
                                                         'email': request.POST['email'],
                                                         'username': request.POST['username'],
                                                         'password1': request.POST['password1']})
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
        login(request, user, backend='django.contrib.auth')
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')


def payment(request, sum):
    liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
    html = liqpay.cnb_form({
        'action': 'p2p',
        'amount': '1000',
        'currency': 'UAH',
        'description': 'Заказ недвижимости через DOMUM',
        'order_id': OrderId.objects.first().next(),
        'version': '3',
        'sandbox': 0,
        'server_url': 'http://127.0.0.1:8000/pay-callback/',
    })
    return HttpResponse(html)


def sort_by_rate(announcement):
    x = -announcement.form_rate(False, False)
    if x == 1:
        return -7
    return x


def fill_photos(announcement, data, start, finish, need_none=False):
    for i in range(start, finish):
        now = None if need_none else data.get('add_photo{}'.format(i))
        if i == 1:
            announcement.photo1 = now
        elif i == 2:
            announcement.photo2 = now
        elif i == 3:
            announcement.photo3 = now
        elif i == 4:
            announcement.photo4 = now
        elif i == 5:
            announcement.photo5 = now
        elif i == 6:
            announcement.photo6 = now
        elif i == 7:
            announcement.photo7 = now
        elif i == 8:
            announcement.photo8 = now


def fill_announcement(announcement, data, request):
    announcement.district = District.objects.get(pseudo_id=data['district'])
    announcement.real_type = RealType.objects.get(pk=data['type'])
    announcement.date = timezone.now()
    announcement.owner = request.user
    announcement.comment = data['comment']
    announcement.repairs = data['repair']
    announcement.area = data['space']
    announcement.distance_to_metro = data['metro']
    announcement.beds = data['beds']
    announcement.floor = data['floor']
    announcement.furniture = data['furniture']
    announcement.garage = data['garage']
    announcement.street_type = StreetType(pk=data['street_type'])
    announcement.street = data['street']
    announcement.home_number = data['home_number']
    announcement.rooms_number = data['rooms']
    announcement.price = data['price']
    announcement.station = MetroStation.objects.get(name=data['metro_name'])
    announcement.metro_id = int(data['metro_id'])
    photos_count = int(request.POST['photos_count'])
    fill_photos(announcement, request.FILES, 1, photos_count)
    fill_photos(announcement, request.FILES, photos_count, 9, True)

from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse


class PayView(TemplateView):
    template_name = 'app/pay.html'

    def get(self, request, *args, **kwargs):
        liqpay = LiqPay(settings.LIQPAY_PUBLIC_KEY, settings.LIQPAY_PRIVATE_KEY)
        params = {
            'action': 'pay',
            'amount': '1',
            'currency': 'USD',
            'description': 'Payment for clothes',
            'order_id': 'order_id_12',
            'version': '3',
            'sandbox': 0, # sandbox mode, set to 1 to enable it
            'server_url': 'http://127.0.0.1:8000/pay-callback/', # url to callback view
        }
        signature = liqpay.cnb_signature(params)
        data = liqpay.cnb_data(params)
        return render(request, self.template_name, {'signature': signature, 'data': data})


def check(request):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return HttpResponse('kek')
