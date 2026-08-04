from django import forms
from django.contrib.auth.models import User
from .models import ContactMessage, Reservation, UserProfile
import datetime


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username or Email',
            'id': 'login-username',
            'required': True,
        }),
        label='Username / Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
            'id': 'login-password',
            'required': True,
        }),
        label='Password'
    )


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First Name',
            'id': 'reg-fname',
            'required': True,
        })
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last Name',
            'id': 'reg-lname',
            'required': True,
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Desired Username',
            'id': 'reg-username',
            'required': True,
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'email@example.com',
            'id': 'reg-email',
            'required': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password (min 8 chars)',
            'id': 'reg-password',
            'required': True,
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm Password',
            'id': 'reg-confirm-password',
            'required': True,
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        username = cleaned_data.get('username')
        if username and User.objects.filter(username=username).exists():
            self.add_error('username', 'Username already taken.')

        email = cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            self.add_error('email', 'An account with this email already exists.')

        return cleaned_data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your registered email address',
            'id': 'forgot-email',
            'required': True,
        }),
        label='Registered Email Address'
    )


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter new password',
            'id': 'reset-new-password',
            'required': True,
        }),
        label='New Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm new password',
            'id': 'reset-confirm-password',
            'required': True,
        }),
        label='Confirm New Password'
    )

    def clean(self):
        cleaned_data = super().clean()
        new_pass = cleaned_data.get('new_password')
        confirm_pass = cleaned_data.get('confirm_password')

        if new_pass and confirm_pass and new_pass != confirm_pass:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-input'}),
            'email':      forms.EmailInput(attrs={'class': 'form-input'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'dietary_preferences', 'favorite_table_notes', 'profile_photo']
        widgets = {
            'phone':                forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000'}),
            'address':              forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'dietary_preferences':  forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Vegetarian, Nut Allergy'}),
            'favorite_table_notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 2, 'placeholder': 'Window table preferred, sparkling water'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model  = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
                'id': 'contact-name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com',
                'id': 'contact-email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+1 (555) 000-0000',
                'id': 'contact-phone',
            }),
            'subject': forms.Select(attrs={
                'class': 'form-select',
                'id': 'contact-subject',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Tell us how we can help you...',
                'rows': 5,
                'id': 'contact-message',
            }),
        }
        labels = {
            'name':    'Full Name',
            'email':   'Email Address',
            'phone':   'Phone (optional)',
            'subject': 'Subject',
            'message': 'Message',
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'guests', 'date', 'time', 'occasion', 'seating_preference', 'special_requests']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Full Name',
                'id': 'res-name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'name@example.com',
                'id': 'res-email',
                'required': True,
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+1 (555) 000-0000',
                'id': 'res-phone',
                'required': True,
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1,
                'max': 20,
                'value': 2,
                'id': 'res-guests',
                'required': True,
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
                'id': 'res-date',
                'min': datetime.date.today().isoformat(),
                'required': True,
            }),
            'time': forms.Select(attrs={
                'class': 'form-select',
                'id': 'res-time',
                'required': True,
            }),
            'occasion': forms.Select(attrs={
                'class': 'form-select',
                'id': 'res-occasion',
            }),
            'seating_preference': forms.Select(attrs={
                'class': 'form-select',
                'id': 'res-seating',
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Dietary requirements, allergies, high chairs, table preferences...',
                'rows': 4,
                'id': 'res-special-req',
            }),
        }