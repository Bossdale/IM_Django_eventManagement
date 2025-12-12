from django.db import models

# 1. WARNING: This class is named 'User', but it is NOT the standard Django auth User.
# This creates a table 'account_user', distinct from 'auth_user' used for login.
class User(models.Model):
    user_type = (('S', 'Student'), ('T', 'Teacher'),)
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20) # Note: This stores plain text, not secure hashes!
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, null=True, blank=True) # Added blank=True
    lastname = models.CharField(max_length=50)
    type = models.CharField(max_length=1, choices=user_type, default='S')

    def __str__(self):
        # 2. FIX: Handle None (null) middlename to prevent crashes
        mid = f" {self.middlename}" if self.middlename else ""
        return f"{self.firstname}{mid} {self.lastname}"

class Student(User):
    course = models.CharField(max_length=20)
    year = models.IntegerField(default=1)
    department = models.CharField(max_length=50)

class Teacher(User):
    age = models.IntegerField()

class Specialization(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50)

    # 3. FIX: Indentation fixed. This must be INSIDE the class.
    class Meta:
         unique_together = ('teacher', 'specialization')