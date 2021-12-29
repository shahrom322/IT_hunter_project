from django import template

register = template.Library()


def replace(string):
    return string.replace(',', ' •')


def convert_digit(number):
    return f'{number:,}'


register.filter('replace', replace)
register.filter('convert_digit', convert_digit)
