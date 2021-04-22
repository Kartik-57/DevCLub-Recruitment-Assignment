from django.db import models
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.models import User

class Book(models.Model):
    Author = models.CharField(max_length=100)
    Publisher = models.CharField(max_length=200)
    Book_Title = models.CharField(max_length=200)
    Genre = models.CharField(max_length=100) 
    Book_Cover = models.FileField()
    ISBN = models.CharField(max_length=20)
    Available = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Book_Title + ' - ' + self.Author

class Review(models.Model):
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Description = models.CharField(max_length=1000)

    def __str__(self):
        return self.Description

class Request(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    request_date = models.DateField(null=True, blank=True)
    lent_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
    close_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=(('p','pending'), ('a', 'accepted'), ('r', 'rejected')), blank=True, default='pending') 

    def __str__(self):
        return self.Available  

    
