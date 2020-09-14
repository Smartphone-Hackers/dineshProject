from django import forms
from dineshApp.models import CompanyMasterModel

class DateInput(forms.DateInput):
    input_type = "date"

class TimeInput(forms.TimeInput):
    input_type = "time"

class CraneCompanyBillForm(forms.Form):
    main_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    bill_number = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))
    sub_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    hours = forms.CharField(widget=forms.TextInput(attrs={"class": 'form-control',}))
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control"}))

class IGPForm(forms.Form):
    start_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    in_time = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "24:00", "pattern": "[0-9]+:[0-9]+"}))
    end_date = forms.DateField(widget=DateInput(attrs={"class": "form-control"}))
    out_time = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "24:00", "pattern": "[0-9]+:[0-9]+"}))
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Amount"}))