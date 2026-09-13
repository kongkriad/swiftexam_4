from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apis.models import School, Classroom, Teacher, Student


class BaseAPITestCase(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='tester', password='pass12345')
        self.client.force_authenticate(user=self.user)
        self.client.credentials(HTTP_ACCEPT='application/json')

        # Schools
        self.school_a = School.objects.create(
            name='Bangkok School', abbreviation='BKS', address='Bangkok'
        )
        self.school_b = School.objects.create(
            name='Chiang Mai School', abbreviation='CMS', address='Chiang Mai'
        )

        # Classrooms
        self.classroom_a1 = Classroom.objects.create(
            school=self.school_a, grade_level='ม.1', room_number='1'
        )
        self.classroom_a2 = Classroom.objects.create(
            school=self.school_a, grade_level='ม.1', room_number='2'
        )
        self.classroom_b1 = Classroom.objects.create(
            school=self.school_b, grade_level='ม.2', room_number='1'
        )

        # Teachers
        self.teacher_1 = Teacher.objects.create(
            first_name='Somchai', last_name='Jaidee', gender='M'
        )
        self.teacher_1.classrooms.set([self.classroom_a1, self.classroom_a2])

        self.teacher_2 = Teacher.objects.create(
            first_name='Malee', last_name='Suksri', gender='F'
        )
        self.teacher_2.classrooms.set([self.classroom_b1])

        # Students
        self.student_1 = Student.objects.create(
            first_name='Somsri', last_name='Rakdee', gender='F', classroom=self.classroom_a1
        )
        self.student_2 = Student.objects.create(
            first_name='Anan', last_name='Yindee', gender='M', classroom=self.classroom_a1
        )
        self.student_3 = Student.objects.create(
            first_name='Nid', last_name='Chaidee', gender='F', classroom=self.classroom_b1
        )


