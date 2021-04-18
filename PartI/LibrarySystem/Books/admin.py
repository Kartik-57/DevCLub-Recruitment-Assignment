from django.contrib import admin
from .models import Book, Summary, Availability

admin.site.register(Book)
admin.site.register(Summary)
admin.site.register(Availability)
