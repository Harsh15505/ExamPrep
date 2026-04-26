from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def is_available(self):
        return self.available_copies > 0

class Member(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class IssueRecord(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    # ForeignKey: Many IssueRecords → One Book (many-to-one)
    # on_delete=CASCADE: if Book deleted, all its IssueRecords are deleted
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='issues')
    issue_date = models.DateField(auto_now_add=True)        # auto-set on creation
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)   # null until book is returned
    returned = models.BooleanField(default=False)

    def is_overdue(self):
        from django.utils import timezone
        if not self.returned:
            return timezone.now().date() > self.due_date
        return False

    def __str__(self):
        return f"{self.book.title} → {self.member.name}"
