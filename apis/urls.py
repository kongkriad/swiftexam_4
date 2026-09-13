from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apis.views.v1 import(
    SchoolViewSet,
    ClassroomViewSet,
    TeacherViewSet,
    StudentViewSet,
)
router = DefaultRouter()
router.register('schools',SchoolViewSet,basename='school')
router.register('classrooms',ClassroomViewSet,basename='classroom')
router.register('teachers',TeacherViewSet,basename='teacher')
router.register('students',StudentViewSet,basename='student')

api_v1_urls = (router.urls, 'v1')

urlpatterns = [
    path('v1/', include(api_v1_urls))
]
