from os import nice
from django.contrib.auth.models import User

from pyexpat import model
from django.db import models
from django.urls import reverse
import uuid
from datetime import date

# Create your models here.
class Genre(models.Model):
	"""Model representing a book genre"""
	name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

	def __str__(self):
		return self.name


class Book(models.Model):
	"""Model to represent a book"""
	title = models.CharField(max_length=200)
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	summary = models.TextField(max_length=1000, help_text='Enter a brief summary of the book')
	isbn = models.CharField('ISBN', max_length=13, unique=True,
	help_text='13 Char <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a> ')


	genre = models.ManyToManyField(Genre, help_text='Select genre for this book')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("book-detail", args=[str(self.id)])
	
class BookInstance(models.Model):
	"""Model representing a specific copy of the book that can be borrowed"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
	 help_text='Unique ID for this book')
	
	book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	book_language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		return False

	LOAN_STATUS = (
		('m', 'Maintenance'),
		('o', 'On loan'),
		('a', 'Available'),
		('r', 'Reserved'),
	)

	status = models.CharField(
		max_length=1,
		choices=LOAN_STATUS,
		blank=True,
		default='m', 
		help_text='Book availability'
	)

	class Meta:
		ordering = ['due_back']
		permissions = (
			("can_mark_returned", "Set book as returned"),
			("can_delete_book_instance", "Can delete book instance"),
		)

	def __str__(self):
		return f'{self.id} ({self.book.title})'


class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField('Died', null=True, blank=True)

	class Meta:
		ordering = ['last_name', 'first_name']

	def get_absolute_url(self):
		return reverse("author", args=[str(self.id)])
	
	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
	LANGUAGES = (
		('eng', 'English'),
		('far', 'Farsi'),
	)

	language = models.CharField(
		max_length=200,
		choices=LANGUAGES,
		default='eng',
		blank=True,
		help_text='Select book language'
	)

	def __str__(self):
		return self.language