from django.shortcuts import render,redirect

import random
from django.core.mail import send_mail
from .forms import bankforms
from .models import bank
from django.db.models import Max

from django.conf import settings
from django.contrib import messages



# Create your views here.
def index(request):

    return render(request,'index.html')


# Create your views here.
def create(request):
    form =bankforms()
    context ={
        'form':form
    }
    if request.method == 'POST':
        
        form=bankforms(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            bank_instance = form.save(commit=False)  # Don't save yet, we need to modify some fields
            
            # If the account number is None, generate a random one
            if bank_instance.account_no is None:
                # Get the maximum account number in the database (if any) and increment by 1
                last_account = bank.objects.aggregate(Max('account_no'))['account_no__max']
                if last_account is None:  # If there are no accounts, start from 1000
                    bank_instance.account_no =123456789888
                else:
                    bank_instance.account_no = last_account + 1 
            
        
            if bank_instance.pin is None:
                # Set a default pin or generate one
                bank_instance.pin = 0000  # Or whatever logic you want for generating a pin

            bank_instance.save()
            print("Account created successfully!")
            
    
    return render(request,'Create-Account.html',context)



def Deposite(request):
    update = True
    if request.method == "POST":
        # Get  the form inputs
        account_no = request.POST.get('account_no')  # Account number from form
        balance = request.POST.get('balance')  # Amount to deposit from form
        pin2= request.POST.get('pin_no')
        try:
            # Try to fetch the bank account from the database based on the account number
            data2 = bank.objects.get(account_no=account_no,pin=pin2)
            
            # If found, proceed with updating the balance
            data2.balance =data2.balance+ float(balance)  # Add the deposit amount to the current balance
            data2.save()  # Save the updated bank account
            
            message = "Deposit successful."
        except bank.DoesNotExist:
            # If account does not exist, handle the error
            message = "Account number not found/wrong Pin entered. Please check the account number."

        # Add the message to the context
        context = {
            'message': message,
            'data2': data2 if 'data2' in locals() else None,  # Only include data2 if found
            'update': update
        }

        return render(request, 'Deposite.html', context)

    # For GET request, just return the form
    return render(request, 'Deposite.html', {'update': update})







def Payments(request):
    update=True
    payment_method = request.POST.get('payment_method')
    if payment_method == "acc1":
        if request.method== "POST":
            sender_account_no = request.POST.get('sender_account_no') 
            recipient_account_no = request.POST.get('recipient_account_no')
            amount = request.POST.get('amount')
            pin2 = request.POST.get('pin_no1')
            try:
                data2 = bank.objects.get(account_no=sender_account_no,pin=pin2)
                data3 = bank.objects.get(account_no=recipient_account_no)
                data2.balance -= float(amount) 
                data3.balance  += float(amount)
                data2.save()  # Save the updated bank account
                data3.save()
                message = f"Amount Transfer successfully To Bank number: {data3.account_no}"
                message1=f"Transfered Amount is: {amount}"
                message2 = f"Your Current balance is: {data2.balance}"
            except bank.DoesNotExist:  
                message = "Account number not found. Please check the account numbers." 
            context = {
                'message': message,
                'message1': message1,
                'message2': message2,
                'data2': data2 if 'data2' in locals() else None, 
                'data3': data3 if 'data3' in locals() else None, 
                'update': update
            }
            return render(request, 'Payments.html', context)
    elif payment_method == "acc2":
        if request.method== "POST":
            sender_account_no = request.POST.get('sender_account_no') 
            recipient_phone_no = request.POST.get('recipient_phone_no')
            amount = request.POST.get('amount')
            pin3 = request.POST.get('pin_no2')
            try:
                data2 = bank.objects.get(account_no=sender_account_no,pin=pin3)
                data3 = bank.objects.get(phone=recipient_phone_no )
                data2.balance -= float(amount) 
                data3.balance  += float(amount)
                data2.save()  # Save the updated bank account
                data3.save()
                message = f"Amount Transfer successfully To Phone Number:  {data3.phone}"
                message1=f"Transfered Amount is:   {amount}"
                message2 = f"Your Current balance is:   {data2.balance}"
            except bank.DoesNotExist:  
                message = "Account number not found. Please check the account numbers." 
            context = {
                'message': message,
                'message1': message1,
                'message2': message2,
                'data2': data2 if 'data2' in locals() else None, 
                'data3': data3 if 'data3' in locals() else None, 
                'update': update
            }
            return render(request, 'Payments.html', context)

    
    return render(request, 'Payments.html', {'update': update})




def generate_otp():
    """Generate a 4-digit OTP."""
    otp=random.randint(1000, 9999)
    return otp

def pin_generation(request):
    global otp
    
    update=True
    pin_gen= request.POST.get('pin_gen')
    if pin_gen == "acc1":
        if request.method== "POST":
            first = request.POST.get('first_name')
            last = request.POST.get('last_name')
            account= request.POST.get('account_no')
            email= request.POST.get('email_id')
            try:
                data = bank.objects.get(account_no=account,email_id=email,first_name=first,last_name=last)
                otp=generate_otp()
                request.session['otp'] = otp 
                request.session['account_no'] = account 
                send_mail(
                     'Your OTP for PIN Generation',
                     f'Your OTP to update your PIN is: {otp}',
                
                     settings.EMAIL_HOST_USER, # Sender email (use your actual email)
                      [email],
                      fail_silently=False,
                      )
                
                
                
                return render(request, 'Pin_generation.html', {'otp_sent': True})

            except bank.DoesNotExist:  
                 return render(request, 'Pin_generation.html', {'error': 'Account not found. Please enter valid details for OTP.'}) 
    elif pin_gen == "acc2":
        if request.method== "POST":
            otp1 = request.POST.get('otp')
            otp=  request.session.get('otp') 
            if otp ==int(otp1) :
                request.session['otp_verified'] = True 
                
                return render(request, 'Pin_generation.html', {'otp_verified': True})
            else:
                return render(request, 'Pin_generation.html', {'error': 'Incorrect OTP. Please try again.'})
    
    elif pin_gen == "acc3":
        if request.method== "POST":
            new_pin= request.POST.get('pin1')
            if request.session.get('otp_verified'):
                try:
                    account1=request.session.get('account_no')
                    data1 = bank.objects.get(account_no=account1)
                    data1.pin = int(new_pin)

                    data1.save()  # Update the PIN in the database
                    
                    # context={
                    # 'data1':data1,
                    # 'update':update,
                    
                    #  }
                    return render(request, 'Pin_generation.html', {'success': 'PIN updated successfully!'})
                except bank.DoesNotExist:
                    return render(request, 'Pin_generation.html', {'error': 'Account not found. Please try again.'})
            else:
                return render(request, 'Pin_generation.html', {'error': 'OTP verification is required before updating PIN.'})

    return render(request, 'Pin_generation.html')





def about(request):
    account_details = None  # Default to None (no account found)
    
    # Check if there is a GET request with the account number
    if request.method == 'GET' and 'account_no' in request.GET:
        account_no = request.GET['account_no']
        
        # Try to fetch the bank account details by account number
        try:
            account_details = bank.objects.get(account_no=account_no)
        except bank.DoesNotExist:
            account_details = None  # If no account found, keep it as None
    
    return render(request, 'about.html', {'account_details': account_details})

