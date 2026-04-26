from django.db import models

class Student(models.Model):
    # Django auto-adds 'id' as primary key (auto-increment)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)          # unique=True → DB UNIQUE constraint + auto form validation
    course = models.CharField(max_length=100)
    date_of_joining = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.course})"

    class Meta:
        ordering = ['-date_of_joining']             # newest students first by default
