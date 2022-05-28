
from dataclasses import fields
import datetime
from pyexpat import model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import context
from django.urls import clear_script_prefix, reverse
from .models import Book, Author, BookInstance, Genre
from .forms import RenewBook
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.models import Author


def index(request):
	"""Views for our home page"""

	# Generate counts of some of the main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# The 'all()' is implied by default
	num_authors = Author.objects.count()
	num_genres = Genre.objects.count()

	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'genres': num_genres,
		'num_visits': num_visits,
	}

	# render the html template index.html with the data in the context variable
	return render(request, 'catalog/index.html', context=context)

# @login_required
class BookList(generic.ListView):
	model = Book
	template_name = 'catalog/books.html'
	queryset = Book.objects.all()
	paginate_by = 5

class BookDetailView(generic.DetailView):
	model = Book
	template_name = 'catalog/book.html'


# Challenge below
class AuthorListView(generic.ListView):
	model = Author
	template_name = 'catalog/authors.html'

class AuthorDetailView(generic.DetailView):
	model = Author
	template_name = 'catalog/author.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/user_books.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')



class BorrowedBooks(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
	permission_required = (
		'catalog.can_mark_returned',
	)
	model = BookInstance
	template_name = 'catalog/borrowed_books.html'
	paginate_by = 10

	# def get_queryset(self):
	# 	return BookInstance.objects.filter(borrower=self.request.user)

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book(request, pk):
	book_instance = get_object_or_404(BookInstance, pk=pk)
	
	# if post request, process data
	if request.method == 'POST':

		#create form and populate it with data from the request
		form = RenewBook(request.POST)

		# check if form is valid
		if form.is_valid():
			book_instance.due_back = form.cleaned_data['renewal_date']
			book_instance.save()

			return HttpResponseRedirect(reverse('borrowed_books') )

	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBook(initial={'renewal_date': proposed_renewal_date})

	context = {
		'form': form,
		'book_instance': book_instance,
	}

	return render(request, 'catalog/book_renewal.html', context)

class CreateAuthor(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = (
		'catalog.can_mark_returned',
	)

	model = Author
	fields = ['first_name', 'last_name', ]
	# initial = {'first_name': 'steven'}

class AuthorUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
	permission_required = (
		'catalog.can_mark_returned',
	)

	model = Author
	fields = '__all__' # Not recommended (potential security issue if more fields added)

class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin,  DeleteView):
	permission_required = (
		'catalog.can_mark_returned',
	)
   
	model = Author
	success_url = reverse_lazy('authors')




class CreateBook(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
	permission_required = (
		'catalog.can_mark_returned'
	)
	model = Book
	fields = '__all__'

class DeleteBook(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
	permission_required = (
		'catalog.can_mark_returned'
	)
	model = Book
	template_name = "catalog/delete_book.html"
	success_url = reverse_lazy('books')

class UpdateBook(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
	permission_required = (
		'catalog.can_mark_returned'
	)
	model = Book
	fields = '__all__'
	template_name = 'catalog/update_book.html'
