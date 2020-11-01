from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from unittest import skip

# import models
from lesson.models import LessonLog, LessonUser, Lesson

# import serializers
from lesson.serializers import LessonLogSerializer, LessonUserSerializer, \
    LessonUserSerializerMini, LessonSerializer

from rest_framework import status
from rest_framework.test import APITestCase


def create_default_user():
    return LessonUser.objects.create_user(username='testuser', password='12345')


def create_admin_user():
    a = LessonUser.objects.create_user(username='admin_test', password='12345')
    adm_group = Group.objects.get(name='admin')
    adm_group.user_set.add(a)
    return a


def create_lesson():
    Lesson.objects.bulk_create(
        [Lesson(name="レッスンテスト", number=1, description="レッスンだけ")
         ]
    )


class RegisterTest(APITestCase):

    def setUp(self):
        self.payload = {'username': 'testuser',
                        'password': '12345'}

    def test_user_can_register(self):
        # username and password is correct
        response1 = self.client.post(reverse('register'), self.payload)
        # username is already registered
        response2 = self.client.post(reverse('register'), self.payload)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.data['username'][0],
                         'A user with that username already exists.')


class LoginTest(APITestCase):

    def setUp(self):
        pass

    def test_user_can_login(self):
        testuser = create_default_user()
        # username and password is correct
        response1 = self.client.post(reverse('login'),
                                     {'username': testuser.username,
                                      'password': '12345'})
        # password is incorrect
        response2 = self.client.post(reverse('login'), {'username': 'testuser',
                                                        'password': '123'})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)


