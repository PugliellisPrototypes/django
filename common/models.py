from django.db import models

class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    established_date = models.DateField()
    total_books = models.IntegerField(default=0)
    total_members = models.IntegerField(default=0)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    library = models.ForeignKey(Library, related_name='books', on_delete=models.CASCADE)
    