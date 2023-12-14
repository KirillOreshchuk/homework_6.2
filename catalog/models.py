from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    objects = None
    name = models.CharField(max_length=50, verbose_name='Продукт')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey('catalog.Category',
                                 on_delete=models.CASCADE,
                                 verbose_name='Категория',
                                 )
    price = models.IntegerField(verbose_name='Цена')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    last_change_date = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=50, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание категории', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, **NULLABLE, verbose_name='slug')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='products/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Статус')
    view_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Посты'


class Version(models.Model):
    objects = None
    VERSION_CHOICES = ((True, 'активная'), (False, 'не активная'))

    product_name = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.IntegerField(default=1, blank=True, verbose_name='Номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Версия')
    is_active = models.BooleanField(choices=VERSION_CHOICES, verbose_name='Статус версии')

    def __str__(self):
        return f'версия:{self.version_name} номер версии: {self.version_number}'

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ('version_number',)


@receiver(post_save, sender=Version)
def set_current_version(sender, instance, **kwargs):
    if instance.is_active:
        Version.objects.filter(product_name=instance.product_name).exclude(pk=instance.pk).update(is_active=False)
