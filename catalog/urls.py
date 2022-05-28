from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('books/', views.BookList.as_view(), name='books'),
	path('authors/', views.AuthorListView.as_view(), name='authors'),
	path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
	path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author'),
	path('book/author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
	path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my_books'),
	path('borrowed_books/', views.BorrowedBooks.as_view(), name='borrowed_books'),
	path('book/<uuid:pk>/renew/', views.renew_book, name='renew_book'),

	path('author/create/', views.CreateAuthor.as_view(), name='author-create'), #create author
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'), #update author
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'), #delete author

	path('book/new-book/', views.CreateBook.as_view(), name='create-book'), #add book
	path('book/<int:pk>/delete-book', views.DeleteBook.as_view(), name='delete-book'),
	path('book/<int:pk>/update-book', views.UpdateBook.as_view(), name='update-book'),

]
