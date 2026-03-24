from datetime import timedelta
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Habit(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    target_per_day = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    start_date = models.DateField(default=timezone.localdate)
    color_theme = models.CharField(max_length=30, default='sky')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('user', 'title')

    def __str__(self):
        return self.title

    @property
    def current_streak(self):
        logs = self.logs.filter(completed=True).order_by('-date').values_list('date', flat=True)
        if not logs:
            return 0
        streak = 0
        today = timezone.localdate()
        expected = today
        log_set = set(logs)
        if today not in log_set and (today - timedelta(days=1)) in log_set:
            expected = today - timedelta(days=1)
        while expected in log_set:
            streak += 1
            expected -= timedelta(days=1)
        return streak

    @property
    def completion_rate(self):
        total = self.logs.count()
        if total == 0:
            return 0
        done = self.logs.filter(completed=True).count()
        return round((done / total) * 100)


class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(default=timezone.localdate)
    completed = models.BooleanField(default=False)
    notes = models.CharField(max_length=255, blank=True)
    completed_count = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-updated_at']
        unique_together = ('habit', 'date')

    def __str__(self):
        return f'{self.habit.title} - {self.date}'
