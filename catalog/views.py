from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm, ProductFormModerator
from catalog.models import Product, Blog, Version
from catalog.services import get_categories_cache


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


@login_required
def categories(request):
    """
    Контроллер, который отвечает за отображение категорий
    """

    context = {
        'object_list': get_categories_cache(),
        'title': 'Все категории'
    }

    return render(request, 'catalog/categories.html', context)


class ProductListView(LoginRequiredMixin, ListView):
    """
    Контроллер, который отвечает за отображение списка всех продуктов
    """
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = Product.objects.filter(owner=self.request.user)
        active_versions = Version.objects.filter(is_active=True).select_related('product_name')
        active_products = {version.product_name_id: version for version in active_versions}
        for product in queryset:
            product.active_version = active_products.get(product.id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['version'] = queryset
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Контроллер, который отвечает за создание продукта
    """
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse('catalog:product_list')

    def form_valid(self, form):
        user = form.save()
        user.owner = self.request.user
        user.save()

        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """
    Контроллер, который отвечает за изменение продукта
    """
    permission_required = 'catalog.change_product'
    model = Product
    form_class = ProductForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user and not self.request.user.is_superuser:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])

    def form_valid(self, form):
        user = form.save()
        user.owner = self.request.user
        user.save()

        return super().form_valid(form)

    def get_form_class(self):
        if self.request.user.groups.filter(name='Moderator').exists():
            return ProductFormModerator
        else:
            return ProductForm


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Контроллер, который отвечает за отображение одного продукта
    """
    model = Product
    form_class = ProductForm


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер, который отвечает за удаление продукта
    """
    model = Product
    success_url = reverse_lazy('catalog:product_list')


class VersionCreateView(CreateView):
    """
    Контроллер, который отвечает за создание версии продукта
    """
    model = Version
    form_class = VersionForm

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])


def not_login(request):
    """
    Контроллер, который отвечает за страницу, на которую перенаправляет пользователя, если он не авторизован
    """
    return render(request, 'catalog/not_login.html')


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
