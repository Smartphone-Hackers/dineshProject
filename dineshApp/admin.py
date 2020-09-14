from django.contrib import admin
from dineshApp.models import HouseRentModel
from dineshApp.models import EBBillModel
from dineshApp.models import PrivatePublicAccount
from dineshApp.models import PublicAccountDetails
from dineshApp.models import CraneOperatorDetailsModel
from dineshApp.models import IGPModelSequence
from dineshApp.models import IGPModel
from dineshApp.models import CraneBillMainDate
from dineshApp.models import CraneBillSubDate
from dineshApp.models import PrivateAccountDetailsModel
from dineshApp.models import CommonBillCalculationModel

# Register your models here.

class ShowHouseRentModel(admin.ModelAdmin):
    list_display = ('id', 'date', 'house', 'rent_recieved', 'account')

class ShowEBBillModel(admin.ModelAdmin):
    list_display = ('id', 'date', 'house', 'eb_no', 'amount', 'yes_no')

class ShowPublicAccountDetails(admin.ModelAdmin):
    list_display = ('id', 'date', 'recieved', 'expense', 'description')

class ShowPrivateAccountDetailsModel(admin.ModelAdmin):
    list_display = ('id', 'bank_name', 'date', 'recieved', 'expense', 'description')

class ShowPublicAccount(admin.ModelAdmin):
    list_display = ('id', 'bank_name', 'balance',)

class ShowCraneOperatorDetailsModel(admin.ModelAdmin):
    list_display = ('id', 'name', 'leave_advance', 'date', 'amount', 'balance')

class ShowIGPModelSequence(admin.ModelAdmin):
    list_display = ('date', 'seq_bill')

class ShowIGPModel(admin.ModelAdmin):
    list_display = ('seq_bill', 'date', 'tot_hours', 'amount')

class ShowCommonBillCalculationModel(admin.ModelAdmin):
    list_display = ('company_name', 'bill_date', 'bill_number', 'tot_hours', 'amount')

class ShowCraneBillMainDate(admin.ModelAdmin):
    list_display = ('company', 'main_date', 'bill_number')

class ShowCraneBillSubDate(admin.ModelAdmin):
    list_display = ('main_date', 'sub_date', 'hours', 'amount')

admin.site.register(HouseRentModel, ShowHouseRentModel)
admin.site.register(EBBillModel, ShowEBBillModel)
admin.site.register(PublicAccountDetails, ShowPublicAccountDetails)
admin.site.register(PrivatePublicAccount, ShowPublicAccount)
admin.site.register(CraneOperatorDetailsModel, ShowCraneOperatorDetailsModel)
admin.site.register(IGPModelSequence, ShowIGPModelSequence)
admin.site.register(IGPModel, ShowIGPModel)
admin.site.register(CraneBillMainDate, ShowCraneBillMainDate)
admin.site.register(CraneBillSubDate, ShowCraneBillSubDate)
admin.site.register(PrivateAccountDetailsModel, ShowPrivateAccountDetailsModel)
admin.site.register(CommonBillCalculationModel, ShowCommonBillCalculationModel)