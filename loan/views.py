from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import User
from customer import models as CMODEL
from customer import forms as CFORM

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'loan/index.html')


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()


def afterlogin_view(request):
    if is_customer(request.user):      
        return redirect('customer/customer-dashboard')
    else:
        return redirect('admin-dashboard')



def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    dict={
        'total_user':CMODEL.Customer.objects.all().count(),
        'total_loan':models.Loan.objects.all().count(),
        'total_category':models.Category.objects.all().count(),
        'total_question':models.Question.objects.all().count(),
        'total_loan_holder':models.LoanRecord.objects.all().count(),
        'approved_loan_holder':models.LoanRecord.objects.all().filter(status='Approved').count(),
        'disapproved_loan_holder':models.LoanRecord.objects.all().filter(status='Disapproved').count(),
        'waiting_loan_holder':models.LoanRecord.objects.all().filter(status='Pending').count(),
    }
    return render(request,'loan/admin_dashboard.html',context=dict)



@login_required(login_url='adminlogin')
def admin_view_customer_view(request):
    customers= CMODEL.Customer.objects.all()
    return render(request,'loan/admin_view_customer.html',{'customers':customers})

@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=CMODEL.User.objects.get(id=customer.user_id)
    userForm=CFORM.CustomerUserForm(instance=user)
    customerForm=CFORM.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=CFORM.CustomerUserForm(request.POST,instance=user)
        customerForm=CFORM.CustomerForm(request.POST,request.FILES,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('admin-view-customer')
    return render(request,'loan/update_customer.html',context=mydict)



@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=CMODEL.Customer.objects.get(id=pk)
    user=User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return HttpResponseRedirect('/admin-view-customer')



def admin_category_view(request):
    return render(request,'loan/admin_category.html')

def admin_add_category_view(request):
    categoryForm=forms.CategoryForm() 
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST)
        if categoryForm.is_valid():
            categoryForm.save()
            return redirect('admin-view-category')
    return render(request,'loan/admin_add_category.html',{'categoryForm':categoryForm})

def admin_view_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'loan/admin_view_category.html',{'categories':categories})

def admin_delete_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'loan/admin_delete_category.html',{'categories':categories})
    
def delete_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    category.delete()
    return redirect('admin-delete-category')

def admin_update_category_view(request):
    categories = models.Category.objects.all()
    return render(request,'loan/admin_update_category.html',{'categories':categories})

@login_required(login_url='adminlogin')
def update_category_view(request,pk):
    category = models.Category.objects.get(id=pk)
    categoryForm=forms.CategoryForm(instance=category)
    
    if request.method=='POST':
        categoryForm=forms.CategoryForm(request.POST,instance=category)
        
        if categoryForm.is_valid():

            categoryForm.save()
            return redirect('admin-update-category')
    return render(request,'loan/update_category.html',{'categoryForm':categoryForm})
  
  

def admin_loan_view(request):
    return render(request,'loan/admin_loan.html')


def admin_add_loan_view(request):
    loanForm=forms.LoanForm() 
    
    if request.method=='POST':
        loanForm=forms.LoanForm(request.POST)
        if loanForm.is_valid():
            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            loan = loanForm.save(commit=False)
            loan.category=category
            loan.save()
            return redirect('admin-view-loan')
    return render(request,'loan/admin_add_loan.html',{'loanForm':loanForm})

def admin_view_loan_view(request):
    loans = models.Loan.objects.all()
    return render(request,'loan/admin_view_loan.html',{'loans':loans})



def admin_update_loan_view(request):
    loans = models.Loan.objects.all()
    return render(request,'loan/admin_update_loan.html',{'loans':loans})

@login_required(login_url='adminlogin')
def update_loan_view(request,pk):
    loan = models.Loan.objects.get(id=pk)
    loanForm=forms.LoanForm(instance=loan)
    
    if request.method=='POST':
        loanForm=forms.LoanForm(request.POST,instance=loan)
        
        if loanForm.is_valid():

            categoryid = request.POST.get('category')
            category = models.Category.objects.get(id=categoryid)
            
            loan = loanForm.save(commit=False)
            loan.category=category
            loan.save()
           
            return redirect('admin-update-loan')
    return render(request,'loan/update_loan.html',{'loanForm':loanForm})
  
  
def admin_delete_loan_view(request):
    loans = models.Loan.objects.all()
    return render(request,'loan/admin_delete_loan.html',{'loans':loans})
    
def delete_loan_view(request,pk):
    loan = models.Loan.objects.get(id=pk)
    loan.delete()
    return redirect('admin-delete-loan')

def admin_view_loan_holder_view(request):
    loanrecords = models.LoanRecord.objects.all()
    return render(request,'loan/admin_view_loan_holder.html',{'loanrecords':loanrecords})

def admin_view_approved_loan_holder_view(request):
    loanrecords = models.LoanRecord.objects.all().filter(status='Approved')
    return render(request,'loan/admin_view_approved_loan_holder.html',{'loanrecords':loanrecords})

def admin_view_disapproved_loan_holder_view(request):
    loanrecords = models.LoanRecord.objects.all().filter(status='Disapproved')
    return render(request,'loan/admin_view_disapproved_loan_holder.html',{'loanrecords':loanrecords})

def admin_view_waiting_loan_holder_view(request):
    loanrecords = models.LoanRecord.objects.all().filter(status='Pending')
    return render(request,'loan/admin_view_waiting_loan_holder.html',{'loanrecords':loanrecords})

def approve_request_view(request,pk):
    loanrecords = models.LoanRecord.objects.get(id=pk)
    loanrecords.status='Approved'
    loanrecords.save()
    return redirect('admin-view-loan-holder')

def disapprove_request_view(request,pk):
    loanrecords = models.LoanRecord.objects.get(id=pk)
    loanrecords.status='Disapproved'
    loanrecords.save()
    return redirect('admin-view-loan-holder')


def admin_question_view(request):
    questions = models.Question.objects.all()
    return render(request,'loan/admin_question.html',{'questions':questions})

def update_question_view(request,pk):
    question = models.Question.objects.get(id=pk)
    questionForm=forms.QuestionForm(instance=question)
    
    if request.method=='POST':
        questionForm=forms.QuestionForm(request.POST,instance=question)
        
        if questionForm.is_valid():

            admin_comment = request.POST.get('admin_comment')
            question = questionForm.save(commit=False)
            question.admin_comment=admin_comment
            question.save()
           
            return redirect('admin-question')
    return render(request,'loan/update_question.html',{'questionForm':questionForm})


def aboutus_view(request):
    return render(request,'loan/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'loan/contactussuccess.html')
    return render(request, 'loan/contactus.html', {'form':sub})

