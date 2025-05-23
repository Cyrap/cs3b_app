from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books')
    pdf_file = models.FileField(upload_to='books/pdfs/', null=True)
    image = models.ImageField(upload_to="books/image/", null=True)
    publish_date = models.DateField(blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.title}"

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    student_code = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=150)
    course = models.CharField(max_length=100)
    is_staff_member = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

class LendingRecord(models.Model):
    STATUS_PENDING = 0
    STATUS_DECLINED = 1
    STATUS_APPROVED = 2

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_DECLINED, 'Declined'),
        (STATUS_APPROVED, 'Approved'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='lendings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lendings')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    returned = models.BooleanField(default=False)
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_PENDING)

    def __str__(self):
        return f"{self.book.title} lent to {self.user.username} from {self.start_date} to {self.end_date or 'Not returned'} (Status: {self.get_status_display()})"

    class Meta:
        ordering = ['-start_date']