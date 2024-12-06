from django.contrib import admin
from .models import Question, Choice, Vote  # Ensure you import Vote

admin.site.site_header = "Pollster Admin"
admin.site.site_title = "Pollster Admin Area"
admin.site.index_title = "Welcome to the Pollster admin area"

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Election Status', {'fields': ['is_open']})  # Adding the election status field to the admin
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'is_open')  # Make sure to display is_open status
    actions = ['close_election']

    def close_election(self, request, queryset):
        queryset.update(is_open=False)
    close_election.short_description = "Mark selected elections as closed"

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
