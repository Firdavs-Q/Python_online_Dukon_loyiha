import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name='Nomi')
    price = models.FloatField(verbose_name='Narxi')
    description = models.TextField(verbose_name='Tavsif')
    category = models.CharField(max_length=100, verbose_name='Kategoriya')
    image = models.URLField(verbose_name='Rasm URL')
    productId = models.FloatField(verbose_name='Mahsulot ID')
    rate = models.FloatField(verbose_name='Reyting')
    count = models.IntegerField(verbose_name='Soni')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


class UserSavat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Savat'
        verbose_name_plural = 'Savat'

    def __str__(self):
        return f"{self.user.username} → {self.product.title} x {self.quantity}"

    def get_total_price(self):
        return self.product.price * self.quantity


class UserLiked(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_items')
    product = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Yoqtirgan'
        verbose_name_plural = 'Yoqtirganlar'

    def __str__(self):
        return f"{self.user.username} → {self.product.title}"
    
    
class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Kommentariya matni')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Kommentariya'
        verbose_name_plural = 'Kommentariyalar'

    def __str__(self):
        return f"{self.user.username} → {self.product.title}: {self.text[:20]}..."