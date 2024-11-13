from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

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

    return render(request, "base.html", {"todo_list": todos})


@require_http_methods(["POST"])
def add(request):
    # if request.method == "POST":
    title = request.POST["title"]
    description = request.POST["description"]
    if title and description:
        todo = Todo(title=title, description=description)
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

