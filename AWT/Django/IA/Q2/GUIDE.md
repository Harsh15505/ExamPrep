# Q2 — Library Management System: Detailed Code Guide

---

## 📌 What This App Does
- Manages Books, Members, and Issue Records in PostgreSQL
- CRUD for Books and Members
- Issue a book to a member (with availability check)
- Return a book (restores available copies)
- Query overdue books
- Query all books issued to a specific member

---

## 📄 models.py — Line by Line

```python
from django.db import models


# ══════════════════════════════════════════════
# MODEL 1: Book
# ══════════════════════════════════════════════
class Book(models.Model):
    title = models.CharField(max_length=200)
    # Short string for the book title. VARCHAR(200) in PostgreSQL.

    author = models.CharField(max_length=100)
    # Author's name

    isbn = models.CharField(max_length=20, unique=True)
    # ISBN is unique per book — unique=True adds UNIQUE constraint in DB
    # No two books can have the same ISBN number

    total_copies = models.PositiveIntegerField(default=1)
    # How many copies the library owns in total
    # PositiveIntegerField: only accepts 0 or positive integers
    # default=1: new books start with 1 copy

    available_copies = models.PositiveIntegerField(default=1)
    # How many copies are currently available for borrowing
    # This gets DECREMENTED when a book is issued
    # This gets INCREMENTED when a book is returned

    def __str__(self):
        return f"{self.title} by {self.author}"
        # Used in admin and in IssueForm's book dropdown

    def is_available(self):
        # Custom method to check if any copy is available
        # Called in the issue_book view before issuing
        return self.available_copies > 0
        # Returns True if at least one copy is free


# ══════════════════════════════════════════════
# MODEL 2: Member
# ══════════════════════════════════════════════
class Member(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)
    # Each member must have a unique email — acts as their unique identifier

    phone = models.CharField(max_length=15, blank=True)
    # blank=True: phone is optional in forms (not required field)
    # Note: no null=True because CharField stores empty string '' not NULL

    joined_date = models.DateField(auto_now_add=True)
    # auto_now_add=True: automatically set to TODAY when member is created
    # This field is NOT editable — Django sets it automatically
    # No need to include it in forms

    def __str__(self):
        return self.name


# ══════════════════════════════════════════════
# MODEL 3: IssueRecord
# This is the LINKING table between Book and Member
# ══════════════════════════════════════════════
class IssueRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    # ForeignKey: creates a MANY-TO-ONE relationship
    #   → Many IssueRecords can reference ONE Book
    #   → In SQL: book_id INTEGER REFERENCES library_app_book(id)
    # on_delete=CASCADE:
    #   → If the Book is deleted, ALL its IssueRecords are also deleted
    #   → Other options: SET_NULL, PROTECT, SET_DEFAULT
    # related_name='issues':
    #   → Allows reverse lookup: book.issues.all() → all issues for a book

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='issues')
    # Same pattern: Many IssueRecords → One Member
    # member.issues.all() → all books this member has issued

    issue_date = models.DateField(auto_now_add=True)
    # Auto-set to today when the record is created (when book is issued)
    # Not editable

    due_date = models.DateField()
    # Staff manually sets the return deadline when issuing
    # Used for overdue checking

    return_date = models.DateField(null=True, blank=True)
    # null=True: allows NULL in DB — the field is empty until book is returned
    # blank=True: not required in forms
    # Set to today when return_book view is called

    returned = models.BooleanField(default=False)
    # False when book is issued, True when book is returned
    # Used to filter: returned=False → currently issued books

    def is_overdue(self):
        # Check if this issue is overdue:
        # Conditions: not returned AND today's date is past due_date
        from django.utils import timezone
        if not self.returned:
            return timezone.now().date() > self.due_date
        return False
        # Returns True only if book hasn't been returned and is past due

    def __str__(self):
        return f"{self.book.title} → {self.member.name}"
        # Traverses ForeignKey: self.book.title accesses the Book's title field
        # self.member.name accesses the Member's name field
```

---

## 📄 forms.py — Line by Line

```python
from django import forms
from .models import Book, Member, IssueRecord


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'total_copies', 'available_copies']
        # We include available_copies so staff can manually set initial count
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_copies': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'phone']
        # Note: 'joined_date' NOT included — auto_now_add handles it
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IssueForm(forms.ModelForm):
    class Meta:
        model = IssueRecord
        fields = ['book', 'member', 'due_date']
        # 'issue_date' excluded — auto_now_add
        # 'return_date' excluded — set programmatically when returned
        # 'returned' excluded — starts as False, changed on return
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            # Select renders a <select> dropdown
            # Django populates it with Book.objects.all()
            # Each option shows Book.__str__: "Python Crash Course by Eric Matthes"

            'member': forms.Select(attrs={'class': 'form-control'}),
            # Same: dropdown of all Member objects

            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
```

---

## 📄 views.py — Line by Line

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
# timezone.now().date() → gives today's date (timezone-aware, safe for production)

from .models import Book, Member, IssueRecord
from .forms import BookForm, MemberForm, IssueForm


