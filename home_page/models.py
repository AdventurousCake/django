# from django.conf import settings
from django.db import models
from core.models import User
# from django.utils import timezone
#
#
# class BotUser(models.Model):
#     # NEED MIGRATION
#     # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     id = models.IntegerField(unique=True, primary_key=True)
#     id_user = models.IntegerField()
#     name = models.CharField(max_length=100)
#     data = models.TextField()
#     created_date = models.DateTimeField(null=True)
#
#     # def publish(self):
#     #     self.published_date = timezone.now()
#     #     self.save()
#
#     class Meta:
#         ordering = ('id',)
#
#     def __str__(self):
#         return 'USER'+self.name


class Message(models.Model):
    # NEED MIGRATION
    author = models.ForeignKey(to=User, related_name='messages', on_delete=models.CASCADE)
    id = models.IntegerField(null=False, unique=True, primary_key=True, max_length=10)  # limit int
    name = models.CharField(null=False, max_length=10)
    text = models.TextField(null=False, max_length=100)
    created_date = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.text}"
