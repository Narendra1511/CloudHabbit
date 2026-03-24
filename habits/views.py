import json
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import HabitForm, HabitLogForm, RegisterForm
from .models import Habit, HabitLog


def landing(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'habits/landing.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your account has been created successfully.')
        return redirect('dashboard')
    return render(request, 'habits/register.html', {'form': form})


@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user).prefetch_related('logs')
    total_habits = habits.count()
    active_habits = habits.filter(is_active=True).count()
    total_logs = HabitLog.objects.filter(habit__user=request.user, completed=True).count()
    completed_today = HabitLog.objects.filter(habit__user=request.user, date=timezone.localdate(), completed=True).count()
    chart_data = habits.annotate(done=Count('logs', filter=Q(logs__completed=True))).values('title', 'done')
    return render(request, 'habits/dashboard.html', {
        'habits': habits,
        'total_habits': total_habits,
        'active_habits': active_habits,
        'total_logs': total_logs,
        'completed_today': completed_today,
        'chart_labels': json.dumps([item['title'] for item in chart_data]),
        'chart_values': json.dumps([item['done'] for item in chart_data]),
    })


@login_required
def habit_create(request):
    form = HabitForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        habit = form.save(commit=False)
        habit.user = request.user
        habit.save()
        messages.success(request, 'Habit created successfully.')
        return redirect('dashboard')
    return render(request, 'habits/habit_form.html', {'form': form, 'page_title': 'Create habit'})


@login_required
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    form = HabitForm(request.POST or None, instance=habit)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Habit updated successfully.')
        return redirect('dashboard')
    return render(request, 'habits/habit_form.html', {'form': form, 'page_title': 'Edit habit', 'habit': habit})


@login_required
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
        messages.success(request, 'Habit deleted successfully.')
        return redirect('dashboard')
    return render(request, 'habits/habit_confirm_delete.html', {'habit': habit})


@login_required
def habit_detail(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    logs = habit.logs.all()[:30]
    form = HabitLogForm()
    return render(request, 'habits/habit_detail.html', {'habit': habit, 'logs': logs, 'form': form})


@login_required
def toggle_today(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    log, created = HabitLog.objects.get_or_create(habit=habit, date=timezone.localdate(), defaults={'completed': True, 'completed_count': habit.target_per_day})
    if not created:
        log.completed = not log.completed
        log.completed_count = habit.target_per_day
        log.save()
    messages.success(request, f"Today's status updated for {habit.title}.")
    return redirect('dashboard')


@login_required
def log_update_or_create(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    form = HabitLogForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        payload = form.cleaned_data
        log, _ = HabitLog.objects.update_or_create(
            habit=habit,
            date=payload['date'],
            defaults={
                'completed': payload['completed'],
                'completed_count': payload['completed_count'],
                'notes': payload['notes'],
            }
        )
        messages.success(request, 'Habit log saved successfully.')
        return redirect('habit_detail', pk=habit.pk)
    logs = habit.logs.all()[:30]
    return render(request, 'habits/habit_detail.html', {'habit': habit, 'logs': logs, 'form': form})
