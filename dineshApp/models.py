from django.db import models

# Create your models here.
class HouseRentModel(models.Model):
    date = models.DateField()
    house = models.CharField(max_length=20)
    rent_recieved = models.IntegerField()
    account = models.CharField(max_length=30)

class EBBillModel(models.Model):
    house = models.CharField(max_length=30)
    date = models.DateField()
    eb_no = models.IntegerField()
    amount = models.IntegerField()
    yes_no = models.CharField(max_length=20)

class PrivatePublicAccount(models.Model):
    bank_name = models.CharField(max_length=50, null=True)
    balance = models.FloatField()

class PublicAccountDetails(models.Model):
    date = models.DateField()
    recieved = models.FloatField(null=True)
    expense = models.FloatField(null=True)
    description = models.TextField()
    balance_history = models.FloatField(null=True)

class PrivateAccountDetailsModel(models.Model):
    bank_name = models.CharField(max_length=50)
    date = models.DateField()
    recieved = models.FloatField(null=True)
    expense = models.FloatField(null=True)
    description = models.TextField()
    balance_history = models.FloatField(null=True)

class CraneOperatorDetailsModel(models.Model):
    name = models.CharField(max_length=30)
    leave_advance = models.CharField(max_length=30)
    date = models.DateField()
    amount = models.FloatField()
    balance = models.FloatField(null=True)

class CraneBillMainDate(models.Model):
    company = models.CharField(max_length=50)
    main_date = models.DateField()
    bill_number = models.IntegerField()

class CraneBillSubDate(models.Model):
    main_date = models.ForeignKey(CraneBillMainDate, on_delete=models.CASCADE)
    sub_date = models.DateField()
    hours = models.CharField(max_length=50)
    amount = models.IntegerField()

class IGPModelSequence(models.Model):
    seq_bill = models.IntegerField()
    date = models.DateField()

class IGPModel(models.Model):
    seq_bill = models.ForeignKey(IGPModelSequence, on_delete=models.CASCADE)
    date = models.DateField()
    tot_hours = models.CharField(max_length=50)
    amount = models.IntegerField()

class NotePadModel(models.Model):
    date = models.DateField(auto_now=True)
    notes = models.TextField()

class CommonBillCalculationModel(models.Model):
    company_name = models.CharField(max_length=50)
    bill_date = models.DateField()
    bill_number = models.IntegerField()
    tot_hours = models.CharField(max_length=50)
    amount = models.IntegerField()

class CompanyMasterModel(models.Model):
    company_name = models.CharField(max_length=100)