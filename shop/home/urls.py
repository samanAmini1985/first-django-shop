from django.urls import path, include
from . import views

app_name = 'home'

url_bucket = [
    path('', views.BucketHome.as_view(), name='bucket'),
    path('delete_obj/<str:key>/', views.DeleteBucketObject.as_view(), name='delete_obj_bucket'),
    path('download_obj/<str:key>/', views.DownloadBucketObject.as_view(), name='download_obj_bucket'),
]
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('category/<slug:category_slug>/', views.HomeView.as_view(), name='category_filter'),
    path('bucket/', include(url_bucket)),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]
