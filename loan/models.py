from django.db import models
from django.contrib.auth.models import User
from customer.models import Customer
class Category(models.Model):
    category_name =models.CharField(max_length=20)
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.category_name

class Loan(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    loan_name = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now=True)
    def __str__(self):
        return self.loan_name

class LoanRecord(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    Loan = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100,default='Pending')
    creation_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.loan

class Question(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    description =models.CharField(max_length=500)
    admin_comment=models.CharField(max_length=200,default='Nothing')
    asked_date =models.DateField(auto_now=True)
    def __str__(self):
        return self.description
