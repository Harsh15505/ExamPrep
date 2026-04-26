from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Book, Member, IssueRecord
from .forms import BookForm, MemberForm, IssueForm


# ── BOOK CRUD ──────────────────────────────────────────────────

def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book added!')
            return redirect('book-list')
    else:
        form = BookForm()
    return render(request, 'library/form.html', {'form': form, 'title': 'Add Book'})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, 'Book updated!')
        return redirect('book-list')
    return render(request, 'library/form.html', {'form': form, 'title': 'Edit Book'})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted!')
        return redirect('book-list')
    return render(request, 'library/confirm_delete.html', {'object': book, 'type': 'Book'})


# ── MEMBER CRUD ────────────────────────────────────────────────

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


# ── ISSUE / RETURN ─────────────────────────────────────────────

def issue_book(request):
    """Issue a book to a member — checks availability before issuing"""
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            if not book.is_available():
                # Check availability: available_copies > 0
                messages.error(request, f'"{book.title}" is not available right now.')
                return render(request, 'library/issue_form.html', {'form': form})
            issue = form.save()
            # Decrement available copies
            book.available_copies -= 1
            book.save()
            messages.success(request, f'"{book.title}" issued to {issue.member.name}!')
            return redirect('issue-list')
    else:
        form = IssueForm()
    return render(request, 'library/issue_form.html', {'form': form})

def return_book(request, pk):
    """Return a book — marks returned=True, restores available_copies"""
    issue = get_object_or_404(IssueRecord, pk=pk)
    if request.method == 'POST':
        issue.returned = True
        issue.return_date = timezone.now().date()
        issue.save()
        # Restore available copy
        issue.book.available_copies += 1
        issue.book.save()
        messages.success(request, f'"{issue.book.title}" returned successfully!')
        return redirect('issue-list')
    return render(request, 'library/return_confirm.html', {'issue': issue})

def issue_list(request):
    """List all issue records"""
    issues = IssueRecord.objects.select_related('book', 'member').all()
    # select_related: fetches book + member in single JOIN query (performance)
    return render(request, 'library/issue_list.html', {'issues': issues})


# ── SPECIAL QUERIES ────────────────────────────────────────────

def overdue_books(request):
    """List overdue books: not returned AND past due_date"""
    today = timezone.now().date()
    overdue = IssueRecord.objects.filter(
        returned=False,
        due_date__lt=today       # due_date < today → overdue
    ).select_related('book', 'member')
    return render(request, 'library/overdue.html', {'overdue': overdue})

def books_by_member(request, member_id):
    """List all books issued to a specific member"""
    member = get_object_or_404(Member, pk=member_id)
    issues = IssueRecord.objects.filter(member=member).select_related('book')
    return render(request, 'library/member_books.html', {'member': member, 'issues': issues})
