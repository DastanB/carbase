from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from main.constants import *
from utils import offer_image_path, offer_image_delete_path, offer_delete_path, validate_file_size, validate_extension

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name

class Image(models.Model):
    description = models.CharField(max_length=255, verbose_name='Описание')
    file = models.FileField(upload_to=offer_image_path, verbose_name='Фото', validators=[validate_file_size, validate_extension], null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images', verbose_name='Автор')

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.description

class AutoMark(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='marks', verbose_name='Логотип')
    
    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

    def __str__(self):
        return self.name

class AutoSaloon(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.CharField(max_length=10000, verbose_name='Описание')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='saloons', verbose_name='Город')
    views = models.PositiveIntegerField(verbose_name='Просмотры')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saloons', verbose_name='Автор')
    marks = models.ManyToManyField(AutoMark, verbose_name='Марки')
    images = models.ManyToManyField(Image, verbose_name='Фотографии')
    
    class Meta:
        verbose_name = 'Автосалон'
        verbose_name_plural = 'Автосалоны'

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name

class ClassCar(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    type_of = models.PositiveSmallIntegerField(choices=CAR_CLASSES, verbose_name='Тип')

    class Meta:
        verbose_name = 'Класс машины'
        verbose_name_plural = 'Классы машин'

    def __str__(self):
        return self.name

class AutoModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    manufactured_in = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cars', verbose_name='Собран в')
    mark = models.ForeignKey(AutoMark, on_delete=models.CASCADE, related_name='cars', verbose_name='Марка машины')
    class_of = models.ForeignKey(ClassCar, on_delete=models.CASCADE, related_name='models', verbose_name='Класс машины')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='models', verbose_name='Фотография')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='models', verbose_name='Автор')

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'

    def __str__(self):
        return self.name

class Option(models.Model):
    type_of = models.PositiveSmallIntegerField(choices=OPTION_TYPES, default=ADDITIONAL, verbose_name='Вид опции')
    name = models.CharField(max_length=550, verbose_name='Название')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='options', verbose_name='Автор')

    class Meta:
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'

    def __str__(self):
        return self.name

class Complectation(models.Model):
    name = models.CharField(max_length=10000, verbose_name='Название')
    color = models.PositiveSmallIntegerField(choices=COLORS, default=WHITE, verbose_name='Цвет')
    description_color = models.CharField(max_length=255, verbose_name='Описание цвета')
    engine_size = models.FloatField(verbose_name='Объем двигателя')
    power = models.PositiveIntegerField(verbose_name='Мощность в л.с')
    torque = models.PositiveIntegerField(verbose_name='Момент в Н.м')
    drive_train = models.PositiveSmallIntegerField(choices=DRIVE_TRAINS, default=FWD, verbose_name='Привод')
    gearbox = models.PositiveSmallIntegerField(choices=GEARBOX_TYPES, default=AUTOMATIC, verbose_name='КПП')
    gears_number = models.PositiveSmallIntegerField(verbose_name='Число скоростей')
    acceleration = models.FloatField(verbose_name='Разгон до 100 км/ч')
    year = models.PositiveIntegerField(verbose_name='Год')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во')
    auto_model = models.ForeignKey(AutoModel, on_delete=models.CASCADE, related_name='complectations', verbose_name='Модель')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comps', verbose_name='Автор')
    

    class Meta:
        verbose_name = 'Комплектация'
        verbose_name_plural = 'Комплектации'

    def __str__(self):
        return self.name

class Discount(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='discounts')

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self):
        return self.title

class Offer(models.Model):
    price = models.PositiveIntegerField(verbose_name='Цена')
    complectation = models.ForeignKey(Complectation, on_delete=models.CASCADE, related_name='offers', verbose_name='Комплектация')
    options = models.ManyToManyField(Option, verbose_name='Опции')
    images = models.ManyToManyField(Image, verbose_name='Фотографии')
    views = models.PositiveIntegerField(verbose_name='Просмотры')
    discounts = models.ManyToManyField(Discount, verbose_name='Акции', default=None)
    date_time = models.DateTimeField(default=datetime.now, verbose_name='Опубликован в')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers', verbose_name='Автор')
    auto_saloon = models.ForeignKey(AutoSaloon, on_delete=models.CASCADE, related_name='comps', verbose_name='Автосалон')
    phone = models.CharField(max_length=16, verbose_name='Номер телефона')


    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'

    def __str__(self):
        return self.complectation.name

class Application(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone = models.CharField(max_length=13)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='apps', verbose_name='Предложение')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
    
    def __str__(self):
        return self.name