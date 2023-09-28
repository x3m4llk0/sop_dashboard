from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import *
from .forms import UserLoginForm, UserRegistrationForm
from django.contrib import auth, messages
from django.urls import reverse

# Create your views here.

def index(request, q_id = None):
    all_bonus = Bonus.objects.all()[::-1]
    all_mistakes = Mistake.objects.all()[::-1]
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    else:
        sop = request.user.user_id.sop
        all_users = TgUser.objects.filter(sop=sop)

        # Для бонусов
        bonus_list = []
        for user in all_users:
            if q_id != None:
                bonus_list.append({'short': user.last_name[:1] + user.first_name[:1],
                                   'tooltip': f'{user.first_name}. {user.last_name[:1]}',
                                   'count': Bonus.objects.filter(employee=user.user_id, quarter=q_id).count()})
            else:
                bonus_list.append({'short': user.last_name[:1] + user.first_name[:1],
                                   'tooltip': f'{user.first_name}. {user.last_name[:1]}',
                                   'count': Bonus.objects.filter(employee=user.user_id).count()})
        bonus_list = sorted(bonus_list, key=lambda item: item['count'], reverse=True)

        # Для ошибок
        mistake_list = []
        for user in all_users:
            if q_id != None:
                mistake_list.append({'short': user.last_name[:1] + user.first_name[:1],
                                     'tooltip': f'{user.first_name}. {user.last_name[:1]}',
                                     'count': Mistake.objects.filter(employee=user.user_id, quarter=q_id).count()})
            else:

                mistake_list.append({'short': user.last_name[:1] + user.first_name[:1],
                                     'tooltip': f'{user.first_name}. {user.last_name[:1]}',
                                     'count': Mistake.objects.filter(employee=user.user_id).count()})
        mistake_list = sorted(mistake_list, key=lambda item: item['count'], reverse=True)

        bonus_mistake_count_list = []
        if q_id != None:
            count_mistakes_list = []
            count_bonus_list = []
            for user in all_users:
                count_mistakes_list.append(Mistake.objects.filter(employee=user.user_id, quarter=q_id).count())
                count_bonus_list.append(Bonus.objects.filter(employee=user.user_id, quarter=q_id).count())
            count_mistakes = max(count_mistakes_list)
            count_bonus = max(count_bonus_list)
            # бонусы
            if count_bonus < 5:
                max_bonus, tab4_bonus, tab3_bonus, tab2_bonus, tab1_bonus = 5, 4, 3, 2, 1

            else:
                max_bonus = (count_bonus // 10 + 1) * 10
                tab4_bonus = round(max_bonus / 1.25)
                tab3_bonus = round(max_bonus // 1.666666)
                tab2_bonus = round(max_bonus // 2.5)
                tab1_bonus = round(max_bonus // 5)
            bonus_mistake_count_list.append(
                {'max_bonus': max_bonus, 'tab4_bonus': tab4_bonus, 'tab3_bonus': tab3_bonus,
                 'tab2_bonus': tab2_bonus, 'tab1_bonus': tab1_bonus})
            # ошибки
            if count_mistakes < 5:
                max_mistake, tab4_mistake, tab3_mistake, tab2_mistake, tab1_mistake = 5, 4, 3, 2, 1
            else:
                max_mistake = (count_mistakes // 10 + 1) * 10
                tab4_mistake = round(max_mistake / 1.25)
                tab3_mistake = round(max_mistake // 1.666666)
                tab2_mistake = round(max_mistake // 2.5)
                tab1_mistake = round(max_mistake // 5)
            bonus_mistake_count_list.append(
                {'max_mistake': max_mistake, 'tab4_mistake': tab4_mistake, 'tab3_mistake': tab3_mistake,
                 'tab2_mistake': tab2_mistake, 'tab1_mistake': tab1_mistake})
        else:
            count_mistakes_list = []
            count_bonus_list = []
            for user in all_users:
                count_mistakes_list.append(Mistake.objects.filter(employee=user.user_id).count())
                count_bonus_list.append(Bonus.objects.filter(employee=user.user_id).count())
            count_mistakes = max(count_mistakes_list)
            count_bonus = max(count_bonus_list)
            # бонусы
            if count_bonus < 5:
                max_bonus, tab4_bonus, tab3_bonus, tab2_bonus, tab1_bonus = 5, 4, 3, 2, 1

            else:
                max_bonus = (count_bonus // 10 + 1) * 10
                tab4_bonus = round(max_bonus / 1.25)
                tab3_bonus = round(max_bonus // 1.666666)
                tab2_bonus = round(max_bonus // 2.5)
                tab1_bonus = round(max_bonus // 5)
            bonus_mistake_count_list.append(
                {'max_bonus': max_bonus, 'tab4_bonus': tab4_bonus, 'tab3_bonus': tab3_bonus,
                 'tab2_bonus': tab2_bonus, 'tab1_bonus': tab1_bonus})
            # ошибки
            if count_mistakes < 5:
                max_mistake, tab4_mistake, tab3_mistake, tab2_mistake, tab1_mistake = 5, 4, 3, 2, 1

            else:
                max_mistake = (count_mistakes // 10 + 1) * 10
                tab4_mistake = round(max_mistake / 1.25)
                tab3_mistake = round(max_mistake // 1.666666)
                tab2_mistake = round(max_mistake // 2.5)
                tab1_mistake = round(max_mistake // 5)
            bonus_mistake_count_list.append(
                {'max_mistake': max_mistake, 'tab4_mistake': tab4_mistake, 'tab3_mistake': tab3_mistake,
                 'tab2_mistake': tab2_mistake, 'tab1_mistake': tab1_mistake})
        # Для слайдера
        slider_list = []
        for user in all_users:
            #находим пользователя в SiteUser и проверяем его на активность. Если не активен, то не записываем его в слайдер
            site_user = SiteUser.objects.filter(user_id=user.user_id).first()
            if not site_user.is_active:
                continue
            else:
                if q_id != None:
                    slider_list.append(
                        {'user_id': user.user_id, 'first_name': user.first_name, 'last_name': user.last_name[:1] + ".",
                         'count_like': Like.objects.filter(employee=user.user_id, quarter=q_id).count(),
                         'photo': user.photo})
                else:
                    slider_list.append(
                        {'user_id': user.user_id, 'first_name': user.first_name, 'last_name': user.last_name[:1] + ".",
                         'count_like': Like.objects.filter(employee=user.user_id).count(), 'photo': user.photo})
        slider_list = sorted(slider_list, key=lambda item: item['last_name'])

        # Для бублика
        if q_id != None:
            donut_dict = {'likes': Like.objects.filter(quarter=q_id).count(),
                          'mistakes': Mistake.objects.filter(quarter=q_id).count(),
                          'bonus': Bonus.objects.filter(quarter=q_id).count()}
        else:
            donut_dict = {'likes': Like.objects.count(), 'mistakes': Mistake.objects.count(),
                          'bonus': Bonus.objects.count()}

        # кварталы
        all_quarter = Quarter.objects.all()

        # сетка бонусов
        bonus_list_map = []
        if q_id != None:
            for item in Bonus.objects.filter(quarter=q_id)[::-1]:
                bonus_list_map.append({'employee': f'{item.employee.first_name} {item.employee.last_name[:1]}.',
                                       'activity': item.activity, 'criterion': item.criterion, 'comment': item.comment,
                                       'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                       'date': item.created_at, 'quarter': item.quarter})
        else:
            for item in Bonus.objects.all()[::-1]:
                bonus_list_map.append({'employee': f'{item.employee.first_name} {item.employee.last_name[:1]}.',
                                       'activity': item.activity, 'criterion': item.criterion, 'comment': item.comment,
                                       'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                       'date': item.created_at, 'quarter': item.quarter})

        # сетка ошибок
        mistake_list_map = []
        if q_id != None:
            for item in Mistake.objects.filter(quarter=q_id)[::-1]:
                mistake_list_map.append({'employee': f'{item.employee.first_name} {item.employee.last_name[:1]}.',
                                         'activity': item.activity, 'criterion': item.criterion,
                                         'comment': item.comment,
                                         'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                         'date': item.created_at, 'quarter': item.quarter})
        else:
            for item in Mistake.objects.all()[::-1]:
                mistake_list_map.append({'employee': f'{item.employee.first_name} {item.employee.last_name[:1]}.',
                                         'activity': item.activity, 'criterion': item.criterion,
                                         'comment': item.comment,
                                         'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                         'date': item.created_at, 'quarter': item.quarter})

        data = {'bonus_list_map': bonus_list_map, 'mistake_list_map': mistake_list_map, 'slider_list': slider_list,
                'donut_dict': donut_dict, 'bonus_list': bonus_list, 'mistake_list': mistake_list, 'q_id': q_id,
                'all_quarter': all_quarter, 'bonus_mistake_count_list': bonus_mistake_count_list}

        return render(request, './index.html', data)



def profile(request, user_id = None, q_id = None):

    if not request.user.is_authenticated or request.user.is_anonymous:
        return HttpResponseRedirect(reverse('login'))
    else:
        sop = request.user.user_id.sop
        all_users = TgUser.objects.filter(sop=sop)
        # Для слайдера
        slider_list = []
        for user in all_users:
            #находим пользователя в SiteUser и проверяем его на активность. Если не активен, то не записываем его в слайдер
            site_user = SiteUser.objects.filter(user_id=user.user_id).first()
            if not site_user.is_active:
                continue
            else:
                if q_id != None:
                    slider_list.append(
                        {'user_id': user.user_id, 'first_name': user.first_name, 'last_name': user.last_name[:1] + ".",
                         'count_like': Like.objects.filter(employee=user.user_id, quarter=q_id).count(),
                         'photo': user.photo})
                else:
                    slider_list.append(
                        {'user_id': user.user_id, 'first_name': user.first_name, 'last_name': user.last_name[:1] + ".",
                         'count_like': Like.objects.filter(employee=user.user_id).count(), 'photo': user.photo})
        slider_list = sorted(slider_list, key=lambda item: item['last_name'])

        # кварталы
        all_quarter = Quarter.objects.all()

        # сетка бонусов
        bonus_list_map = []
        if q_id != None:
            for item in Bonus.objects.filter(quarter=q_id, employee=user_id)[::-1]:
                bonus_list_map.append({'employee': f'{item.employee.first_name} {item.employee.last_name[:1]}.',
                                       'activity': item.activity, 'criterion': item.criterion, 'comment': item.comment,
                                       'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                       'date': item.created_at, 'quarter': item.quarter})
        else:
            for item in Bonus.objects.filter(employee=user_id)[::-1]:
                bonus_list_map.append({'employee': f'{item.employee.first_name} {item.employee.last_name[:1]}.',
                                       'activity': item.activity, 'criterion': item.criterion, 'comment': item.comment,
                                       'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                       'date': item.created_at, 'quarter': item.quarter})

        # сетка ошибок
        mistake_list_map = []
        if q_id != None:
            for item in Mistake.objects.filter(quarter=q_id, employee=user_id)[::-1]:
                mistake_list_map.append({'employee': f'{item.employee.first_name} {item.employee.last_name[:1]}.',
                                         'activity': item.activity, 'criterion': item.criterion,
                                         'comment': item.comment,
                                         'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                         'date': item.created_at, 'quarter': item.quarter})
        else:
            for item in Mistake.objects.filter(employee=user_id)[::-1]:
                mistake_list_map.append({'employee': f'{item.employee.first_name} {item.employee.last_name[:1]}.',
                                         'activity': item.activity, 'criterion': item.criterion,
                                         'comment': item.comment,
                                         'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                         'date': item.created_at, 'quarter': item.quarter})

        if q_id != None:
            all_mistake_count = Mistake.objects.filter(employee=user_id, quarter=q_id).count()
            all_bonus_count = Bonus.objects.filter(employee=user_id, quarter=q_id).count()
        else:
            all_mistake_count = Mistake.objects.filter(employee=user_id).count()
            all_bonus_count = Bonus.objects.filter(employee=user_id).count()

        like_list_map = []
        if q_id != None:
            for item in Like.objects.filter(quarter=q_id, employee=user_id)[::-1]:
                like_list_map.append({'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                      'date': item.created_at})
        else:
            for item in Like.objects.filter(employee=user_id)[::-1]:
                like_list_map.append({'initiator': f'{item.initiator.first_name} {item.initiator.last_name[:1]}.',
                                      'date': item.created_at})

        data = {'selected_user_id': user_id, 'bonus_list_map': bonus_list_map, 'mistake_list_map': mistake_list_map,
                'slider_list': slider_list, 'q_id': q_id, 'all_quarter': all_quarter,
                'all_mistake_count': all_mistake_count, 'all_bonus_count': all_bonus_count,
                'like_list_map': like_list_map}

        return render(request, './profile.html', data)


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, './auth/login.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


def registration(request):
    if request.method == 'POST':
        data_request = request.POST.copy()
        if data_request['role'] == 'ns':
            data_request['access'] = 'agreement'
        else:
            data_request['access'] = 'user'

        form = UserRegistrationForm(data=data_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрированы!')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, './auth/registration.html', context)
