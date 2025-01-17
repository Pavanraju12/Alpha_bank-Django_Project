from django.db import models

# Create your models here.
class bank(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    phone = models.BigIntegerField()
    DOB = models.DateField()
    email_id = models.EmailField()
    address= models.TextField()
    father_name = models.CharField(max_length=52)
    mother_name = models.CharField(max_length=50)
    gender =models.CharField(max_length=32)
    pin_code= models.IntegerField()
    image=models.ImageField(upload_to="images")
    balance=models.IntegerField()


    pin=models.IntegerField(null=True, blank=True)
   

    account_no =models.IntegerField(null=True, blank=True)