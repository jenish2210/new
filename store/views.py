from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

# simple session-based cart
def _get_cart(request):
    return request.session.setdefault('cart', {})

def cart_add(request, product_id):
    cart = _get_cart(request)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session.modified = True
    return redirect('cart_detail')

def cart_remove(request, product_id):
    cart = _get_cart(request)
    cart.pop(str(product_id), None)
    request.session.modified = True
    return redirect('cart_detail')

def cart_detail(request):
    cart = _get_cart(request)
    items = []
    total = 0
    for pid, qty in cart.items():
        try:
            p = Product.objects.get(pk=int(pid))
            subtotal = p.price * qty
            items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
            total += subtotal
        except Product.DoesNotExist:
            pass
    return render(request, 'store/cart_detail.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    cart = _get_cart(request)
    if not cart:
        return redirect('product_list')
    order = Order.objects.create(user=request.user, address='Not provided')
    for pid, qty in cart.items():
        p = Product.objects.get(pk=int(pid))
        OrderItem.objects.create(order=order, product=p, quantity=qty, price=p.price)
    order.paid = True
    order.save()
    request.session['cart'] = {}
    return render(request, 'store/checkout_success.html', {'order': order})

@login_required
def order_history(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
