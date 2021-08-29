from django.conf import settings
from django.db import models
from django.utils import timezone


class BotUser(models.Model):
    # NEED MIGRATION
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.IntegerField(unique=True, primary_key=True)
    id_user = models.IntegerField()
    name = models.CharField(max_length=100)
    data = models.TextField()
    created_date = models.DateTimeField(null=True)

    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return 'USER'+self.name