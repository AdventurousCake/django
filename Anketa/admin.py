from django.contrib import admin

from django.contrib import admin

from .forms import UserAdminForm
from .models import UserAccount, UserAnketa


@admin.register(UserAccount)
class UserAccount2Admin(admin.ModelAdmin):
    list_display = ('uid', 'username', 'first_name', 'user_type', 'user_anketa_status', 'user_anketa_data', 'created_date')

    form = UserAdminForm


admin.site.register(UserAnketa)

# @admin.register(UserAccount)
# class UserAccount2Admin(admin.ModelAdmin):
#     list_display = ('uid', 'username', 'first_name', 'user_type', 'user_anketa_status', 'user_anketa_data', 'created_date')
    # list_display = [field.name for field in UserAccount._meta.get_fields()]
    # exclude = ""
    # search_fields = ('title', 'text', 'author')
