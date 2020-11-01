from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.utils import timezone
from django.db.models import Q

from .models import LessonLog, LessonUser, Lesson
from .serializers import LessonLogSerializer, LessonUserSerializer, \
    LessonUserSerializerMini, LessonSerializer

from django.contrib.auth import get_user_model  # If custom user model used

from .serializers import UserSerializer
from .permissions import AdminOnly


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny]
    model = get_user_model()
    serializer_class = UserSerializer


class IsAdminViewSet(APIView):
    def get(self, request):
        resp = {'is_admin': False, 'user_id': request.user.id,
                'username': request.user.username}
        if request.user.groups.filter(name='admin').exists():
            resp['is_admin'] = True
        return Response(resp,
                        status=status.HTTP_200_OK)


class LessonLogViewSet(APIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        queryset = LessonLog.objects.all().order_by('user_id', 'lesson_id')
        serializer = LessonLogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileViewSet(APIView):
    def get(self, request):
        queryset = LessonLog.objects.filter(user_id=request.user.id).order_by(
            'lesson_id')
        serializer = LessonLogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonAllViewSet(APIView):
    def get(self, request):
        all_lesson = Lesson.objects.all()
        serializer = LessonSerializer(all_lesson, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class LessonListViewSet(APIView):

    def get(self, request):
        all_lesson = Lesson.objects.all()

        def makelog(l):
            lessonlog = LessonLog.objects.filter(user_id=request.user,
                                                 lesson_id=l.id).first()
            return {'lesson': LessonSerializer(l).data,
                    'lessonlog': LessonLogSerializer(lessonlog).data}

        resp = list(map(makelog, all_lesson))
        return Response(resp,
                        status=status.HTTP_200_OK)


class LessonDetailViewSet(APIView):

    def get(self, request, lesson_id):
        lessonlog = LessonLog.objects.filter(user_id=request.user,
                                             lesson_id=lesson_id).first()
        lesson = Lesson.objects.filter(pk=lesson_id).first()
        response_data = {'lesson': LessonSerializer(lesson).data,
                         'lessonlog': LessonLogSerializer(lessonlog).data,
                         }
        return Response(response_data, status=status.HTTP_200_OK)


class LessonDetailAdminViewSet(APIView):
    permission_classes = [AdminOnly]

    def get(self, request, lesson_id):
        lessonlog = LessonLog.objects.filter(
            lesson_id=lesson_id).order_by('user_id')
        serializer = LessonLogSerializer(lessonlog, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, lesson_id):
        lesson = Lesson.objects.get(pk=lesson_id)
        serializer = LessonSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewLessonViewSet(APIView):
    permission_classes = [AdminOnly]

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartLessonViewSet(APIView):

    def post(self, request, lesson_id):
        # check if the same user_id and lesson_id combination exists on lessonlog to accept post
        is_lessonlog = LessonLog.objects.filter(
            lesson_id=lesson_id,
            user_id=request.user).exists()
        data = {
            "user_id": request.user.id,
            "lesson_id": lesson_id
        }
        serializer = LessonLogSerializer(data=data)
        if serializer.is_valid() and not is_lessonlog:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteLessonViewSet(APIView):

    def put(self, request, lesson_id):
        # filtering user_id, lesson_id, status is INPROGRESS or NOTAPPROVED
        lessonlog = LessonLog.objects.filter(
            Q(user_id=request.user),
            Q(lesson_id=lesson_id),
            Q(status=LessonLog.INPROGRESS) | Q(status=LessonLog.NOTAPPROVED)
        ).first()
        if not lessonlog:
            error_result = 'user id %s and lesson id %s is not found in lesson log or the status is not %s or %s' % \
                           (request.user, lesson_id,
                            LessonLog.INPROGRESS, LessonLog.NOTAPPROVED)
            return Response(error_result,
                            status=status.HTTP_400_BAD_REQUEST)
        lessonlog.status = LessonLog.UNDERREVIEW
        data = {
            "user_id": request.user.id,
            "lesson_id": lesson_id
        }
        serializer = LessonLogSerializer(lessonlog, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListViewSet(APIView):
    permission_classes = [AdminOnly]

    def get(self, request):
        queryset = LessonLog.objects.filter(status=LessonLog.UNDERREVIEW)
        serializer = LessonLogSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApproveRejectViewSet(APIView):
    permission_classes = [AdminOnly]

    def put(self, request, change_status):
        lessonlog = LessonLog.objects.filter(user_id=request.data[
            'user_id'], lesson_id=request.data['lesson_id'],
                                             status=LessonLog.UNDERREVIEW).first()
        if not lessonlog:
            error_result = 'user id %s and lesson id %s is not found in lesson log or the status is not %s' % \
                           (request.data['user_id'], request.data['lesson_id'],
                            LessonLog.UNDERREVIEW)
            return Response(error_result,
                            status=status.HTTP_400_BAD_REQUEST)

        if change_status == 'approve':
            lessonlog.end_ts = timezone.now()
            lessonlog.status = LessonLog.APPROVED
        elif change_status == 'reject':
            lessonlog.status = LessonLog.NOTAPPROVED
        else:
            return Response('status should be approve or reject',
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = LessonLogSerializer(lessonlog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

