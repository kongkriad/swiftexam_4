from django_filters import FilterSet, filters

from apis.models import School,Classroom,Teacher,Student

class SchoolFilter(FilterSet):
    name = filter.CharFilter(field_name='name',lookup_expr='icontains')

    class Meta:
        model = School
        fields = ['name']

class ClassroomFilter(FilterSet):
    School = filter.NumberFilter(field_name='school_id')

    class Meta:
        model = Classroom
        fields = ['school']

class TeacherFilter(FilterSet):
    school = filters.NumberFilter(field_name='classrooms__school_id', distinct=True)
    classroom = filters.NumberFilter(field_name='classrooms__id', distinct=True)
    firstname = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    lastname = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = filters.CharFilter(field_name='gender')

    class Meta:
        model = Teacher
        fields = ['school', 'classroom', 'firstname', 'lastname', 'gender']


class StudentFilter(FilterSet):
    school = filters.NumberFilter(field_name='classroom__school_id')
    classroom = filters.NumberFilter(field_name='classroom_id')
    firstname = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    lastname = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    gender = filters.CharFilter(field_name='gender')

    class Meta:
        model = Student
        fields = ['school', 'classroom', 'firstname', 'lastname', 'gender']

# code here
