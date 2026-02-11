from itertools import product
from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Sum, F
from databases.models import Post, UserSavat, UserLiked
from django.db.models import Q
from django.db.models import Sum

class HOMEPageView(TemplateView):
    model = Post
    template_name = 'homeP.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get("q", "").strip()

        products = self.model.objects.all()

        # 🔍 SEARCH
        if q:
            products = products.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        context['products'] = products
        context['q'] = q   # input ichida yozuv qolishi uchun

        # ❤️ LIKE + 🛒 CART
        if self.request.user.is_authenticated:
            liked_products = UserLiked.objects.filter(
                user=self.request.user
            ).values_list('product_id', flat=True)

            context['liked_products'] = list(liked_products)

            cart_count = UserSavat.objects.filter(
                user=self.request.user
            ).aggregate(total=Sum('quantity'))['total'] or 0

            context['cart_count'] = cart_count
        else:
            context['liked_products'] = []
            context['cart_count'] = 0

        return context

    


class SavatView(TemplateView):
    template_name = 'savat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if not user.is_authenticated:
            context['products'] = []
            context['total_price'] = 0
            context['total_items'] = 0
            return context

        
        cart_items = UserSavat.objects.filter(
            user=user
        ).select_related('product')
        
        context['products'] = cart_items
        
        
        total_price = sum(item.get_total_price() for item in cart_items)
        context['total_price'] = total_price
        
        
        total_items = sum(item.quantity for item in cart_items)
        context['total_items'] = total_items

        return context


class LikedView(TemplateView):
    
    template_name = 'yoqtirgan.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if not user.is_authenticated:
            context['products'] = []
            return context

        
        liked_items = UserLiked.objects.filter(
            user=user
        ).select_related('product')
        
        context['products'] = [item.product for item in liked_items]

        return context


def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('home')
    
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Savatga qo'shish uchun tizimga kiring!")
        return redirect('home')

    product = get_object_or_404(Post, id=product_id)
    
    
    cart_item, created = UserSavat.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
       
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"✅ {product.title} miqdori oshirildi! (Jami: {cart_item.quantity})")
    else:
        messages.success(request, f"✅ {product.title} savatga qo'shildi!")

   
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def toggle_like(request, product_id):
    if request.method != 'POST':
        return redirect('home')
    
    if not request.user.is_authenticated:
        messages.warning(request, "⚠️ Like bosish uchun tizimga kiring!")
        return redirect('home')

    product = get_object_or_404(Post, id=product_id)
    
    
    liked_item = UserLiked.objects.filter(
        user=request.user,
        product=product
    ).first()

    if liked_item:
       
        liked_item.delete()
        messages.info(request, f"💔 {product.title} like'dan olib tashlandi!")
    else:
       
        UserLiked.objects.create(
            user=request.user,
            product=product
        )
        messages.success(request, f"❤️ {product.title} like qilindi!")

    
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def remove_from_cart(request, product_id):
    if request.method != 'POST':
        return redirect('savat')
    
    if not request.user.is_authenticated:
        return redirect('home')

    cart_item = get_object_or_404(
        UserSavat,
        user=request.user,
        product_id=product_id
    )
    
    product_title = cart_item.product.title
    cart_item.delete()
    messages.success(request, f"🗑️ {product_title} savatdan olib tashlandi!")

    return redirect('savat')


def update_cart_quantity(request, product_id):
    if request.method != 'POST':
        return redirect('savat')
    
    if not request.user.is_authenticated:
        return redirect('home')

    cart_item = get_object_or_404(
        UserSavat,
        user=request.user,
        product_id=product_id
    )
    
    action = request.POST.get('action')
    
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, "✅ Miqdor oshirildi!")
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, "✅ Miqdor kamaytirildi!")
        else:
            cart_item.delete()
            messages.info(request, "🗑️ Mahsulot savatdan olib tashlandi!")

    return redirect('savat')

def buyurtma_berish(request):
    models = UserSavat.objects.filter(user=request.user)
    return render(request, 'payment.html', {'models': models})


def payment(request):
    products = UserSavat.objects.filter(user=request.user)
    return render(request, 'payment.html', {'products': products})


def bosh_sahifaga_qaytarish(request):
    messages.success(request, "✅ To'lov muvaffaqiyatli amalga oshirildi! Rahmat!")
    return render(request, 'homeP.html')