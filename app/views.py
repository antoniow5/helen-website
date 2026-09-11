from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth import authenticate, login

from .models import Favorite, ProductVariant, Product, Cart, CartItem


def index(request):
    return render(request, "index.html")

def index2(request):
    return render(request, "index2.html")

def catalog(request):
    return render(request, 'catalog.html')


def item(request):
    return render(request, 'item.html')


def item2(request, item_id):
    cart_items_count = 0
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart_items_count = cart.items.count()
    else:
        session_id = request.session.session_key
        if session_id:
            cart = Cart.objects.filter(session_id=session_id).first()
            if cart:
                cart_items_count = cart.items.count()



    product = Product.objects.get_or_404(id=item_id)
    variants = ProductVariant.objects.filter(product_id=product.id)

    variants = variants.filter(stock_quantity__gt=0) 
    variants = variants.select_related('color', 'size')  

    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, product_id=product.id).exists()
    else:
        is_favorited = False

    context = {
        'product': product,
        'variants': variants,
        'is_favorited': is_favorited,
        'cart_items_count': cart_items_count,
    }

    
    # what to send
    # Basics
        # request user or session
        # cart number of items
    # Item 
        # item itself
        # item photos
        # item variants
        

    return render(request, "item.html", context)


def item_favorite(request, item_id):
    product = Product.objects.get_or_404(id=item_id)

    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to favorite an item.")
    
    favorite, created = Favorite.objects.get_or_create(user=request.user, product_id=product.id)
    if not created:
        favorite.delete()

    return HttpResponse(status=204)  


def add_to_cart(request, variant_id):
    variant = ProductVariant.objects.get_or_404(id=variant_id)

    if variant.stock_quantity <= 0:
        return HttpResponse("This product variant is out of stock.", status=400)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=variant)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return HttpResponse(status=204)  # Redirect to the cart page after adding the item



def cart(request):
    return render(request, 'cart.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('index')  
    else:
        return render(request, 'login.html')


def authentication(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return HttpResponseForbidden("Invalid request method.")
    