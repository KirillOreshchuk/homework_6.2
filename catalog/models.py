from django.db import models

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
    creation_date = models.DateTimeField(**NULLABLE, verbose_name='Дата создания')
    last_change_date = models.DateTimeField(**NULLABLE, verbose_name='Дата последнего изменения')

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
    created_at = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, **NULLABLE, verbose_name='Статус')
    view_count = models.IntegerField(default=0, **NULLABLE, verbose_name='Количество просмотров')

    def __str__(self):
        return {self.title}

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Посты'
