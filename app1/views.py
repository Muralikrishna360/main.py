from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
import random
import http.client
from django.conf import settings

def send_otp(mobile, otp):
    conn = http.client.HTTPSConnection("api.msg91.com")
    authkey = settings.authkey
    headers = {'content-type': "application/json"}
    url ="http://control.msg91.com/api/sendotp.php?otp="+otp+"&sender=ABC&message="+'your otp is'+otp+'&mobile='+mobile+'&authkey='+authkey+'&country=91'

    conn.request("GET", url, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return None


def otp(request):
    mobile =  request.session['mobile']
    context = {'mobile':mobile}

    return render(request, 'otp.html', context)


# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['mobile']

        check_user = User.objects.filter(email=email).first()
        check_profile = Profile.objects.filter(mobile =mobile).first()

        if check_user or check_profile:
            context = {'message': 'user already existed', 'class': 'danger'}
            return render(request, 'register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.save()

        otp = str(random.randint(1000, 9999))

        profile = Profile(user=user, mobile=mobile, otp=otp)
        profile.save()
        send_otp(mobile, otp)
        request.session['mobile'] = mobile



        return redirect('otp')
    else:
         return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'home.html', {'name': username})
        else:
            return render(request, 'register.html')

    else:

        return render(request, 'login.html')