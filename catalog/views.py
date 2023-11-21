from django.shortcuts import render


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

