from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .  import views


router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register ('carts', views.CartViewSet)
router.register ('customers', views.CustomerViewSet)
router.register ('orders', views.OrderViewset, basename='orders')


products_router = routers.NestedSimpleRouter(router, 'products' , lookup='product')
products_router.register('reviews',views.ReviewViewSet , basename='product-reviews' )

cart_router = routers.NestedDefaultRouter(router, 'carts' , lookup='cart') #once we set to 'cart' we have a 
#lookup parameter= cart_pk that how we extracted it in CartitemViewSet metho get_queryset
cart_router.register('items', views.CartItemViewset, basename='cart-items')


urlpatterns = router.urls + products_router.urls + cart_router.urls







 

# urlpatterns = [ 
    
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view() , name='collection-detail'),
#     path('collections/', views.CollectionList.as_view())
# ] 