# ══════════════════════════════════════════════
# BOOK VIEWS
# ══════════════════════════════════════════════

def book_list(request):
    books = Book.objects.all()
    # Fetch all books: SELECT * FROM library_app_book;
    return render(request, 'library/book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)   # Bind submitted data
        if form.is_valid():
            form.save()                  # INSERT INTO library_app_book ...
            messages.success(request, 'Book added!')
            return redirect('book-list')
    else:
        form = BookForm()               # Empty form for GET request
    return render(request, 'library/form.html', {'form': form, 'title': 'Add Book'})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    # request.POST or None:
    #   On POST: request.POST is a dict → binds data to form
    #   On GET:  request.POST is empty QueryDict → evaluates as None → unbound form
    # This is a shorthand to avoid the if/else pattern
    # instance=book → form updates this book (not create new)
    if form.is_valid():
        form.save()                     # UPDATE library_app_book SET ... WHERE id=pk
        messages.success(request, 'Book updated!')
        return redirect('book-list')
    return render(request, 'library/form.html', {'form': form, 'title': 'Edit Book'})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()                   # DELETE FROM library_app_book WHERE id=pk
        # CASCADE: also deletes all IssueRecords with this book_id
        messages.success(request, 'Book deleted!')
        return redirect('book-list')
    return render(request, 'library/confirm_delete.html', {'object': book, 'type': 'Book'})


# ══════════════════════════════════════════════
# MEMBER VIEWS (same pattern as Book)
# ══════════════════════════════════════════════

def member_list(request):
    members = Member.objects.all()
    return render(request, 'library/member_list.html', {'members': members})

def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added!')
            return redirect('member-list')
    else:
        form = MemberForm()
    return render(request, 'library/form.html', {'form': form, 'title': 'Add Member'})

def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, 'Member updated!')
        return redirect('member-list')
    return render(request, 'library/form.html', {'form': form, 'title': 'Edit Member'})

def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('member-list')
    return render(request, 'library/confirm_delete.html', {'object': member, 'type': 'Member'})


