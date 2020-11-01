from django.contrib import admin
from .models import LessonUser, Lesson, LessonLog


class LessonAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonUser)
admin.site.register(LessonLog)
