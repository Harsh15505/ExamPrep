from django.contrib import admin
from .models import Book, Member, IssueRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'isbn', 'total_copies', 'available_copies']
    search_fields = ['title', 'author', 'isbn']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'joined_date']
    search_fields = ['name', 'email']

@admin.register(IssueRecord)
class IssueRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'member', 'issue_date', 'due_date', 'returned', 'return_date']
    list_filter = ['returned']
    search_fields = ['book__title', 'member__name']
    # book__title: traverses ForeignKey to filter by related Book's title
