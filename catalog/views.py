from django.shortcuts import render
from catalog.models import Category, Product


def catalog(request):
    """
    Контроллер, который отвечает за отображение каталога продуктов
    """
    category_list = Category.objects.all()
    context = {
        'object_list': category_list

    }
    return render(request, 'catalog/catalog.html', context)


def display_home_page(request):
    """
    Контроллер, который отвечает за отображение домашней страницы
    """
    return render(request, 'catalog/home_page.html')


def display_contact_info(request):
    """
    Контроллер, который отвечает за отображение контактной информации
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print(f'Имя: {name}, телефон: {phone}, сообщение: {message}')

    return render(request, 'catalog/contact_info.html')


def product(request, category_id):
    """
    Контроллер, который отвечает за отображение продуков
    """
    category = Category.objects.get(id=category_id)
    product_list = Product.objects.filter(category_id=category)

    context = {
        'object_list': product_list,
        'category': category
    }
    return render(request, 'catalog/product.html', context)


def one_product(request, pk):
    product_item = Product.objects.get(pk=pk)

    context = {
        'product': product_item,
    }

    return render(request, 'catalog/one_product.html', context)
