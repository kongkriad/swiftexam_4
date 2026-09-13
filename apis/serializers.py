from rest_framework import serializers

from apis.models import School,Classroom,Teacher,Student

class ClassroomMiniSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model =Classroom
        fields = ['id', 'school', 'school_name', 'grade_level', 'room_number']

class TeacherMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender']

class StudentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name', 'abbreviation', 'address']

class SchoolDetailSerializer(serializers.ModelSerializer):
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = [
            'id', 'name', 'abbreviation', 'address',
            'classroom_count', 'teacher_count', 'student_count',
        ]

    def get_classroom_count(self, obj):
        return obj.classrooms.count()

    def get_teacher_count(self, obj):
        return Teacher.objects.filter(classrooms__school=obj).distinct().count()

    def get_student_count(self, obj):
        return Student.objects.filter(classroom__school=obj).count()

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'school', 'grade_level', 'room_number']

class ClassroomDetailSerializer(serializers.ModelSerializer):
    teachers = TeacherMiniSerializer(many=True, read_only=True)
    students = StudentMiniSerializer(many=True, read_only=True)

    class Meta:
        modl = Classroom
        fields = ['id', 'school', 'grade_level', 'room_number', 'teachers', 'students']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'classrooms']

class TeacherDetailSerializer(serializers.ModelSerializer):
        classrooms = ClassroomMiniSerializer(many=True, read_only=True)

        class Meta:
            model = Teacher
            fields = ['id', 'first_name', 'last_name', 'gender', 'classrooms']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'classroom']

class StudentDetailSerializer(serializers.ModelSerializer):
    classroom = ClassroomMiniSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'classroom']
# code here
