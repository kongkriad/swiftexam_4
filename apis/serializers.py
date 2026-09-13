from rest_framework import serializers

from apis.models import School,Classroom,Teacher,Student

class TeacherSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender']


class StudentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender']


class ClassroomSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'year', 'room']

# ---------- School ----------

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
            'classroom_count', 'teacher_count', 'student_count'
        ]

    def get_classroom_count(self, obj):
        return obj.classrooms.count()

    def get_teacher_count(self, obj):
        # นับครูที่สอนในห้องเรียนของโรงเรียนนี้ (ไม่ซ้ำ)
        return Teacher.objects.filter(classrooms__school=obj).distinct().count()

    def get_student_count(self, obj):
        return Student.objects.filter(classroom__school=obj).count()


# ---------- Classroom ----------

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'school', 'year', 'room']


class ClassroomDetailSerializer(serializers.ModelSerializer):
    teachers = TeacherSimpleSerializer(many=True, read_only=True)
    students = StudentSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'school', 'year', 'room', 'teachers', 'students']


# ---------- Teacher ----------

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'classrooms']


class TeacherDetailSerializer(serializers.ModelSerializer):
    classrooms = ClassroomSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'gender', 'classrooms']


# ---------- Student ----------

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'classroom']


class StudentDetailSerializer(serializers.ModelSerializer):
    classroom = ClassroomSimpleSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'classroom']
# code here
