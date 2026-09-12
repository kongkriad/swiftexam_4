from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

api_v1_urls = (router.urls, 'v1')

urlpatterns = [
    path('v1/', include(api_v1_urls))
]
