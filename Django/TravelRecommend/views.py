from django.core.files import File
from django.db.models.fields.files import FieldFile
from django.forms import ImageField
from django.http import HttpResponse
from django.shortcuts import render, redirect
#django get_object_or_404
from TravelRecommend import UserCF
import os
import csv
# Create your views here.
from TravelRecommend import models


def index(request):
    return render(request, 'index.html')


def user_index(request, id):
    routes = UserCF.UserBasedCF.my_route(id)
    print("ID:",id)
    return render(request,'index.html', {'routes': routes, 'user_id': id})


def city(request, city_name):
    print("CITY:", city_name)
    try:
        city_obj = models.CityInfo.objects.get(spot_name=city_name)
        img = models.IMG.objects.filter(city__spot_name=city_name)
    except:
        return render(request, 'undefined.html')
    else:
        return render(request, 'city.html', {'city_obj': city_obj, 'img': img})


def recommend(request, id):
    cities = UserCF.UserBasedCF.user_recommend(id)
    print("recommendID:", id)
    return render(request,'recommend.html', {'cities': cities})


def login(request):
    if request.method == "POST":
        usr = request.POST.get('usr', None)
        pwd = request.POST.get('pwd', None)
        if usr and pwd:  # 确保用户名和密码都不为空
            usr = usr.strip()
            try:
                obj = models.UserInfo.objects.get(user_id=usr)
            except Exception as e:
                return render(request, 'login.html', {'error': "用户id不存在"})
            if pwd != obj.pwd:
                return render(request, 'login.html', {'error': "用户id或密码不正确"})
            return redirect('/'+str(usr)+'/')
        else:
            return render(request, 'login.html', {'error': "请填写用户id"})
    else:
        return render(request, 'login.html')

