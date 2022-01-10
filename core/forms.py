from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from core.models import Application, Vacancy, Company, Resume


User = get_user_model()


class SignupForm(forms.Form):
    """Форма для регистрации на сайте."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))

    username_regex = RegexValidator(r'^[a-z0-9_-]{6,16}')
    username = forms.CharField(
        label='Логин',
        max_length=20,
        validators=[username_regex],
        required=True,
        help_text='Логин должен насчитывать от 6 до 16 символов и может состоять из латинских букв и цифр.'
    )
    first_name = forms.CharField(label='Имя', max_length=20)
    last_name = forms.CharField(label='Фамилия', max_length=20)
    email = forms.CharField(
        label='Почтовый адресс',
        widget=forms.EmailInput(),
        help_text='Минимум 6 символов'
    )
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    repeat_password = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput()
    )

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['repeat_password']

        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')

        username = self.cleaned_data.get('username', None)

        if not username:
            raise forms.ValidationError('Поле логина не верно')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'Пользователь с таким логином уже существует'
            )

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.save()
        auth = authenticate(**self.cleaned_data)
        return auth


class LoginForm(forms.Form):
    """Форма для авторизации на сайте."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Войти'))

    username = forms.CharField(label='Логин', max_length=20)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class ApplicationForm(forms.ModelForm):

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
            'name', 'surname', 'status',
            'salary', 'specialty', 'grade',
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

