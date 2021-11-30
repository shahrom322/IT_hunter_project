from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


User = get_user_model()


class Vacancy(models.Model):
    title = models.CharField(
        'Название вакансии',
        max_length=50
    )
    specialty = models.ForeignKey(
        'Specialty',
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Специальность',
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Компания'
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

    class Meta:
        ordering = ['-published_at']


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
        upload_to='company_images',
        default='https://place-hold.it/100x60',
    )
    description = models.TextField('Информация о компании')
    employee_count = models.PositiveSmallIntegerField('Количество сотрудников')
    owner = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Владелец'
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
        upload_to='specialties_images',
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
        related_name='applications',
        verbose_name='Вакансия'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Пользователь'
    )

    def __str__(self):
        return self.written_username


class Resume(models.Model):
    STATUS = [
        ('0', 'Не ищу работу'),
        ('1', 'Рассматриваю предложения'),
        ('2', 'Ищу работу')
    ]
    GRADE = [
        ('0', 'Стажер'),
        ('1', 'Джуниор'),
        ('2', 'Мидл'),
        ('3', 'Сеньор'),
        ('4', 'Лид')
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Пользователь'
    )
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    status = models.CharField(
        'Статус',
        choices=STATUS,
        default=None,
        max_length=50
    )
    salary = models.PositiveIntegerField('Зарплата')
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.CASCADE,
        related_name='resume',
        verbose_name='Специальность'
    )
    grade = models.CharField(
        'Квалификация',
        choices=GRADE,
        default=None,
        max_length=50
    )
    photo = models.ImageField(
        'Фотография',
        upload_to='user_images',
        default='https://place-hold.it/100x60',
    )
    education = models.CharField('Образование', max_length=100)
    experience = models.TextField('Опыт работы', null=True)
    description = models.TextField('О себе', null=True)
    portfolio = models.CharField('Портфолио', max_length=100)
    phone = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефонный номер должен быть в формате: '+999999999'"
    )
    phone = models.CharField(
        'Телефон ',
        validators=[phone],
        max_length=17,
        blank=True
    )

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        ordering = ['-pk']