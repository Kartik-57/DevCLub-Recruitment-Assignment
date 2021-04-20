from django.contrib import admin
from .models import Book, Review, Availability

admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Availability)
