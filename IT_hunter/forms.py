from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from IT_hunter.models import Application, Vacancy, Company


class SignupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Зарегистрироваться'))

        self.helper.form_class = 'form-signup pt-5'
        self.helper.label_class = 'col-lg-6'
        self.helper.field_class = 'col-lg-12'

    username = forms.CharField(label='Логин', max_length=20)
    first_name = forms.CharField(label='Имя', max_length=20)
    last_name = forms.CharField(label='Фамилия', max_length=20)
    email = forms.CharField(
        label='Почтовый адресс',
        widget=forms.EmailInput()
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

        username = self.cleaned_data['username']

        for user in User.objects.all():
            if username in user.username:
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Войти'))

        self.helper.form_class = "form-signin pt-5"
        self.helper.label_class = "col-lg-6"
        self.helper.field_class = "col-lg-12"

    username = forms.CharField(label='Логин', max_length=20)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class ApplicationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit('submit', 'Отправить'))

        self.helper.form_class = "card mt-4 mb-3"
        self.helper.label_class = "col-lg-6"

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

    def save(self, request, id):
        Application.objects.create(
            user=request.user,
            vacancy=Vacancy.objects.get(id=id),
            written_username=self.cleaned_data['written_username'],
            written_phone=self.cleaned_data['written_phone'],
            written_cover_letter=self.cleaned_data['written_cover_letter']
        )


class CompanyForm(forms.ModelForm):

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
            'employee_count': forms.TextInput(attrs={
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