from rest_framework import serializers

from apis.models import (
    School,
    Classroom,
    Teacher,
    Student,
)


# =========================================================
# Classroom Mini Serializer
# =========================================================

class ClassroomMiniSerializer(serializers.ModelSerializer):
    school_name = serializers.CharField(
        source='school.name',
        read_only=True
    )

    class Meta:
        model = Classroom
        fields = [
            'id',
            'school',
            'school_name',
            'grade_level',
            'room_number',
        ]


# =========================================================
# Teacher Mini Serializer
# =========================================================

class TeacherMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
        ]


# =========================================================
# Student Mini Serializer
# =========================================================

class StudentMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
        ]


# =========================================================
# School Serializer
# =========================================================

class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = [
            'id',
            'name',
            'abbreviation',
            'address',
        ]


# =========================================================
# School Detail Serializer
# =========================================================

class SchoolDetailSerializer(serializers.ModelSerializer):
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = [
            'id',
            'name',
            'abbreviation',
            'address',
            'classroom_count',
            'teacher_count',
            'student_count',
        ]

    def get_classroom_count(self, obj):
        return obj.classrooms.count()

    def get_teacher_count(self, obj):
        return Teacher.objects.filter(
            classrooms__school=obj
        ).distinct().count()

    def get_student_count(self, obj):
        return Student.objects.filter(
            classroom__school=obj
        ).count()


# =========================================================
# Classroom Serializer
# =========================================================

class ClassroomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classroom
        fields = [
            'id',
            'school',
            'grade_level',
            'room_number',
        ]


# =========================================================
# Classroom Detail Serializer
# =========================================================

class ClassroomDetailSerializer(serializers.ModelSerializer):
    teachers = TeacherMiniSerializer(
        many=True,
        read_only=True
    )

    students = StudentMiniSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Classroom
        fields = [
            'id',
            'school',
            'grade_level',
            'room_number',
            'teachers',
            'students',
        ]


# =========================================================
# Teacher Serializer
# =========================================================

class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'classrooms',
        ]


# =========================================================
# Teacher Detail Serializer
# =========================================================

class TeacherDetailSerializer(serializers.ModelSerializer):
    classrooms = ClassroomMiniSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Teacher
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'classrooms',
        ]


# =========================================================
# Student Serializer
# =========================================================

class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'classroom',
        ]


# =========================================================
# Student Detail Serializer
# =========================================================

class StudentDetailSerializer(serializers.ModelSerializer):
    classroom = ClassroomMiniSerializer(
        read_only=True
    )

    class Meta:
        model = Student
        fields = [
            'id',
            'first_name',
            'last_name',
            'gender',
            'classroom',
        ]

# code here