# ══════════════════════════════════════════════
# ISSUE A BOOK — Core Feature
# ══════════════════════════════════════════════
def issue_book(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            # form.cleaned_data: dict of validated Python objects
            # cleaned_data['book'] → the actual Book object (not just its ID)

            if not book.is_available():
                # Check BEFORE issuing: available_copies > 0?
                messages.error(request, f'"{book.title}" is not available right now.')
                return render(request, 'library/issue_form.html', {'form': form})
                # Re-show the form with an error message — don't save

            issue = form.save()
            # INSERT INTO library_app_issuerecord (book_id, member_id, due_date, returned)
            # VALUES (book.pk, member.pk, '2024-07-01', False);

            book.available_copies -= 1
            # Decrement available copies — one copy is now with a member
            book.save()
            # UPDATE library_app_book SET available_copies=available_copies-1 WHERE id=book.pk

            messages.success(request, f'"{book.title}" issued to {issue.member.name}!')
            return redirect('issue-list')
    else:
        form = IssueForm()
    return render(request, 'library/issue_form.html', {'form': form})


# ══════════════════════════════════════════════
# RETURN A BOOK — Core Feature
# ══════════════════════════════════════════════
def return_book(request, pk):
    issue = get_object_or_404(IssueRecord, pk=pk)
    # Fetch the specific IssueRecord being returned

    if request.method == 'POST':
        issue.returned = True
        # Mark the issue record as returned

        issue.return_date = timezone.now().date()
        # Record the actual return date (today)

        issue.save()
        # UPDATE library_app_issuerecord SET returned=True, return_date='2024-06-15' WHERE id=pk

        issue.book.available_copies += 1
        # Access the related Book via ForeignKey: issue.book → the Book object
        # Increment available copies — the copy is back in the library

        issue.book.save()
        # UPDATE library_app_book SET available_copies=available_copies+1 WHERE id=book_pk

        messages.success(request, f'"{issue.book.title}" returned successfully!')
        return redirect('issue-list')

    return render(request, 'library/return_confirm.html', {'issue': issue})


# ══════════════════════════════════════════════
# LIST ALL ISSUES
# ══════════════════════════════════════════════
def issue_list(request):
    issues = IssueRecord.objects.select_related('book', 'member').all()
    # select_related('book', 'member'):
    #   Without it: accessing issue.book.title for each row = N+1 DB queries
    #   With it: Django does ONE SQL JOIN → fetches books + members in one query
    #   SQL: SELECT * FROM issuerecord
    #        JOIN book ON issuerecord.book_id = book.id
    #        JOIN member ON issuerecord.member_id = member.id
    return render(request, 'library/issue_list.html', {'issues': issues})


# ══════════════════════════════════════════════
# OVERDUE BOOKS — Special Query
# ══════════════════════════════════════════════
def overdue_books(request):
    today = timezone.now().date()
    overdue = IssueRecord.objects.filter(
        returned=False,          # Book not yet returned
        due_date__lt=today       # AND due_date < today (past deadline)
        # __lt = "less than" lookup
        # SQL: WHERE returned = False AND due_date < '2024-06-26'
    ).select_related('book', 'member')
    return render(request, 'library/overdue.html', {'overdue': overdue})


# ══════════════════════════════════════════════
# BOOKS ISSUED TO A SPECIFIC MEMBER — Special Query
# ══════════════════════════════════════════════
def books_by_member(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    issues = IssueRecord.objects.filter(member=member).select_related('book')
    # filter(member=member): WHERE member_id = member.pk
    # SQL: SELECT * FROM issuerecord
    #      JOIN book ON issuerecord.book_id = book.id
    #      WHERE issuerecord.member_id = 3
    return render(request, 'library/member_books.html', {'member': member, 'issues': issues})
```

---

## 📄 urls.py — Line by Line

```python
from django.urls import path
from . import views

urlpatterns = [
    # ── Books ─────────────────────────────────────────
    path('books/', views.book_list, name='book-list'),
    # /library/books/ → list all books

    path('books/add/', views.add_book, name='add-book'),
    # /library/books/add/ → add a book

    path('books/<int:pk>/edit/', views.edit_book, name='edit-book'),
    # /library/books/5/edit/ → edit book with id=5

    path('books/<int:pk>/delete/', views.delete_book, name='delete-book'),

    # ── Members ───────────────────────────────────────
    path('members/', views.member_list, name='member-list'),
    path('members/add/', views.add_member, name='add-member'),
    path('members/<int:pk>/edit/', views.edit_member, name='edit-member'),
    path('members/<int:pk>/delete/', views.delete_member, name='delete-member'),

    # ── Issue / Return ────────────────────────────────
    path('issue/', views.issue_book, name='issue-book'),
    # /library/issue/ → form to select book + member + due_date

    path('issue/list/', views.issue_list, name='issue-list'),
    # /library/issue/list/ → all issue records

    path('return/<int:pk>/', views.return_book, name='return-book'),
    # /library/return/7/ → return IssueRecord with id=7

    # ── Special Queries ───────────────────────────────
    path('overdue/', views.overdue_books, name='overdue-books'),
    # /library/overdue/ → list all overdue (unreturned + past due_date)

    path('members/<int:member_id>/books/', views.books_by_member, name='member-books'),
    # /library/members/3/books/ → all books issued to member id=3
    # Note: uses 'member_id' not 'pk' as the parameter name
]
```

---

## 📄 Key Template Highlights

### `book_list.html` — Availability Badge
```html
{% if book.available_copies > 0 %}
    <span class="badge bg-success">{{ book.available_copies }}</span>
    <!-- Green badge: shows count of available copies -->
{% else %}
    <span class="badge bg-danger">0 (Unavailable)</span>
    <!-- Red badge: no copies available -->
{% endif %}
```

### `issue_list.html` — Status + Return Button
```html
{% if issue.returned %}
    <span class="badge bg-success">Returned ({{ issue.return_date }})</span>
    <!-- Book is back — show return date -->
{% else %}
    <span class="badge bg-warning text-dark">Issued</span>
    <!-- Book is out — show Return button -->
{% endif %}

{% if not issue.returned %}
    <a href="{% url 'return-book' issue.pk %}">Return</a>
    <!-- Only show Return button for un-returned books -->
{% endif %}
```

### `overdue.html` — Timesince Filter
```html
<td>{{ issue.due_date|timesince }} ago</td>
<!-- |timesince: Django filter that shows time elapsed -->
<!-- e.g., "3 days ago", "1 week, 2 days ago" -->
```

### `member_list.html` — Link to member's books
```html
<a href="{% url 'member-books' member.pk %}">{{ member.name }}</a>
<!-- Clicking the member's name → /library/members/3/books/ -->
<!-- Shows all books issued to that member -->
```

---

## 🔑 Key Concepts Summary for Q2

| Concept | Where | Why |
|---|---|---|
| `ForeignKey(Book, on_delete=CASCADE)` | `models.py` | Many IssueRecords → One Book |
| `ForeignKey(Member, on_delete=CASCADE)` | `models.py` | Many IssueRecords → One Member |
| `related_name='issues'` | `models.py` | `book.issues.all()` reverse lookup |
| `auto_now_add=True` | `models.py` | Auto-sets date on creation |
| `null=True, blank=True` | `models.py` | Optional field (return_date before return) |
| `book.is_available()` | `views.py` | Custom method: `available_copies > 0` |
| `form.cleaned_data['book']` | `views.py` | Get validated Python object from form |
| `book.available_copies -= 1` | `views.py` | Decrement on issue |
| `book.available_copies += 1` | `views.py` | Increment on return |
| `select_related('book', 'member')` | `views.py` | JOIN query — avoids N+1 problem |
| `due_date__lt=today` | `views.py` | Overdue query: due_date < today |
| `filter(member=member)` | `views.py` | Books issued to a specific member |
| `issue.book.title` | Templates | ForeignKey traversal in template |
