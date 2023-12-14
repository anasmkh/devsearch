from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .form import ProjectForm

from projects.models import Project, Tag


# Create your views here.

def projects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )

    page = request.GET.get('page')
    result = 3
    paginator = Paginator(projects, result)
    print(paginator)
    try:
        projects = Paginator.page(paginator, page)
    except PageNotAnInteger:
        page = 1
        projects = Paginator.page(paginator, page)
    except EmptyPage:
        page = Paginator.num_pages
        projects = Paginator.page(paginator, page)

    leftIndex = (int(page) - 1)
    if leftIndex < 1 :
        leftIndex = 1
    rightIndex = (int(page) + 2)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    customRange = range(leftIndex,rightIndex)
    context = {'projects': projects, 'search_query': search_query, 'paginator': paginator, 'customRange':customRange}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectobj = Project.objects.get(id=pk)
    tags = projectobj.tags.all()
    context = {'project': projectobj, 'tags': tags}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def creatproject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def updateproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def deleteproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {'object': project}
    return render(request, 'projects/delete-form.html', context)
