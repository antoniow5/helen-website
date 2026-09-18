from django.contrib.auth import authenticate, login, get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Favorite, ProductVariant, Product, Cart, CartItem, Size, Color

User = get_user_model()


def get_cart_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )
    else:
        # Make sure the session has a session key
        if not request.session.session_key:
            request.session.create()

        session_id = request.session.session_key

        cart, created = Cart.objects.get_or_create(
            session_id=session_id
        )

    return cart.items.count()
               


def index(request):
    return render(request, "pages/index.html")


def index2(request):
    return render(request, "archive/index2.html")


def catalog(request):

    cart_items_count = get_cart_count(request)

    sizes = Size.objects.all().order_by('code')
    colors = Color.objects.all().order_by('hex_code')

    context = {
                'cart_items_count': cart_items_count,

                'sizes': sizes,
                'colors': colors,
               }
    return render(request, 'pages/catalog.html', context)


def item2(request):
    return render(request, 'pages/item.html')


def item(request, item_id):

    cart_items_count = get_cart_count(request)

    product = get_object_or_404(Product, id=item_id)

    variants = ProductVariant.objects.filter(product_id=product.id)
    variants = variants.filter(stock_quantity__gt=0) 
    variants = variants.select_related('color', 'size').order_by('size__name', 'color__hex_code')  

    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, product_id=product.id).exists()
    else:
        is_favorited = False

    context = {
        'cart_items_count': cart_items_count,

        'product': product,
        'variants': variants,
        'is_favorited': is_favorited,
    }

    # what to send
    # Basics
        # request user or session
        # cart number of items
    # Item 
        # item itself
        # item photos
        # item variants
        
    return render(request, "pages/item.html", context)


def item_favorite(request, item_id):
    product = get_object_or_404(Product, id=item_id)

    if not request.user.is_authenticated:
        return JsonResponse({'status': False, 'message': "You must be logged in to favorite an item."}, 
                            status = 403)
    
    favorite, created = Favorite.objects.get_or_create(user=request.user, product_id=product.id)
    if not created:
        favorite.delete()
        status = 'deleted'
    else:
        status='created'
        
    return JsonResponse({'status': True, 'message': status})  



def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if variant.stock_quantity <= 0:
        return JsonResponse({
            'status': False,
            'message': 'This product variant is out of stock.'
        }, status=400)

    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )
    else:
        session_id = request.session.session_key

        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        cart, created = Cart.objects.get_or_create(
            session_id=session_id
        )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_variant=variant,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({
        'status': True,
        'message': 'Product added to cart.',
        'quantity': cart_item.quantity,
        'cart_items_count': cart.items.count()
    })


def cart(request):
    return render(request, 'pages/cart.html')



def user_container(request):
    return render(request, 'pages/user_container.html')



def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')  
        else:
            return render(request, 'pages/login.html')
        
    elif request.method == 'POST':
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')

        try:
            username = User.objects.get(email = email)
        except:
            return render(request, 'pages/login.html', {'error': 'Invalid email or password.'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            return render(request, 'pages/login.html', {'error': 'Invalid username or password.'})
    else:
        return HttpResponseForbidden("Invalid request method.")


def logout_user(request):
    pass


def register_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')  
        else:
            return render(request, 'pages/register.html')

    if request.method == 'POST':
        errors = {}
        
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()

        required_fields = { 
            'email': email, 
            'password': password, 
            'repeat_password': repeat_password, 
            'first_name': first_name, 
            'last_name': last_name, 
            } 
        
        for field, value in required_fields.items(): 
            if not value: 
                errors[field] = 'Вы должны заполнить это поле'

        if errors:
            return render(request, 'pages/register.html', context={'error': errors})
        
        if password and repeat_password and password != repeat_password: 
            errors['repeat_password'] = 'Пароли не совпадают'

        if User.objects.filter(email=email).exists():
            errors['email'] = "Пользователь с таким email уже существует"

        try: 
            validate_email(email) 
        except ValidationError: 
            errors['email'] = 'Введите корректный адрес электронной почты'


        if len(first_name) > 35: 
            errors['first_name'] = 'Фамилия не должна превышать 35 символов'

         
        if len(last_name) > 35: 
            errors['last_name'] = 'Имя не должно превышать 35 символов'

        if errors:
            return render(request, 'pages/register.html', context={'error': errors})

        #registration logic
        try:
            user = User(
                username=email,
                email=email,
                first_name = first_name,
                last_name = last_name
            )
            user.set_password(password)
            user.save()
        except:
            message = "Что-то пошло не так"
            return render(request, 'pages/register.html', context={'message': message})
        
        login(request, user)

        return redirect('index')
