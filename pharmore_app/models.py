from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils.timezone import now  
from django.core.files.storage import FileSystemStorage
receipt_storage = FileSystemStorage(location='media/receipts')

class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock Quantity",
        help_text="Current available stock"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured Product",
        help_text="Display on homepage"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'name']

    def __str__(self):
        return f"{self.name} (Stock: {self.quantity})"

class Cart(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='user_cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Keep only auto_now_add
    updated_at = models.DateTimeField(auto_now=True)

    def total_items(self):
        return self.cartitem_set.count()

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='cart_items'  # Explicit related name
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='in_carts'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'item']

    def __str__(self):
        return f"{self.quantity}x {self.item.name} in Cart #{self.cart.id}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('C', 'Completed'),
        ('X', 'Cancelled'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='P'
    )
    shipping_address = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items'  # Add this line
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name='in_orders'
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.item.name} in Order #{self.order.id}"

class BlogPost(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_posts'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.author.username}"

class Comment(models.Model):
    post = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='post_comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"