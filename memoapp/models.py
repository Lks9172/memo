from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class Memos(models.Model):
    name_id = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length=50, db_column='제목')
    text = models.TextField(max_length=150, db_column='내용', help_text="메모 내용은 150자 이내로 입력가능합니다.")
    update_date = models.DateTimeField(auto_now=True)
    priority = models.BooleanField(db_column='중요도')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    @property
    def total_likes(self):
        return self.likes.count()  # likes 컬럼의 값의 갯수를 센다

    def generate(self):
        update_date = timezone.now()
        self.save()

    def __str__(self):
        return '%s by %s' %(self.name_id, self.title)