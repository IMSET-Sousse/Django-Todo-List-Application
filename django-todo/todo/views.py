from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Task, Category, Tag
from .forms import TaskForm, CategoryForm, TagForm, RegisterForm

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')
    
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    category_id = request.GET.get('category')
    if category_id:
        tasks = tasks.filter(category__id=category_id)
    
    tag_id = request.GET.get('tag')
    if tag_id:
        tasks = tasks.filter(tags__id=tag_id)
    
    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority=priority)
    
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {
        'tasks': tasks,
        'categories': categories,
        'tags': tags,
        'search_query': search_query,
        'selected_category': int(category_id) if category_id else None,
        'selected_tag': int(tag_id) if tag_id else None,
        'selected_priority': int(priority) if priority else None,
    }
    return render(request, 'todo/task_list.html', context)

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            form.save_m2m()  # Save many-to-many relations (tags)
            messages.success(request, 'Task created successfully!')
            return redirect('todo:task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('todo:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('todo:task_list')
    return render(request, 'todo/task_confirm_delete.html', {'task': task})

@login_required
def manage_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('todo:manage_categories')
    else:
        form = CategoryForm()
    
    categories = Category.objects.all()
    return render(request, 'todo/manage_categories.html', {
        'form': form,
        'categories': categories
    })

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
    return redirect('todo:manage_categories')

@login_required
def manage_tags(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag added successfully!')
            return redirect('todo:manage_tags')
    else:
        form = TagForm()
    
    tags = Tag.objects.all()
    return render(request, 'todo/manage_tags.html', {
        'form': form,
        'tags': tags
    })

@login_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
    return redirect('todo:manage_tags')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'todo/register.html', {'form': form})