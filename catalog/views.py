from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from catalog.models import Category, Product, Blog


class CategoryListView(ListView):
    model = Category
    template_name = 'catalog/catalog.html'


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


class ProductDetailView(DetailView):
    """
    Контроллер, который отвечает за отображение одного продукта
    """
    model = Product
    template_name = 'catalog/one_product.html'


class BlogCreateView(CreateView):
    """
    Контроллер, который отвечает за создание поста
    """
    model = Blog
    fields = ('title', 'body', 'image', 'is_published')
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)


class BlogListView(ListView):
    """
    Контроллер, который отвечает за отображение всех постов (опубликованных)
    """
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogUpdateView(UpdateView):
    """
    Контроллер, который отвечает за редактирование поста
    """
    model = Blog
    fields = ('title', 'body', 'image', 'is_published')
    template_name = 'catalog/blog_update.html'

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDetailView(DetailView):
    """
    Контроллер, который отвечает за отображение одного поста
    """
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    """
    Контроллер, который отвечает за удаление поста
    """
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
