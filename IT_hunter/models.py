from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models


class Vacancy(models.Model):
    title = models.CharField(
        'Название вакансии',
        max_length=50
    )
    specialty = models.ForeignKey(
        'Specialty',
        on_delete=models.CASCADE,
        related_name='vacancies'
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='vacancies'
    )
    skills = models.CharField(
        'Навыки',
        max_length=255
    )
    description = models.TextField('Текст')
    salary_min = models.PositiveIntegerField('Зарплата от')
    salary_max = models.PositiveIntegerField('Зарплата до')
    published_at = models.DateTimeField(
        'Опубликованно',
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(
        'Название компании',
        max_length=50
    )
    location = models.CharField(
        'Город',
        max_length=50
    )
    logo = models.ImageField(
        'Логотип',
        upload_to='speciality_images',
        default='https://place-hold.it/100x60',
    )
    description = models.TextField('Информация о компании')
    employee_count = models.PositiveSmallIntegerField('Количество сотрудников')
    owner = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.SlugField(
        'Код',
        unique=True,
    )
    title = models.CharField(
        'Название специализации',
        max_length=50
    )
    picture = models.ImageField(
        'Картинка',
        upload_to='company_images',
        default='https://place-hold.it/100x60'
    )

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField('Имя', max_length=50)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'"
    )
    written_phone = models.CharField(
        'Телефон ',
        validators=[phone_regex],
        max_length=17,
        blank=True,
    )
    written_cover_letter = models.TextField('Сопроводительное письмо')
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    def __str__(self):
        return self.written_username
