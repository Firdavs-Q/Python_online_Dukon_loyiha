from django.contrib import admin
from .models import Post, UserSavat, UserLiked


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'count', 'rate']
    list_filter = ['category']
    search_fields = ['title', 'description']
    list_per_page = 20


@admin.register(UserSavat)
class UserSavatAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__title']
    raw_id_fields = ['user', 'product']


@admin.register(UserLiked)
class UserLikedAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__title']
    raw_id_fields = ['user', 'product']