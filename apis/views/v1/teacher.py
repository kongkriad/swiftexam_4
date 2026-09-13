from rest_framework import viewsets

from apis.models import Teacher
from apis.serializers import TeacherSerializer,TeacherDetailSerializer
from apis.filters import TeacherFilter

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all().distinct()
    serializer_class = TeacherSerializer
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeacherDetailSerializer
        return TeacherSerializer
