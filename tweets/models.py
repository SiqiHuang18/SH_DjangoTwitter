from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now
# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        ordering = ('user', '-created_at')

    @property
    def hours_to_now(self):
        # datetime.now has no time zone , need to add utc time
        return (utc_now() - self.created_at).seconds // 3600

    def __str__(self):
        # print(tweet instance) content
        return f'{self.created_at} {self.user}: {self.content}'