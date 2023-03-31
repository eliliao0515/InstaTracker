from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
# from .methods import get_follower_names, get_following_names
from .methods import loader

# Create your views here.
@csrf_protect
def login(request):
    # make sure the user is logged out
    logout(request)

    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        try:
            # Check input
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request)
                request.session['username'] = username
                request.session['password'] = password
            else:
                return render(request, "error.html", {'e':'User not found!'})
            
            return redirect('/dashboard/home/')
        
        except Exception as e:
            return render(request, 'error.html', {'e':e})

def home(request):
    username = request.session.get('username', None)
    password = request.session.get('password', None)

    if not username or not password:
        return render(request, 'error.html', {'e':'Invalid login'})
    
    ins = loader(username, password)

    if not ins:
        return redirect('/dashboard/login/')
    
    name = ins.get_username()
    picture_url = ins.get_image()

    return render(request, "home.html", {'followers': len(ins.followers), 
                                        'followings': len(ins.followings), 
                                        'User_name': name,
                                        'profile_image': picture_url,
                                        'new_followers': len(ins.get_diff()['new_follower']),
                                        'new_followings': len(ins.get_diff()['new_following']),
                                        'new_followers_list':ins.get_diff()['new_follower'],
                                        'lost_followers_list':ins.get_diff()['lost_follower'],
                                        'new_followings_list':ins.get_diff()['new_following'],
                                        'lost_followings_list':ins.get_diff()['lost_following']})