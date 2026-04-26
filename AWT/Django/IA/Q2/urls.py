from django.urls import path
from . import views

urlpatterns = [
    # Books
    path('books/', views.book_list, name='book-list'),
    path('books/add/', views.add_book, name='add-book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit-book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete-book'),

    # Members
    path('members/', views.member_list, name='member-list'),
    path('members/add/', views.add_member, name='add-member'),
    path('members/<int:pk>/edit/', views.edit_member, name='edit-member'),
    path('members/<int:pk>/delete/', views.delete_member, name='delete-member'),

    # Issue / Return
    path('issue/', views.issue_book, name='issue-book'),
    path('issue/list/', views.issue_list, name='issue-list'),
    path('return/<int:pk>/', views.return_book, name='return-book'),

    # Special Queries
    path('overdue/', views.overdue_books, name='overdue-books'),
    path('members/<int:member_id>/books/', views.books_by_member, name='member-books'),
]

# Project-level urls.py should include:
# path('library/', include('library_app.urls')),
