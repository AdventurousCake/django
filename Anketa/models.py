from django.db import models
from django.forms import Textarea
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _


# class SettingsSearchViewEnum(models.TextChoices):
#     FULL = 'FULL'
#     COMPACT = 'COMPACT'
#     COMPACT2 = 'COMPACT2'
#     CUSTOM1 = 'CUSTOM1'


class UserStatus(models.TextChoices):
    SOLVED = 'SOLVED', _('Решено')
    ACTIVE = 'ACTIVE', _('Активно')
    IN_PROCESS = 'IN_PROCESS', _('В процессе')
    REJECTED = 'REJECTED', _('Отклонено')


class UserType(models.TextChoices):
    PRIVATE = 'PRIVATE', _('Частное')
    LEGAL_ENTITY = 'LEGAL_ENTITY', _('Юр. лицо')


# m2m
class UserAnketa(models.Model):
    data = models.CharField(max_length=255, blank=True)


class UserAccount(models.Model):
    class Meta:
        ordering = ['-created_date']
        db_table = "UserAccount"
        verbose_name_plural = "Пользователи и заявки"
        verbose_name = "Пользователи и заявки"


    uid = models.BigIntegerField(primary_key=True, unique=True, null=False, auto_created=False)
    username = models.CharField(max_length=255, blank=True)

    first_name = models.CharField(max_length=255, blank=False, verbose_name="Имя")
    last_name = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    # state = models.CharField(max_length=255, blank=True)
    # street = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)

    # MAIN LOGIC
    user_type = models.CharField(choices=UserType.choices, max_length=50, default=UserType.PRIVATE, verbose_name="Тип заявки")
    user_anketa_status = models.CharField(choices=UserStatus.choices, max_length=50, default=UserStatus.ACTIVE, verbose_name="Статус заявки")
    user_anketa_data = models.CharField(max_length=4096, default=None, blank=False, verbose_name="Текст заявки",)
    # user_anketa_data = models.TextField(max_length=4096, default=None, blank=False, verbose_name="Текст заявки")

    user_anketa_list = models.ManyToManyField(to=UserAnketa)

    # settings = models.CharField(max_length=50, blank=True, default=None)
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
