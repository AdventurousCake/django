from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):  # or StackedInline
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # порядок полей
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]

    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

    # date_hierarchy = ...
    list_per_page = 10


admin.site.register(Question, QuestionAdmin)

# отдельно без инлайна
# admin.site.register(Choice)
