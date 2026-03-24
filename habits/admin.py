from django.contrib import admin
from .models import Habit, HabitLog


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'frequency', 'target_per_day', 'is_active', 'created_at')
    search_fields = ('title', 'user__username', 'category')
    list_filter = ('frequency', 'is_active', 'color_theme')


@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):
    list_display = ('habit', 'date', 'completed', 'completed_count', 'updated_at')
    search_fields = ('habit__title', 'notes')
    list_filter = ('completed', 'date')
