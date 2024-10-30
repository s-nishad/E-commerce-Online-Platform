from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('create/', views.create_product_view, name='create_product'),
    path('all_products/', views.get_all_product_view, name='all_products'),
    path('<str:guid>/', views.product_by_guid, name='product_by_guid'),
    path('<str:guid>/update/', views.update_product_view, name='update_product'),
    path('<str:guid>/delete/', views.delete_product_view, name='delete_product'),
    path('stocks/<str:guid>/update', views.create_stock_view, name='product_stocks_update'),
]
