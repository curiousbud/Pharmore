from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='user_register'),
    path('update_stock/<int:item_id>/', views.update_stock, name='update_stock'),
    path('order/<int:order_id>/download/', views.download_receipt, name='download_receipt'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('blog/comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.create_post, name='create_post'),
    path('blog/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('blog/like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('order/<int:order_id>/download/', views.download_receipt, name='download_receipt'),
    path('admin/register/', views.admin_register, name='admin_register'),
    path('items/', views.item_list, name='item_list'),
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('manage_items/', views.manage_items, name='manage_items'),
    path('add_item/', views.add_item, name='add_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]