class AuthenticationTests(APITestCase):
    def test_anonymous_request_is_rejected(self):
        response = self.client.get('/api/v1/schools/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SchoolAPITests(BaseAPITestCase):
    def test_create_school(self):
        payload = {'name': 'Phuket School', 'abbreviation': 'PKS', 'address': 'Phuket'}
        response = self.client.post('/api/v1/schools/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 3)
        self.assertEqual(response.data['name'], 'Phuket School')

    def test_school_list(self):
        response = self.client.get('/api/v1/schools/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_school_list_filter_by_name(self):
        response = self.client.get('/api/v1/schools/', {'name': 'bangkok'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Bangkok School')

    def test_school_detail_includes_counts(self):
        response = self.client.get(f'/api/v1/schools/{self.school_a.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classroom_count'], 2)
        self.assertEqual(response.data['teacher_count'], 1)
        self.assertEqual(response.data['student_count'], 2)

    def test_school_detail_counts_for_school_with_no_children(self):
        empty_school = School.objects.create(name='Empty School')
        response = self.client.get(f'/api/v1/schools/{empty_school.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classroom_count'], 0)
        self.assertEqual(response.data['teacher_count'], 0)
        self.assertEqual(response.data['student_count'], 0)

    def test_update_school(self):
        response = self.client.patch(
            f'/api/v1/schools/{self.school_a.id}/', {'address': 'New Address'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school_a.refresh_from_db()
        self.assertEqual(self.school_a.address, 'New Address')

    def test_delete_school(self):
        response = self.client.delete(f'/api/v1/schools/{self.school_a.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(School.objects.filter(id=self.school_a.id).exists())


class ClassroomAPITests(BaseAPITestCase):
    def test_create_classroom(self):
        payload = {'school': self.school_b.id, 'grade_level': 'ม.3', 'room_number': '1'}
        response = self.client.post('/api/v1/classrooms/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classroom.objects.count(), 4)

    def test_classroom_list(self):
        response = self.client.get('/api/v1/classrooms/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_classroom_list_filter_by_school(self):
        response = self.client.get('/api/v1/classrooms/', {'school': self.school_a.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {row['id'] for row in response.data}
        self.assertEqual(ids, {self.classroom_a1.id, self.classroom_a2.id})

    def test_classroom_detail_includes_teachers_and_students(self):
        response = self.client.get(f'/api/v1/classrooms/{self.classroom_a1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        teacher_ids = {row['id'] for row in response.data['teachers']}
        student_ids = {row['id'] for row in response.data['students']}
        self.assertEqual(teacher_ids, {self.teacher_1.id})
        self.assertEqual(student_ids, {self.student_1.id, self.student_2.id})

    def test_update_classroom(self):
        response = self.client.patch(
            f'/api/v1/classrooms/{self.classroom_a1.id}/', {'room_number': '9'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.classroom_a1.refresh_from_db()
        self.assertEqual(self.classroom_a1.room_number, '9')

    def test_delete_classroom(self):
        response = self.client.delete(f'/api/v1/classrooms/{self.classroom_b1.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Classroom.objects.filter(id=self.classroom_b1.id).exists())


class TeacherAPITests(BaseAPITestCase):
    def test_create_teacher(self):
        payload = {
            'first_name': 'Prasert',
            'last_name': 'Wongsa',
            'gender': 'M',
            'classrooms': [self.classroom_a1.id],
        }
        response = self.client.post('/api/v1/teachers/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 3)

    def test_teacher_list(self):
        response = self.client.get('/api/v1/teachers/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_teacher_list_filter_by_school(self):
        response = self.client.get('/api/v1/teachers/', {'school': self.school_a.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {row['id'] for row in response.data}
        self.assertEqual(ids, {self.teacher_1.id})

    def test_teacher_list_filter_by_classroom(self):
        response = self.client.get('/api/v1/teachers/', {'classroom': self.classroom_b1.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {row['id'] for row in response.data}
        self.assertEqual(ids, {self.teacher_2.id})

    def test_teacher_list_filter_by_firstname(self):
        response = self.client.get('/api/v1/teachers/', {'firstname': 'som'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.teacher_1.id)

    def test_teacher_list_filter_by_lastname(self):
        response = self.client.get('/api/v1/teachers/', {'lastname': 'suksri'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.teacher_2.id)

    def test_teacher_list_filter_by_gender(self):
        response = self.client.get('/api/v1/teachers/', {'gender': 'F'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {row['id'] for row in response.data}
        self.assertEqual(ids, {self.teacher_2.id})

    def test_teacher_detail_includes_classrooms(self):
        response = self.client.get(f'/api/v1/teachers/{self.teacher_1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        classroom_ids = {row['id'] for row in response.data['classrooms']}
        self.assertEqual(classroom_ids, {self.classroom_a1.id, self.classroom_a2.id})

    def test_update_teacher(self):
        response = self.client.patch(
            f'/api/v1/teachers/{self.teacher_1.id}/',
            {'classrooms': [self.classroom_b1.id]},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher_1.refresh_from_db()
        self.assertEqual(
            set(self.teacher_1.classrooms.values_list('id', flat=True)),
            {self.classroom_b1.id},
        )

    def test_delete_teacher(self):
        response = self.client.delete(f'/api/v1/teachers/{self.teacher_1.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Teacher.objects.filter(id=self.teacher_1.id).exists())


class StudentAPITests(BaseAPITestCase):
    def test_create_student(self):
        payload = {
            'first_name': 'Kanya',
            'last_name': 'Meechai',
            'gender': 'F',
            'classroom': self.classroom_b1.id,
        }
        response = self.client.post('/api/v1/students/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 4)

    def test_student_list(self):
        response = self.client.get('/api/v1/students/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_student_list_filter_by_school(self):
        response = self.client.get('/api/v1/students/', {'school': self.school_a.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {row['id'] for row in response.data}
        self.assertEqual(ids, {self.student_1.id, self.student_2.id})

    def test_student_list_filter_by_classroom(self):
        response = self.client.get('/api/v1/students/', {'classroom': self.classroom_b1.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {row['id'] for row in response.data}
        self.assertEqual(ids, {self.student_3.id})

    def test_student_list_filter_by_firstname(self):
        response = self.client.get('/api/v1/students/', {'firstname': 'som'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.student_1.id)

    def test_student_list_filter_by_lastname(self):
        response = self.client.get('/api/v1/students/', {'lastname': 'yindee'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.student_2.id)

    def test_student_list_filter_by_gender(self):
        response = self.client.get('/api/v1/students/', {'gender': 'F'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {row['id'] for row in response.data}
        self.assertEqual(ids, {self.student_1.id, self.student_3.id})

    def test_student_list_filter_combined(self):
        response = self.client.get(
            '/api/v1/students/', {'classroom': self.classroom_a1.id, 'gender': 'F'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {row['id'] for row in response.data}
        self.assertEqual(ids, {self.student_1.id})

    def test_student_detail_includes_classroom(self):
        response = self.client.get(f'/api/v1/students/{self.student_1.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classroom']['id'], self.classroom_a1.id)
        self.assertEqual(response.data['classroom']['school'], self.school_a.id)

    def test_update_student(self):
        response = self.client.patch(
            f'/api/v1/students/{self.student_1.id}/',
            {'classroom': self.classroom_b1.id},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student_1.refresh_from_db()
        self.assertEqual(self.student_1.classroom_id, self.classroom_b1.id)

    def test_delete_student(self):
        response = self.client.delete(f'/api/v1/students/{self.student_1.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(id=self.student_1.id).exists())

# Create your tests here.
