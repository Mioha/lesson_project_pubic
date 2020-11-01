from django.db import migrations
from lesson.models import LessonLog, LessonUser, Lesson
from django.contrib.auth.models import Group


# make admin group
def add_default_groups(apps, schema_editor):
    Group.objects.create(name='admin')


def create_default_user(apps, schema_editor):
    """
    build the user you now have access to via Django magic
    :param apps:
    :param schema_editor:
    :return:
    """
    a = LessonUser.objects.create_user(username='admin', password='12345abcde')
    LessonUser.objects.create_superuser(username='mm', email='',
                                        password='12345abcde')
    adm_group = Group.objects.get(name='admin')
    adm_group.user_set.add(a)


def create_lessons(apps, schema_editor):
    Lesson.objects.bulk_create(
        [Lesson(name="レッスンテスト", number=1, description="あいうえお"),
         Lesson(name="バレーレッスン", number=2, description="テストのレッスン"),
         Lesson(name="レッスン", number=3, description="これはテストです")
         ]
    )


def create_lessonlogs(apps, schema_editor):
    LessonUser.objects.bulk_create(
        [LessonUser(username='user1', password='12345abcde'),
         LessonUser(username='user2', password='12345abcde'),
         LessonUser(username='user3', password='12345abcde')
         ]
    )

    lesson1 = Lesson.objects.get(pk=1)
    lesson2 = Lesson.objects.get(pk=2)
    user1 = LessonUser.objects.get(username='user1')
    user2 = LessonUser.objects.get(username='user2')

    LessonLog.objects.bulk_create(
        [LessonLog(user_id=user1, lesson_id=lesson1),
         LessonLog(user_id=user1, lesson_id=lesson2,
                   status=LessonLog.UNDERREVIEW),
         LessonLog(user_id=user2, lesson_id=lesson1, status=LessonLog.APPROVED),
         LessonLog(user_id=user2, lesson_id=lesson2,
                   status=LessonLog.NOTAPPROVED)
         ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ('lesson', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(add_default_groups),
        migrations.RunPython(create_default_user),
        migrations.RunPython(create_lessons),
        migrations.RunPython(create_lessonlogs)
    ]
