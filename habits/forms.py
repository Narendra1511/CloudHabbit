from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Habit, HabitLog


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class StyledAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class HabitForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=timezone.localdate)

    class Meta:
        model = Habit
        fields = ['title', 'description', 'category', 'frequency', 'target_per_day', 'start_date', 'color_theme', 'is_active']

    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 3:
            raise forms.ValidationError('Habit title must be at least 3 characters long.')
        return title


class HabitLogForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=timezone.localdate)

    class Meta:
        model = HabitLog
        fields = ['date', 'completed', 'completed_count', 'notes']

    def clean_notes(self):
        return self.cleaned_data['notes'].strip()
