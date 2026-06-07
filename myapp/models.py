from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Expert(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    Name=models.CharField(max_length=50)
    DOB=models.DateField()
    Gender=models.CharField(max_length=15)
    Photo=models.FileField()
    Place=models.CharField(max_length=50)
    Post=models.CharField(max_length=50)
    Pin=models.IntegerField()
    Phone_number=models.BigIntegerField()
    Email=models.CharField(max_length=50)

class User_table(models.Model):
    LOGIN = models.ForeignKey(User, on_delete=models.CASCADE)
    Name=models.CharField(max_length=50)
    DOB=models.DateField()
    Gender=models.CharField(max_length=15)
    Photo=models.FileField()
    Place=models.CharField(max_length=50)
    Post=models.CharField(max_length=50)
    Pin=models.IntegerField()
    Phone_number=models.BigIntegerField()
    Email=models.CharField(max_length=50)

class Feedback_table(models.Model):
    User=models.ForeignKey(User_table,on_delete=models.CASCADE)
    Feedback=models.CharField(max_length=200)
    Date=models.DateField()
    Expert=models.ForeignKey(Expert,on_delete=models.CASCADE)

class Complaint(models.Model):
    User = models.ForeignKey(User_table, on_delete=models.CASCADE)
    Complaint=models.CharField(max_length=200)
    Date = models.DateField()
    Reply=models.CharField(max_length=200)

class Tips(models.Model):
    Expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    Tip=models.CharField(max_length=200)
    Details=models.CharField(max_length=1000)
    Date = models.DateField()

class Transaction(models.Model):
    User = models.ForeignKey(User_table, on_delete=models.CASCADE)
    Exp_type=models.CharField(max_length=20)
    Mode=models.CharField(max_length=50)
    Amount=models.IntegerField()
    Date = models.DateField()
    Tan_type=models.CharField(max_length=50)

class Reminder(models.Model):
    User = models.ForeignKey(User_table, on_delete=models.CASCADE)
    Type=models.CharField(max_length=20)
    Amount = models.IntegerField()
    Details=models.CharField(max_length=200)
    Status=models.CharField(max_length=100)
    Date = models.DateField()
    reminder_date = models.DateField()

class Suggestions(models.Model):
    Expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    User = models.ForeignKey(User_table, on_delete=models.CASCADE)
    Suggestion = models.CharField(max_length=200)
    Date = models.DateField()

class Chat(models.Model):
    From_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='from_id')
    To_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='to_id')
    Message = models.CharField(max_length=200)
    Date = models.DateField()
    Time = models.CharField(max_length=200)
    Status = models.CharField(max_length=50)

class Goal(models.Model):
    User = models.ForeignKey(User_table, on_delete=models.CASCADE)
    Amount = models.IntegerField()
    Date = models.DateField()
    Details = models.CharField(max_length=200)




class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)



class Notification(models.Model):
    User = models.ForeignKey(User_table, on_delete=models.CASCADE)
    Date = models.DateField()
