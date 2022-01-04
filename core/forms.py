from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
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


class ApplicationForm(forms.Form):
    """Форма для создания отклика на вакансию."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit('submit', 'Отправить'))

    written_username = forms.CharField(
        label='Имя',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'id': "userName",
        })
    )
    written_phone = forms.IntegerField(
        label='Телефон',
        widget=forms.NumberInput(attrs={
            'class': "form-control",
            'id': "userPhone",
            'placeholder': "79999999999"
        })
    )
    written_cover_letter = forms.CharField(
        label='Сопроводительное письмо',
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'id': "userMsg",
            'rows': "8"
        })
    )

    def save(self, user, pk):
        Application.objects.create(
            user=user,
            vacancy=Vacancy.objects.get(pk=pk),
            written_username=self.cleaned_data['written_username'],
            written_phone=self.cleaned_data['written_phone'],
            written_cover_letter=self.cleaned_data['written_cover_letter']
        )


class CompanyForm(forms.ModelForm):
    """Фомра для создания своей компании."""

    class Meta:
        model = Company
        fields = ('name', 'location', 'description', 'employee_count')
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
            })
        }

    def save(self, request):
        if len(request.FILES) != 0:
            logo = "/company_images/" + str(request.FILES['logo'])
        else:
            try:
                logo = Company.objects.get(owner=request.user).logo
            except ObjectDoesNotExist:
                logo = None
        obj, created = Company.objects.update_or_create(
            owner=request.user,
            defaults={
                'name': self.cleaned_data['name'],
                'location': self.cleaned_data['location'],
                'description': self.cleaned_data['description'],
                'employee_count': self.cleaned_data['employee_count'],
                'logo': logo
            }
        )


class VacancyForm(forms.ModelForm):
    """Форма для создания своей вакансии."""

    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'skills', 'description', 'salary_min', 'salary_max')
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

    def save(self, user, pk):
        company = Company.objects.get(owner=user)
        obj, created = Vacancy.objects.update_or_create(
            pk=pk,
            defaults={
                'title': self.cleaned_data['title'],
                'specialty': self.cleaned_data['specialty'],
                'company': company,
                'skills': self.cleaned_data['skills'],
                'description': self.cleaned_data['description'],
                'salary_max': self.cleaned_data['salary_max'],
                'salary_min': self.cleaned_data['salary_min']
            }
        )


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

    def save(self, user):
        obj, created = Resume.objects.update_or_create(
            user=user,
            defaults={
                'name': self.cleaned_data['name'],
                'surname': self.cleaned_data['surname'],
                'status': self.cleaned_data['status'],
                'salary': self.cleaned_data['salary'],
                'specialty': self.cleaned_data['specialty'],
                'grade': self.cleaned_data['grade'],
                'education': self.cleaned_data['education'],
                'experience': self.cleaned_data['experience'],
                'portfolio': self.cleaned_data['portfolio'],
            }
        )
