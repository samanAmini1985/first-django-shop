from django.db import models
from django.contrib.auth import get_user_model
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Order(models.Model):
    '''
    to create a new order we should make two models:
    first: a model that saves order and user information
    second: what objects are in this order
    '''
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(decimal_places=2, max_digits=4, null=True, blank=True, default=None)

    class Meta:
        ordering = ('paid', '-updated')

    def __str__(self):
        return f'{self.user} - {str(self.id)}'

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total
            return float(total - discount_price)
        return total


class OrderItem(models.Model):
    '''
    how many items of each product are in cart
    '''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class Coupon(models.Model):
    '''
    this model provide a coupon to discount
    '''
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
