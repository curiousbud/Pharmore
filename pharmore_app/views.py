from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Item, Cart, CartItem, Order, OrderItem, BlogPost, Comment
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .forms import ItemForm, BlogPostForm, CommentForm
from .utils import generate_receipt
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm

def home(request):
    featured_items = Item.objects.filter(is_featured=True)[:3]
    recent_posts = BlogPost.objects.order_by('-created_at')[:2] if request.user.is_authenticated else None
    return render(request, 'home.html', {
        'featured_items': featured_items,
        'recent_posts': recent_posts
    })
def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Cart.objects.create(user=user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@staff_member_required
def admin_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            return redirect('manage_users')
    else:
        form = UserCreationForm()
    return render(request, 'admin_register.html', {'form': form})

@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Item, Cart, CartItem

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1
            
        if quantity < 1:
            messages.error(request, "Quantity must be at least 1")
            return redirect('item_list')
            
        if quantity > item.quantity:
            messages.error(request, f"Only {item.quantity} available in stock")
            return redirect('item_list')
            
        # Get or create user's cart
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Update or create cart item
        cart_item, created = CartItem.objects.update_or_create(
            cart=cart,
            item=item,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity = quantity  # Set exact quantity
            cart_item.save()
        
        messages.success(request, f"Added {quantity} {item.name} to cart")
        
    return redirect('item_list')

@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()  # Changed from cartitem_set to cart_items
    total = sum(item.item.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.cart_items.all()  # Use 'cart_items' instead of 'cartitem_set'

    total = 0
    for cart_item in cart_items:
        total += cart_item.quantity * cart_item.item.price

    order = Order.objects.create(
        user=request.user,
        total_price=total,
        shipping_address=request.POST.get('shipping_address', ''),
        payment_method=request.POST.get('payment_method', '')
    )

    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            item=cart_item.item,
            quantity=cart_item.quantity,
            price=cart_item.item.price
        )

    cart_items.delete()  # Clear the cart after checkout

    return render(request, 'checkout.html', {'order': order})

@staff_member_required
def manage_items(request):
    items = Item.objects.all()
    return render(request, 'manage_items.html', {'items': items})

@staff_member_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Added {item.quantity} units of {item.name}")
            return redirect('manage_items')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

@staff_member_required
def update_stock(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        try:
            item.quantity = int(new_quantity)
            item.save()
            messages.success(request, f"Updated stock for {item.name} to {item.quantity}")
        except ValueError:
            messages.error(request, "Invalid quantity value")
        return redirect('manage_items')
    return render(request, 'update_stock.html', {'item': item})

@staff_member_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('manage_items')

@staff_member_required
def manage_users(request):
    users = User.objects.filter(is_staff=False)
    return render(request, 'manage_users.html', {'users': users})

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_users')

def logout_view(request):
    logout(request)  # Log the user out
    return redirect('login')

@login_required
def download_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Create in-memory PDF buffer
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- Pharmacy Header ---
    p.setFont("Helvetica-Bold", 16)
    p.drawString(20*mm, height-20*mm, "PHARMORE DRUGSTORE")
    p.setFont("Helvetica", 10)
    p.drawString(20*mm, height-25*mm, "123 Wellness Lane")
    p.drawString(20*mm, height-30*mm, "New Delhi, DL 110001")
    p.drawString(20*mm, height-35*mm, "License No: DL/2024/PHARM/12345")

    # --- Receipt Details ---
    p.line(20*mm, height-40*mm, width-20*mm, height-40*mm)
    p.setFont("Courier-Bold", 12)
    p.drawString(20*mm, height-45*mm, "MEDICAL INVOICE")
    p.setFont("Courier", 10)
    p.drawString(20*mm, height-50*mm, f"Date: {order.created_at.strftime('%d-%b-%Y %I:%M %p')}")
    p.drawString(20*mm, height-55*mm, f"Order ID: PH{order.id:05d}")

    # --- Items Table ---
    y_position = height - 65*mm
    p.setFont("Courier-Bold", 10)
    p.drawString(20*mm, y_position, "MEDICINE NAME")
    p.drawString(100*mm, y_position, "QTY")
    p.drawString(130*mm, y_position, "PRICE")
    p.drawString(160*mm, y_position, "TOTAL")
    
    y_position -= 5*mm
    p.line(20*mm, y_position, width-20*mm, y_position)
    y_position -= 7*mm
    
    p.setFont("Courier", 10)
    for item in order.order_items.all():
        p.drawString(22*mm, y_position, item.item.name[:25])  # Truncate long names
        p.drawString(102*mm, y_position, str(item.quantity))
        p.drawString(132*mm, y_position, f"₹{item.price:.2f}")
        p.drawString(162*mm, y_position, f"₹{item.price * item.quantity:.2f}")
        y_position -= 5*mm

    # --- Totals ---
    y_position -= 5*mm
    p.line(20*mm, y_position, width-20*mm, y_position)
    y_position -= 7*mm
    p.setFont("Courier-Bold", 12)
    p.drawString(140*mm, y_position, "TOTAL:")
    p.drawString(160*mm, y_position, f"₹{order.total_price:.2f}")

    # --- Pharmacy Footer ---
    y_position -= 15*mm
    p.setFont("Courier-Oblique", 8)
    p.drawString(20*mm, y_position, "* This is a computer generated invoice")
    y_position -= 5*mm
    p.drawString(20*mm, y_position, "* Store Timing: 24x7")
    y_position -= 5*mm
    p.drawString(20*mm, y_position, "* For returns, contact within 24 hours")
    y_position -= 5*mm
    p.drawString(20*mm, y_position, "GSTIN: 07AAACP8819J1Z1")

    # Finalize PDF
    p.showPage()
    p.save()

    # Prepare response
    buffer.seek(0)
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Pharmore_Receipt_{order.id}.pdf"'
    return response

@login_required
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'blog/list.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/create.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.user == post.author or request.user.is_staff:
        post.delete()
    return redirect('blog_list')

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('blog_list')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user.is_staff:
        comment.delete()
    return redirect('blog_detail', post_id=comment.post.id)

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comment_set.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})