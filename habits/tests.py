from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Habit, HabitLog


class HabitViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='demo', password='Password123!')

    def test_landing_page(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_create_habit_authenticated(self):
        self.client.login(username='demo', password='Password123!')
        response = self.client.post(reverse('habit_create'), {
            'title': 'Drink Water',
            'description': 'Drink more water daily',
            'category': 'Health',
            'frequency': 'daily',
            'target_per_day': 8,
            'start_date': '2026-03-19',
            'color_theme': 'sky',
            'is_active': True,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Habit.objects.count(), 1)

    def test_toggle_today(self):
        self.client.login(username='demo', password='Password123!')
        habit = Habit.objects.create(user=self.user, title='Read', frequency='daily', target_per_day=10)
        response = self.client.get(reverse('toggle_today', args=[habit.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(HabitLog.objects.filter(habit=habit).exists())
