# from django.shortcuts import render

# # Create your views here.

import requests
from django.shortcuts import render

def home(request):
    # # API'ni chaqirish
    # api_url = 'https://fakestoreapi.com/products'
    # response = requests.get(api_url)
    
    # if response.status_code == 200:  # Muvaffaqiyatli bo'lsa
    #     products = response.json()  # JSON'ni Python list (massiv) ga aylantirish
    # else:
    #     products = []  # Xato bo'lsa, bo'sh list
    #     print(f"API xatosi: {response.status_code}")  # Terminalda ko'rsatish
    
    # Template'ga uzatish {'products': products}
    return render(request, 'home.html', )  # products – massiv

def sahif(request):
    return render(request, 'sahif.html')