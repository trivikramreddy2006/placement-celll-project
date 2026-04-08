from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    branch = forms.CharField(max_length=100, required=False, help_text="Required if registering as a Student")
    cgpa = forms.DecimalField(max_digits=4, decimal_places=2, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('role')
        if commit:
            user.save()
            if user.is_student():
                StudentProfile.objects.create(
                    user=user,
                    branch=self.cleaned_data.get('branch', 'Not Specified'),
                    cgpa=self.cleaned_data.get('cgpa', 0.0),
                    active_backlogs=0,
                    is_blacklisted=False
                )
        return user