class IsAdminTest(APITestCase):

    def setUp(self):
        pass

    def test_basic_user_can_receive_is_admin_and_user_id(self):
        """
        Test that basic users can receive if the user is admin and user ID.
        """
        testuser = create_default_user()
        self.client.force_authenticate(user=testuser)
        expected = {'is_admin': False, 'user_id': testuser.id,
                    'username': testuser.username}
        response = self.client.get(reverse('is_admin'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)

    def test_admin_user_can_receive_is_admin_and_user_id(self):
        """
        Test that admin users can receive if the user is admin and user ID.
        """
        adminuser = create_admin_user()
        self.client.force_authenticate(user=adminuser)
        expected = {'is_admin': True, 'user_id': adminuser.id,
                    'username': adminuser.username}
        response = self.client.get(reverse('is_admin'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected)


class LessonLogTest(APITestCase):

    def setUp(self):
        pass

    def test_basic_user_cannot_see_lessonlog(self):
        """
        Test that basic users cannot access all users lesson logs.
        only visible to admin users.
        """
        testuser = create_default_user()
        self.client.force_authenticate(user=testuser)
        response = self.client.get(reverse('lessonlog'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_see_lessonlog(self):
        """
        Test that admin users can access all users lesson logs.
        """
        adminuser = create_admin_user()
        self.client.force_authenticate(user=adminuser)
        log = LessonLog.objects.all().order_by('user_id', 'lesson_id')
        serializer = LessonLogSerializer(log, many=True)
        response = self.client.get(reverse('lessonlog'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileTest(APITestCase):

    def setUp(self):
        pass

    def test_user_can_only_see_their_lesson_logs(self):
        """
        Test that user can only see their lesson logs.
        """
        user1 = LessonUser.objects.get(username='user1')
        self.client.force_authenticate(user=user1)
        response = self.client.get(reverse('profile'))
        queryset = LessonLog.objects.filter(user_id=user1.id).order_by(
            'lesson_id')
        serializer = LessonLogSerializer(queryset, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LessonAllTest(APITestCase):

    def setUp(self):
        pass

    def test_user_can_see_all_lessons(self):
        """
        Test that user can see all lessons.
        """
        testuser = create_default_user()
        self.client.force_authenticate(user=testuser)
        lesson = Lesson.objects.all()
        serializer = LessonSerializer(lesson, many=True)
        response = self.client.get(reverse('lessons_all'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LessonListTest(APITestCase):

    def setUp(self):
        pass

    def test_user_can_only_see_all_lessons_and_their_logs(self):
        """
        Test that user can only see all lessons info and their lesson logs.
        """
        user1 = LessonUser.objects.get(username='user1')
        self.client.force_authenticate(user=user1)
        all_lesson = Lesson.objects.all()

        def makelog(l):
            lessonlog = LessonLog.objects.filter(user_id=user1.id,
                                                 lesson_id=l.id).first()
            return {'lesson': LessonSerializer(l).data,
                    'lessonlog': LessonLogSerializer(lessonlog).data}

        resp = list(map(makelog, all_lesson))
        response = self.client.get(reverse('lessons'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, resp)


class LessonDetail(APITestCase):

    def setUp(self):
        pass

    def test_user_can_only_see_the_lesson_and_their_log(self):
        """
        Test that user can only see the lesson info and their lesson log.
        """
        user1 = LessonUser.objects.get(username='user1')
        self.client.force_authenticate(user=user1)
        valid_lesson = Lesson.objects.first()
        log = LessonLog.objects.filter(user_id=user1,
                                       lesson_id=valid_lesson).first()
        resp = {'lesson': LessonSerializer(valid_lesson).data,
                'lessonlog': LessonLogSerializer(log).data}
        response = self.client.get(
            reverse('lesson_detail', args=(valid_lesson.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, resp)


class LessonDetailAdminTest(APITestCase):

    def setUp(self):
        pass

    def test_basic_user_cannot_see_all_user_lessonlog(self):
        """
        Test that basic users cannot access all user lesson logs of the lesson
        only visible to admin users.
        """
        testuser = create_default_user()
        self.client.force_authenticate(user=testuser)
        valid_lesson = Lesson.objects.first()
        response = self.client.get(
            reverse('lessons_admin', args=(valid_lesson.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_see_lessonlog(self):
        """
        Test that admin users can access all user lesson logs of the lesson.
        """
        adminuser = create_admin_user()
        self.client.force_authenticate(user=adminuser)
        valid_lesson = Lesson.objects.first()
        lessonlog = LessonLog.objects.filter(
            lesson_id=valid_lesson).order_by('user_id')
        serializer = LessonLogSerializer(lessonlog, many=True)
        response = self.client.get(
            reverse('lessons_admin', args=(valid_lesson.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class LessonEditTest(APITestCase):

    def setUp(self):
        self.valid_lesson = Lesson.objects.first()
        self.payload = {
            'lesson_id': self.valid_lesson.id,
            'name': 'Mio lesson',
            'number': 1,
            'description': '7/1 test'
        }
        self.payload2 = {
            'lesson_id': self.valid_lesson.id,
            'name': 'Mio lesson',
            'number': 1,
        }
        self.expected = {
            'id': self.valid_lesson.id,
            'name': 'Mio lesson',
            'number': 1,
            'description': '7/1 test'
        }

    def test_basic_user_cannot_edit_lesson(self):
        """
        Test that basic users cannot edit lesson.
        """
        testuser = create_default_user()
        self.client.force_authenticate(user=testuser)
        response = self.client.put(
            reverse('lessons_admin', args=(self.valid_lesson.id,)),
            self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_edit_lesson(self):
        """
        Test that admin users can edit lesson.
        """
        adminuser = create_admin_user()
        self.client.force_authenticate(user=adminuser)
        # when payload is correct
        response = self.client.put(
            reverse('lessons_admin', args=(self.valid_lesson.id,)),
            self.payload)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, self.expected)
        # when payload is insufficient
        response = self.client.put(
            reverse('lessons_admin', args=(self.valid_lesson.id,)),
            self.payload2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class NewLessonTest(APITestCase):

    def setUp(self):
        self.payload = {
            'name': 'Mio lesson',
            'number': 1,
            'description': '7/1 test'
        }
        self.payload2 = {
            'name': 'Mio lesson',
            'number': 1
        }

    def test_basic_user_cannot_create_lesson(self):
        """
        Test that basic users cannot create lesson.
        """
        testuser = create_default_user()
        self.client.force_authenticate(user=testuser)
        response = self.client.post(
            reverse('lesson_new'), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_create_lesson(self):
        """
        Test that admin users can create lesson.
        """
        adminuser = create_admin_user()
        self.client.force_authenticate(user=adminuser)
        # when payload is correct
        response = self.client.post(
            reverse('lesson_new'), self.payload)
        expected = {
            'id': response.data['id'],
            'name': 'Mio lesson',
            'number': 1,
            'description': '7/1 test'
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected)
        # when payload is insufficient
        response = self.client.post(
            reverse('lesson_new'), self.payload2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StartLessonTest(APITestCase):

    def setUp(self):
        self.user1 = LessonUser.objects.get(username='user1')
        self.client.force_authenticate(user=self.user1)

    def test_user_cant_start_lesson_if_already_started(self):
        """
        Test that user cant start the lesson if there is already lesson log.
        """
        valid_log = LessonLog.objects.filter(user_id=self.user1).first()
        response = self.client.post(
            reverse('start', args=(valid_log.lesson_id.id,)))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_start_lesson(self):
        """
        Test that user can start the lesson if there is no lesson log.
        """
        create_lesson()
        valid_lesson = Lesson.objects.last()
        response = self.client.post(
            reverse('start', args=(valid_lesson.id,)))
        expected = {
            'end_ts': None,
            'status': 'In Progress',
            'user_id': {
                'id': self.user1.id,
                'username': self.user1.username
            },
            'lesson_id': {
                'id': valid_lesson.id,
                'name': valid_lesson.name,
                'number': valid_lesson.number,
                'description': valid_lesson.description
            }
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['end_ts'], expected['end_ts'])
        self.assertEqual(response.data['status'], expected['status'])
        self.assertEqual(response.data['user_id'], expected['user_id'])
        self.assertEqual(response.data['lesson_id'], expected['lesson_id'])


class CompleteLessonTest(APITestCase):

    def setUp(self):
        self.user1 = LessonUser.objects.get(username='user1')
        self.user2 = LessonUser.objects.get(username='user2')
        self.valid_log = LessonLog.objects.filter(user_id=self.user1).last()

    def test_user_cant_complete_lesson(self):
        """
        Test that user cant complete the lesson if the lesson log is Under Review or Approved.
        """
        under_review_log = LessonLog.objects.filter(user_id=self.user1.id,
                                                    status=LessonLog.UNDERREVIEW).first()
        approved_log = LessonLog.objects.filter(user_id=self.user2.id,
                                                status=LessonLog.APPROVED).first()

        # status = Under Review : users cannot complete lesson
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(
            reverse('comp', args=(under_review_log.lesson_id.id,)))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # status = Approved : users cannot complete lesson
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(
            reverse('comp', args=(approved_log.lesson_id.id,)))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # the lesson log doesn't exists : users cannot complete lesson
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(
            reverse('comp', args=(self.valid_log.lesson_id.id + 100,)))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_complete_lesson(self):
        """
        Test that user can complete the lesson
        if the lesson log is In Progress or Not Approved.
        """
        inprogress_log = LessonLog.objects.filter(user_id=self.user1.id,
                                                  status=LessonLog.INPROGRESS).first()
        not_approved_log = LessonLog.objects.filter(user_id=self.user2.id,
                                                    status=LessonLog.NOTAPPROVED).first()
        # status = In Progress : users can complete lesson
        self.client.force_authenticate(user=self.user1)
        response = self.client.put(
            reverse('comp', args=(inprogress_log.lesson_id.id,)))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['status'], LessonLog.UNDERREVIEW)

        # status = Not Approved : users can complete lesson
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(
            reverse('comp', args=(not_approved_log.lesson_id.id,)))
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['status'], LessonLog.UNDERREVIEW)


class ReviewListTest(APITestCase):

    def setUp(self):
        pass

    def test_basic_user_cannot_see_lessonlogs_for_review(self):
        """
        Test that basic users cannot see lesson logs for review.
        """
        testuser = create_default_user()
        self.client.force_authenticate(user=testuser)
        response = self.client.get(reverse('review'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_see_lessonlogs_for_review(self):
        """
        Test that admin users can see lesson logs for review.
        """
        adminuser = create_admin_user()
        self.client.force_authenticate(user=adminuser)
        log = LessonLog.objects.filter(status=LessonLog.UNDERREVIEW)
        serializer = LessonLogSerializer(log, many=True)
        response = self.client.get(reverse('review'))
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ApproveTest(APITestCase):

    def setUp(self):
        valid_log = LessonLog.objects.filter(pk=1).first()
        LessonLog.objects.filter(pk=1).update(status=LessonLog.UNDERREVIEW)
        self.payload = {
            'user_id': valid_log.user_id.id,
            'lesson_id': valid_log.lesson_id.id
        }
        self.status = 'approve'

    def test_basic_user_cannot_approve_lesson(self):
        """
        Test that basic users cannot approve lesson.
        """
        self.testuser = create_default_user()
        self.client.force_authenticate(user=self.testuser)
        response = self.client.put(
            reverse('approve_reject', args=(self.status,)), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_approve_lesson(self):
        """
        Test that admin users can approve lesson if the lesson log is Under Review.
        """
        adminuser = create_admin_user()
        self.client.force_authenticate(user=adminuser)
        # status = Under Review : users can approve lesson
        response = self.client.put(
            reverse('approve_reject', args=(self.status,)), self.payload)

        self.assertEqual(response.data['status'], LessonLog.APPROVED)
        self.assertNotEqual(response.data['end_ts'], None)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        # status = In Progress : users cannot approve lesson
        LessonLog.objects.filter(pk=1).update(status=LessonLog.INPROGRESS)
        response = self.client.put(
            reverse('approve_reject', args=(self.status,)), self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RejectTest(APITestCase):

    def setUp(self):
        valid_log = LessonLog.objects.filter(pk=1).first()
        LessonLog.objects.filter(pk=1).update(status=LessonLog.UNDERREVIEW)
        self.payload = {
            'user_id': valid_log.user_id.id,
            'lesson_id': valid_log.lesson_id.id
        }
        self.status = 'reject'

    def test_basic_user_cannot_reject_lesson(self):
        """
        Test that basic users cannot reject lesson.
        """
        testuser = create_default_user()
        self.client.force_authenticate(user=testuser)
        response = self.client.put(
            reverse('approve_reject', args=(self.status,)), self.payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_reject_lesson(self):
        """
        Test that admin users can reject lesson if the lesson log is Under Review.
        """
        adminuser = create_admin_user()
        self.client.force_authenticate(user=adminuser)
        # status = Under Review : users can reject lesson
        response = self.client.put(
            reverse('approve_reject', args=(self.status,)), self.payload)
        self.assertEqual(response.data['status'], LessonLog.NOTAPPROVED)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        # status = In Progress : users cannot reject lesson
        LessonLog.objects.filter(pk=1).update(status=LessonLog.INPROGRESS)
        response = self.client.put(
            reverse('approve_reject', args=(self.status,)), self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
