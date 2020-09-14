from django.shortcuts import render, redirect
from django.views import View
from dineshApp.models import (HouseRentModel, PublicAccountDetails, EBBillModel, PrivatePublicAccount)
from dineshApp.models import (CraneOperatorDetailsModel, IGPModel, IGPModelSequence)
from datetime import datetime, date
from dineshApp import views


# Create your views here.
class ViewHouseRent(views.HouseRent):
    template_name = "view-house_rent.html"

class ViewAccountDetails(views.AccountDetails):
    template_name = "view-account_details.html"
    
class ViewEBBill(views.EBBill):
    template_name = "view-eb-bill.html"

class ViewIGPCalculation(views.IGPCalculation):
    template_name = "view-igp.html"

class ViewCraneOperatorDetails(views.CraneOperatorDetails):
    template_name = "view-CraneOperatorDetails.html"

class ViewCraneCompanyBill(views.CraneCompanyBill):
    template_name = "view-crane-company-bill.html"

class ViewCraneMoreDetails(views.CraneMoreDetails):
    template_name = "view-crane_bill_more.html"

class ViewCraneOperatorDetailsEdit(views.CraneOperatorDetailsEdit):
    template_name = "view-CraneOperatorDetails.html"
    def post(self, request, pk):
        name = request.POST.get("name")
        leave_advance = request.POST.get("leave_advance")
        get_date = request.POST.get("date")
        get_date = datetime.strptime(get_date, "%Y-%m-%d")
        amount = float(request.POST.get("amount"))

        name, salary = name.split("-")[0].strip(), name.split("-")[1][2:-1]
        crane_operator_data = CraneOperatorDetailsModel.objects.get(pk=pk)
        if crane_operator_data.amount < amount:
            balance = crane_operator_data.balance - (abs(amount - crane_operator_data.amount))
        elif crane_operator_data.amount > amount:
            balance = crane_operator_data.balance + (abs(amount - crane_operator_data.amount))

        crane_operator_data.name = name
        crane_operator_data.leave_advance = leave_advance
        crane_operator_data.date = get_date
        crane_operator_data.amount = amount
        crane_operator_data.balance = balance
        crane_operator_data.save()
        return redirect("/ViewCraneOperatorDetails")

class ViewCraneOperatorDetailsDelete(View):
    template_name = "view-CraneOperatorDetails.html"
    def get(self, request, pk):
        crane_operator_data = CraneOperatorDetailsModel.objects.get(pk=pk)
        crane_operator_data.delete()
        return redirect("/ViewCraneOperatorDetails")
