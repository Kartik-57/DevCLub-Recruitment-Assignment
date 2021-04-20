from django.db import models
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse

class Book(models.Model):
    Author = models.CharField(max_length=100)
    Publisher = models.CharField(max_length=200)
    Book_Title = models.CharField(max_length=200)
    Genre = models.CharField(max_length=100) 
    Book_Cover = models.FileField()
    ISBN = models.CharField(max_length=20)

    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.Book_Title + ' - ' + self.Author

class Review(models.Model):
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Description = models.CharField(max_length=1000)

    def __str__(self):
        return self.Description

class Availability(models.Model):
    Book = models.ForeignKey(Book, on_delete=models.CASCADE)
    Available = models.BooleanField(default=True)

    def __str__(self):
        return self.Available  

    
