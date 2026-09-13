from rest_framework import viewsets

from apis.models import School
from apis.serializers import SchoolSerializer, SchoolDetailSerializer
from apis.filters import SchoolFilter


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolDetailSerializer
        return SchoolSerializer
