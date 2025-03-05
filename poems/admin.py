from django.contrib import admin

from .models import Questionnaire, Poem, PoemSet

# Register your models here.
admin.site.register(PoemSet)
admin.site.register(Questionnaire)
admin.site.register(Poem)
