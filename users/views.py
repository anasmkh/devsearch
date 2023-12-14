from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from .forms import customUserForm, updateProfileForm, skillForm
from django.shortcuts import render, redirect
from .models import Profile, Skill


# Create your views here.

def loginUser(request):
    page = 'login'
    #
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request,'username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request,'username of password is not correct')

    return render(request,'users/login_register.html')
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.info(request, 'User was logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = customUserForm()
    if request.method == 'POST':
        form = customUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #### مشان اذا كان في حدا كتب نفس الاسم بغير احرف كبيرة او صغيرة مثلا
            user.username=user.username.lower()
            user.save()
            messages.success(request,'User account was created!')
            login(request,user)
            return redirect('update_profile')
        else:
            messages.error(request,'An Error Occurred During Registration')
    context = {'page': page,'form':form}
    return render(request,'users/login_register.html',context)


def profiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')


    skills = Skill.objects.filter(name__icontains=search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query)|
        Q(headline__icontains=search_query)|
        Q(skill__in=skills)
    )

    page = request.GET.get('page')
    result = 1
    paginator = Paginator(profiles, result)
    print(paginator)
    try:
        profiles = Paginator.page(paginator, page)
    except PageNotAnInteger:
        page = 1
        profiles = Paginator.page(paginator, page)
    except EmptyPage:
        page = Paginator.num_pages
        profiles = Paginator.page(paginator, page)

    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1
    rightIndex = (int(page) + 2)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    customRange = range(leftIndex, rightIndex)



    context = {'profiles': profiles,'search_query':search_query,'paginator': paginator,'customRange':customRange}

    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description__exact='')
    otherskills = profile.skill_set.filter(description='')
    context = {
        'profile': profile,
        'topskills': topskills,
        'otherskills': otherskills
    }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context={'profile': profile,'skills':skills,'projects':projects}
    return render(request, 'users/account.html',context)


def updateProfile(request):
    profile = request.user.profile
    form = updateProfileForm(instance=profile)
    if request.method == 'POST':
        form = updateProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context={'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form =skillForm()
    if request.method =='POST':
        form = skillForm(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'This Skill Created Successfully!')
            return redirect('account')
    context={'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form =skillForm(instance=skill)
    if request.method =='POST':
        form = skillForm(request.POST,request.FILES,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'This Skill Updated Successfully!')
            return redirect('account')
    context={'form':form}
    return render(request,'users/skill_form.html',context)


@login_required(login_url='login')
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method =='POST':
        skill.delete()
        messages.success(request,'This Skill Deleted Successfully!')
        return redirect('account')
    context = {'skill':skill}
    return render(request, 'users/delete-form.html', context)