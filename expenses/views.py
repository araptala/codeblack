from django.shortcuts import render, redirect, get_object_or_404
from .models import *
import json
from django.conf import settings
import os
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.contrib.auth.models import User

# Django math methods
from django.db.models import Sum


def forex(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'forex', 'AUDUSD_D1.json')
    # Rest of your code...


# Create your views here.

def index(request):
    page_name = 'Expense Manager'

    events = Event.objects.all()
    expenses = Expense.objects.all()
    tasks = Task.objects.all()

    photos = Photo.objects.all()
    logo = photos[0]

    context = {
        'page_name': page_name,
        'events': events,
        'expenses': expenses,
        'tasks': tasks,
        'logo': logo,
        'photos': photos,
    }

    return render(request, 'index.html', context)


@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    expenses = Expense.objects.filter(event=event)
    tasks = Task.objects.filter(event=event)
    context = {
        'event': event,
        'expenses': expenses,
        'tasks': tasks
    }
    return render(request, 'event_detail.html', context)


@login_required
def create_expense(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        expense = Expense.objects.create(
            event=event, amount=amount, description=description)
        return redirect('event_detail', event_id=event.id)
    return render(request, 'create_expense.html', {'event': event})


@login_required
def create_task(request):
    event = Event.objects.first()  # Select the appropriate event for the task creation
    form = TaskForm(request.POST or None)
    tasks = Task.objects.all()
    new_tasks = Task.objects.order_by('-created_at')

    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.event = event
        print("Task: ", task)
        task.save()
        return redirect('tasks')

    context = {
        'event': event,
        'form': form,
        'tasks': tasks,
        'new_tasks': new_tasks,
    }
    return render(request, 'create_task.html', context)


# Delete
@login_required
def update_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        expense.amount = amount
        expense.description = description
        expense.save()
        return redirect('event_detail', event_id=expense.event.id)
    return render(request, 'update_expense.html', {'expense': expense})


@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, pk=expense_id)
    event_id = expense.event.id
    if request.method == 'POST':
        expense.delete()
        return redirect('event_detail', event_id=event_id)
    return render(request, 'delete_expense.html', {'expense': expense})


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        task.title = title
        task.description = description
        task.save()
        return redirect('event_detail', event_id=task.event.id)
    return render(request, 'update_task.html', {'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    event_id = task.event.id
    if request.method == 'POST':
        task.delete()
        return redirect('event_detail', event_id=event_id)
    return render(request, 'delete_task.html', {'task': task})


@login_required
def dashboard(request):
    page_name = 'Dashboard'
    users = User.objects.all()
    photos = Photo.objects.all()
    logo = photos[0]

    events = Event.objects.all()
    expenses = Expense.objects.all()
    tasks = Task.objects.all()
    completed_tasks = tasks.filter(completed=True)
    pending_tasks = tasks.filter(status='inprogress')

    total_amount = Task.objects.aggregate(
        sum_amount=Sum('amount'))['sum_amount']

    context = {
        'page_name': page_name,
        'events': events,
        'expenses': expenses,
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'users': users,
        'pending_tasks': pending_tasks,
        'logo': logo,
        'total_amount': total_amount,
    }

    return render(request, 'dashboard.html', context)


@login_required
def tasks(request):
    page_name = 'All tasks'

    tasks = Task.objects.order_by('-pk')
    photos = Photo.objects.all()
    new_tasks = Task.objects.order_by('-created_at')
    logo = photos[0]

    total_amount = Task.objects.aggregate(
        sum_amount=Sum('amount'))['sum_amount']

    context = {
        'page_name': page_name,
        'tasks': tasks,
        'logo': logo,
        'total_amount': total_amount,
        'new_tasks': new_tasks,
    }

    return render(request, 'tasks.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')
    # Additional logic or redirection if needed


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Replace 'index' with the appropriate URL name for your index page
            return redirect('tasks')

    return render(request, 'login.html')
