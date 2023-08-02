from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Category(models.Model):
    '''
    this is a model for all categories, that ordered by name of category by class Meta
    '''

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', blank=True, null=True)
    is_sub = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolut_url(self):
        return reverse('home:category_filter', args=[self.slug, ])


class Product(models.Model):
    '''
    this is a model for products it has a foreignkey to Category model
    '''
    category = models.ManyToManyField(Category, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField()
    description = RichTextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug])
