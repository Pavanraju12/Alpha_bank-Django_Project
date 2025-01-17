from django import forms
from .models import bank

class bankforms(forms.ModelForm):
    class Meta:
        model= bank
        # fields= "__all__"
        fields = ['first_name', 'last_name', 'phone', 'DOB', 'email_id',
                  'address', 'father_name', 'mother_name', 'gender',
                  'pin_code', 'image', 'balance', 'pin', 'account_no']
    
    # Hide account_no, balance, and pin fields
    account_no = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    # balance = forms.IntegerField(widget=forms.placeholder, required=True)
    pin = forms.IntegerField(widget=forms.HiddenInput(), required=False)
        
        
        
        # fields= ['first_name','last_name','phone','DOB','email_id','address','father_name','mother_name','gender','pin_code','image']