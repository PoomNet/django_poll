from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission

from polls.models import Poll, Question, Choice,Comment

admin.site.register(Permission)

class questioninline(admin.StackedInline):
    model = Question
    extra = 1

class choiceinline(admin.TabularInline):
    model = Choice
    extra = 1
class pollAdmin(admin.ModelAdmin):
    list_display = ['id','title','start_date','end_date','del_flag']
    list_per_page = 10
    list_filter = ['start_date','end_date','del_flag']
    search_fields = ['title']

    fieldsets = [
        (None,{'fields':['title','del_flag']}),
        ("Active",{'fields': ['start_date','end_date'],'classes':['collapse']})
    ]
    inlines = [questioninline]
class questionAdmin(admin.ModelAdmin):
    list_display = ['id','poll','text']
    list_per_page = 10
    list_filter = ['poll']
    search_fields = ['text']

    inlines = [choiceinline]
class choiceAdmin(admin.ModelAdmin):
    list_display = ['id','question','text','value']
    list_per_page = 10
    list_filter = ['value']
    search_fields = ['question']

class commentAdmin(admin.ModelAdmin):
    list_display = ['id','title','email','tel','poll']
    search_fields = ['title']
    list_filter = ['poll']

admin.site.register(Poll,pollAdmin)
admin.site.register(Question,questionAdmin)
admin.site.register(Choice,choiceAdmin)
admin.site.register(Comment, commentAdmin)