from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from collections import defaultdict
import json
from django.utils.safestring import mark_safe

from .models import Todo

# Create your views here.
def index(request):
    sort = request.GET.get('sort', None)
    filter_by = request.GET.get('filter', None)

    todos = Todo.objects.all()

    if filter_by == 'completed':
        todos = todos.filter(complete=True)
    elif filter_by == 'incomplete':
        todos = todos.filter(complete=False)

    if sort == 'created_at_asc':
        todos = todos.order_by('created_at') 
    elif sort == 'created_at_desc':
        todos = todos.order_by('-created_at') 
    elif sort == 'completed_first':
        todos = todos.order_by('-complete', 'created_at') 
    elif sort == 'incomplete_first':
        todos = todos.order_by('complete', 'created_at') 
    elif sort == 'deadline_asc':
        todos = todos.order_by('deadline_at')
    elif sort == 'deadline_desc':
        todos = todos.order_by('-deadline_at')

    return render(request, "base.html", {"todo_list": todos})


@require_http_methods(["POST"])
def add(request):
    # if request.method == "POST":
    title = request.POST["title"]
    description = request.POST["description"]

    try:
        deadline_days = int(request.POST["deadline_days"])
    except ValueError:
        messages.error(request, "Invalid input for deadline days. Please enter a valid integer.")
        return redirect("index")
    
    deadline_at = datetime.now() + timedelta(days=deadline_days)
    if title and description:
        todo = Todo(title=title, description=description, deadline_at=deadline_at)
        todo.save()
    return redirect("index")

def update(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.complete = not todo.complete
    todo.save()
    return redirect("index")

@require_http_methods(["POST", "GET"])
def edit(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    
    if request.method == 'POST':
        try:
            todo.title = request.POST["title"]
            todo.description = request.POST["description"]
            todo.save()
            return redirect("index")
        except KeyError:
            # Обработка ситуации, когда нужные ключи отсутствуют
            return render(request, 'edit.html', {'todo': todo, 'error': 'Пожалуйста, заполните все поля.'})
    
    # Обработка GET-запроса для отображения формы
    return render(request, 'edit.html', {'todo': todo})

def delete(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    return redirect("index")

def calendar(request):
    tasks = Todo.objects.all()
    tasks_by_date = defaultdict(list)
    
    for task in tasks:
        task_date_str = task.deadline_at.strftime('%Y-%m-%d')
        tasks_by_date[task_date_str].append(task.title)

    tasks_by_date_json = mark_safe(json.dumps(tasks_by_date))

    return render(request, 'calendar.html', {'tasks_by_date_json': tasks_by_date_json})

