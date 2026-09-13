from django.db import models

class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class School(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='ชื่อโรงเรียน'
    )

    abbreviation = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='ตัวย่อชื่อโรงเรียน'
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='ที่อยู่'
    )

    def __str__(self):
        return self.name

class Classroom(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='classrooms'
    )

    grade_level = models.CharField(
        max_length=5,
        verbose_name='ชั้นปี'
    )

    room_number = models.CharField(
        max_length=10,
        verbose_name='ห้อง'
    )

    class Meta:
        unique_together = ('school', 'grade_level', 'room_number')
        ordering = ['school', 'grade_level', 'room_number']

    def __str__(self):
        return f'{self.grade_level}/{self.room_number} ({self.school.name})'

class Teacher(models.Model):
    first_name = models.CharField(
        max_length=150,
        verbose_name='ชื่อ'
    )

    last_name = models.CharField(
        max_length=150,
        verbose_name='นามสกุล'
    )

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name='เพศ'
    )

    classrooms = models.ManyToManyField(
        Classroom,
        related_name='teachers',
        blank=True,
        verbose_name='ห้องเรียน'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Student(models.Model):
    first_name = models.CharField(
        max_length=150,
        verbose_name='ชื่อ'
    )

    last_name = models.CharField(
        max_length=150,
        verbose_name='นามสกุล'
    )

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name='เพศ'
    )

    classroom = models.ForeignKey(
        Classroom,
        related_name='students',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='ห้องเรียน'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Create your models here.
