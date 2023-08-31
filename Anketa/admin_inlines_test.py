from django.contrib import admin

from .forms import UserAdminForm
from .models import UserAccount, UserAnketa


class ListInline(admin.TabularInline):
    model = UserAccount.user_anketa_list.through
    extra = 1


# class AnketaInline(admin.StackedInline):
#     model = UserAnketa
#     extra = 0

# class AnketaInline(admin.StackedInline):
#     model = UserAnketa
#     extra = 0


@admin.register(UserAccount)
class UserAccount2Admin(admin.ModelAdmin):
    list_display = ('uid', 'username', 'first_name', 'user_type', 'user_anketa_status', 'user_anketa_data', 'created_date')

    form = UserAdminForm

    inlines = ListInline,
    # exclude = ['user_anketa_list']


@admin.register(UserAnketa)
class UserAnketaAdmin(admin.ModelAdmin):
    list_display = ('id', 'data')
    inlines = ListInline,


# admin.site.register(UserAnketa)


# @admin.register(UserAccount)
# class UserAccount2Admin(admin.ModelAdmin):
#     list_display = ('uid', 'username', 'first_name', 'user_type', 'user_anketa_status', 'user_anketa_data', 'created_date')
    # list_display = [field.name for field in UserAccount._meta.get_fields()]
    # exclude = ""
    # search_fields = ('title', 'text', 'author')
