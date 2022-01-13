from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

from core.models import Application, Vacancy, Company, Resume

User = get_user_model()


class SignupForm(UserCreationForm):
    """Форма для регистрации на сайте."""

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))

    username_regex = RegexValidator(r'^[a-z0-9_-]{6,16}')
    username = forms.CharField(
        label='Логин',
        max_length=20,
        validators=[username_regex],
        required=True,
        help_text='Логин должен насчитывать от 6 до 16 символов и может состоять из латинских букв и цифр.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ApplicationForm(forms.ModelForm):
    """Форма для создания отклика на вакансию."""

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Отправить'))

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')


class CompanyForm(forms.ModelForm):
    """Фомра для создания своей компании."""

    class Meta:
        model = Company
        fields = ('name', 'location', 'description', 'employee_count', 'logo')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'id': "companyName",
            }),
            'location': forms.TextInput(attrs={
                'class': "form-control",
                'id': "companyLocation",
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'id': "companyInfo",
                'rows': "4",
            }),
            'employee_count': forms.NumberInput(attrs={
                'class': "form-control",
                'id': "companyTeam",
            }),
            'logo': forms.FileInput(attrs={
                'class': "custom-file-input",
                'id': 'inputGroupFile01'
            })
        }


class VacancyForm(forms.ModelForm):
    """Форма для создания своей вакансии."""

    class Meta:
        model = Vacancy
        fields = (
            'title', 'specialty', 'skills',
            'description', 'salary_min', 'salary_max'
        )
        widgets = {
            'title': forms.TextInput(attrs={
                'class': "form-control",
                'id': "vacancyTitle",
            }),
            'specialty': forms.Select(attrs={
                'class': "form-control",
                'id': "userSpecialization",
            }),
            'skills': forms.Textarea(attrs={
                'class': "form-control",
                'id': "vacancySkills",
                'rows': "3",
            }),
            'description': forms.Textarea(attrs={
                'class': "form-control",
                'id': "vacancyDescription",
                'rows': "13",

            }),
            'salary_min': forms.NumberInput(attrs={
                'class': "form-control",
                'id': "vacancySalaryMin",
            }),
            'salary_max': forms.NumberInput(attrs={
                'class': "form-control",
                'id': "vacancySalaryMax",
            }),
        }


class ResumeForm(forms.ModelForm):
    """Форма для создания своего резюме."""

    class Meta:
        model = Resume
        fields = (
            'name', 'surname', 'status', 'salary',
            'specialty', 'grade', 'photo',
            'education', 'experience', 'portfolio'
        )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': "form-control",
                'id': "userName"
            }),
            'surname': forms.TextInput(attrs={
                'class': "form-control",
                'id': "userSurname"
            }),
            'status': forms.Select(attrs={
                'class': "form-control",
                'id': "userReady"
            }),
            'salary': forms.NumberInput(attrs={
                'class': "form-control",
                'id': "userSalary"
            }),
            'specialty': forms.Select(attrs={
                'class': "form-control",
                'id': "userSpecialization"
            }),
            'grade': forms.Select(attrs={
                'class': "form-control",
                'id': "userQualification"
            }),
            'education': forms.Textarea(attrs={
                'class': "form-control text-uppercase",
                'id': "userEducation",
                'rows': "4",
                'style': "color:#000;",
            }),
            'experience': forms.Textarea(attrs={
                'class': "form-control",
                'rows': "4",
                'id': "userExperience",
                'style': "color:#000;"
            }),
            'portfolio': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "http://anylink.github.io",
                'id': "userPortfolio"
            })
        }
