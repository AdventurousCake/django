from django.db import models
from django.utils import timezone


class SettingsSearchViewEnum(models.TextChoices):
    FULL = 'FULL'
    COMPACT = 'COMPACT'
    COMPACT2 = 'COMPACT2'
    CUSTOM1 = 'CUSTOM1'


class UserStatus(models.TextChoices):
    SOLVED = 'Решено'
    ACTIVE = 'Активно'
    IN_PROCESS = 'В процессе'
    REJECTED = 'Отклонено'


# o2m
class UserAnketa(models.Model):
    pass


class UserAccount(models.Model):
    uid = models.BigIntegerField(primary_key=True, unique=True, null=False, auto_created=False)
    username = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255, blank=True)

    country = models.CharField(max_length=255, blank=True)
    # city = models.CharField(max_length=255, blank=True)
    # state = models.CharField(max_length=255, blank=True)
    # street = models.CharField(max_length=255, blank=True)

    email = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)

    user_anketa_status = models.CharField(choices=UserStatus, default=UserStatus.ACTIVE)
    user_anketa_data = models.CharField(max_length=255, default=None)

    settings = models.CharField(max_length=50, blank=True, default=None)
    created_date = models.DateTimeField(default=timezone.now, blank=True)
    updated_date = models.DateTimeField(default=timezone.now, blank=True)

    # is_premium = models.BooleanField(blank=True, null=True)
    # raw_data = models.TextField(blank=True)

    # def upd(self):
    #     self.upd_date = timezone.now()
    #     self.save()

    def __str__(self):
        return f"<{self.uid}, {self.first_name}>"
        # return "__all__" #notw

    class Meta:
        ordering = ['-created_date']
        db_table = "UserAccount"