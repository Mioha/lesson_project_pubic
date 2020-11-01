from django.db import models
from django.contrib.auth.models import AbstractUser


class LessonUser(AbstractUser):
    is_test = models.CharField(max_length=50)


class Lesson(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField()
    description = models.TextField()

    # def __str__(self):
    #     return self.name


class LessonLog(models.Model):
    user_id = models.ForeignKey(LessonUser, on_delete=models.CASCADE)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    start_ts = models.DateTimeField(auto_now_add=True)
    end_ts = models.DateTimeField(null=True, blank=True)

    INPROGRESS = 'In Progress'
    UNDERREVIEW = 'Under Review'
    APPROVED = 'Approved'
    NOTAPPROVED = 'Not Approved'
    STATUS_CHOICE = (
        (INPROGRESS, 'In Progress'),
        (UNDERREVIEW, 'Under Review'),
        (APPROVED, 'Approved'),
        (NOTAPPROVED, 'Not Approved'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICE,
                              default=INPROGRESS)
