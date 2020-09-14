from django.shortcuts import render, redirect
from django.views import View
from dineshApp.models import HouseRentModel
from dineshApp.models import EBBillModel
from dineshApp.models import (PublicAccountDetails, PrivateAccountDetailsModel)
from dineshApp.models import (PrivatePublicAccount, CommonBillCalculationModel)
from dineshApp.models import (CraneOperatorDetailsModel, IGPModel, IGPModelSequence)
from datetime import date, datetime, timedelta
from dineshApp.forms import (CraneCompanyBillForm, IGPForm)
from dineshApp.models import (CraneBillMainDate, CraneBillSubDate, CompanyMasterModel)
from dineshApp.models import NotePadModel
from django.contrib import messages
from django.db.models import Sum
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class HouseRent(View):
    template_name = "house_rent.html"
    def get(self, request):
        house = ['2BHK - (20,000)', '1BHK - (10,000)']
        accounts = ['DineshRaj', 'DeviCrane', 'Cash on Hand']
        current_year = date.today().year
        house_rents_all = HouseRentModel.objects.all()
        
        get_year = request.GET.get("year")
        
        house_rent_year = list(set([ house.date.year for house in house_rents_all ]))
        house_rent_year.sort()

        if get_year is None:
            house_rents = HouseRentModel.objects.filter(date__year=current_year)
        else:
            house_rents = HouseRentModel.objects.filter(date__year=get_year)
            current_year = get_year

        house_rents = {
            "house_rents": house_rents,
            "houses": house,
            "accounts": accounts,
            "house_rent_year": house_rent_year,
            "current_year": current_year,
            }
        return render(request, template_name=self.template_name, context=house_rents)
    
    def post(self, request):
        date = request.POST.get('date')
        house = request.POST.get('house')
        rent = request.POST.get('rent')
        account = request.POST.get('account')
        print(date, house, rent, account)

        house_rents = HouseRentModel(date=date, house=house, rent_recieved=rent, account=account)
        house_rents.save()
        return redirect("/dinesh/")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class HouseRentEdit(View):
    template_name = "house_rent.html"
    def get(self, request, pk):
        house = ['2BHK - (20,000)', '1BHK - (10,000)']
        accounts = ['DineshRaj', 'DeviCrane', 'Cash on Hand']
        house_rents = HouseRentModel.objects.get(id=pk)
        house_rent_date = house_rents.date.strftime('%Y-%m-%d')

        house_rents = {
            "houses": house,
            "house_edit": house_rents,
            "accounts": accounts,
            "house_rent_date": house_rent_date,
        }

        return render(request, template_name=self.template_name, context=house_rents)
    
    def post(self, request, pk):
        date = request.POST.get('date')
        house = request.POST.get('house')
        rent = request.POST.get('rent')
        account = request.POST.get('account')
        
        house_rents = HouseRentModel.objects.get(id=pk)
        house_rents.date = date
        house_rents.house = house
        house_rents.rent_recieved = rent
        house_rents.account = account
        house_rents.save()

        return redirect("/dinesh/")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class HouseRentDelete(View):
    template_name = "house_rent.html"
    def get(self, request, pk):
        house_rent = HouseRentModel.objects.get(id=pk)
        house_rent.delete()
        return redirect("/dinesh/")

class EBBill(View):
    template_name = "eb-bill.html"
    def get(self, request):
        current_year = date.today().year
        eb_bill_all_data = EBBillModel.objects.all()
        get_year = request.GET.get("year")
        
        eb_bill_year = list(set([ eb.date.year for eb in eb_bill_all_data ]))
        eb_bill_year.sort()

        if get_year is None:
            eb_bill = EBBillModel.objects.filter(date__year=current_year)
        else:
            eb_bill = EBBillModel.objects.filter(date__year=get_year) 
            current_year = get_year        

        datas = {
            "houses": ['1BHK', '2BHK', '3BHK',],
            "eb_num": [4270, 4874, 4876],
            "yes_no": ['Yes', 'No'],
            "eb_bills": eb_bill,
            "eb_bill_year": eb_bill_year,
            "current_year": current_year
        }
        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request):
        date = request.POST.get("date")
        house = request.POST.get("house")
        eb_no = int(request.POST.get("eb_num")) if request.POST.get("eb_num") else 0
        amount = request.POST.get("amount")
        yes_no = request.POST.get("yes_no")

        eb_bill = EBBillModel(date=date, house=house, eb_no=eb_no, amount=amount, yes_no=yes_no)
        eb_bill.save()
        return redirect("/dinesh/EB-Bill")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class EBBillEdit(View):
    template_name = "eb-bill.html"
    def get(self, request, pk):
        eb_bill = EBBillModel.objects.get(id=pk)
        eb_bill_date = eb_bill.date.strftime('%Y-%m-%d')
        datas = {
            "houses": ['1BHK', '2BHK', '3BHK',],
            "eb_num": [4270, 4874, 4876],
            "yes_no": ['Yes', 'No'],
            "eb_bill": eb_bill,
            "eb_bill_date": eb_bill_date,
        }
        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request, pk):
        date = request.POST.get("date")
        house = request.POST.get("house")
        eb_no = int(request.POST.get("eb_num")) if request.POST.get("eb_num") else 0
        amount = request.POST.get("amount")
        yes_no = request.POST.get("yes_no")

        eb_bill = EBBillModel.objects.get(id=pk)
        eb_bill.date = date
        eb_bill.house = house
        eb_bill.eb_no = eb_no
        eb_bill.amount = amount
        eb_bill.yes_no = yes_no
        eb_bill.save()
        return redirect("/dinesh/EB-Bill")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class EBBillDelete(View):
    def get(self, request, pk):
        eb_bill = EBBillModel.objects.get(id=pk)
        eb_bill.delete()
        return redirect("/dinesh/EB-Bill")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class PublicAccountInitial(View):
    template_name = "publicaccount_initial.html"
    def get(self, request):
        ppa = PrivatePublicAccount.objects.all()
        bank_accounts = ["Devi Crane", "Indian Bank", "IDFC"]
        datas = {
            "ppa": ppa,
            "bank_accounts": bank_accounts,
        }
        return render(request, template_name=self.template_name, context=datas)

    def post(self, request):
        back_account = request.POST.get("account")
        amount = request.POST.get("amount")
        check = PrivatePublicAccount.objects.filter(bank_name=back_account)
        if check:
            bal_update = check.first()
            bal_update.balance = amount
            bal_update.save()
        else:
            pa = PrivatePublicAccount(bank_name=back_account, balance=amount)
            pa.save()
        return redirect("/dinesh/public-initial")

class AccountDetails(View):
    template_name = "account_details.html"
    def get(self, request):
        recieved_expense = ["Recieved", "Expense"]
        
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")

        current_balance = PrivatePublicAccount.objects.filter(bank_name="Devi Crane")
        if current_balance:
            current_balance = PrivatePublicAccount.objects.all().first()
        else:
            current_balance = ""
            
        if from_date is None:
            pub_acc_det = PublicAccountDetails.objects.all()[::-1][:10]
            first_data = pub_acc_det[0] if pub_acc_det else ""
        else:
            pub_acc_det = PublicAccountDetails.objects.filter(date__range=(from_date, to_date)).order_by('date')
            first_data = ""

        datas = {
            "recieved_expense": recieved_expense,
            "pub_acc_det": pub_acc_det,
            "current_balance": current_balance,
            "first_data": first_data,
        }
        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request):
        date = request.POST.get("date")
        recieved_expense = request.POST.get("recieved_expense")
        amount = float(request.POST.get('amount'))
        description = request.POST.get("description")
        check = PrivatePublicAccount.objects.filter(bank_name="Devi Crane")

        if check:
            if recieved_expense == "Recieved":
                current_balance = PrivatePublicAccount.objects.filter(bank_name="Devi Crane").first()
                recieve_amt = current_balance.balance + amount
                current_balance.balance = recieve_amt
                current_balance.save()

                pub_acc_det = PublicAccountDetails(date=date, recieved=amount, description=description, balance_history=recieve_amt)
                pub_acc_det.save()
            else:
                current_balance = PrivatePublicAccount.objects.filter(bank_name="Devi Crane").first()
                recieve_amt = current_balance.balance - amount
                current_balance.balance = recieve_amt
                current_balance.save()

                pub_acc_det = PublicAccountDetails(date=date, expense=amount, description=description, balance_history=recieve_amt)
                pub_acc_det.save()
        else:
            messages.info(request, "Please Add Initial Amount")

        return redirect('/dinesh/AccountDetails')

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class AccountDetailsDelete(View):
    def get(self, request, pk):
        pub_acc_det = PublicAccountDetails.objects.get(id=pk)
        pub_acc_det.delete()
        
        pub_acc_det = PublicAccountDetails.objects.all()

        if pub_acc_det:
            pub_acc_det = PublicAccountDetails.objects.first()
            pa = PrivatePublicAccount.objects.filter(bank_name="Devi Crane").first()
            pa.balance = pub_acc_det.balance_history
            pa.save()
        return redirect("/dinesh/AccountDetails")

class CraneOperatorDetails(View):
    template_name = "CraneOperatorDetails.html"
    def get(self, request):
        employees = ['Srinivasan - (16000)', 'Rathanam - (15000)']
        leave_advance = ['Leave', 'Advance', 'Salary']
        
        employee_names = [ employees[0].split("-")[0].strip(), employees[1].split("-")[0].strip(), ]

        emp_name = request.GET.get("emp-name")
        emp_date = request.GET.get("emp-date")
        remaining_salary = ""
        if emp_name is not None and emp_date is not None:
            emp_date = datetime.strptime(emp_date, "%Y-%m-%d")
            crane_operators = CraneOperatorDetailsModel.objects.filter(name=emp_name).filter(date__month=emp_date.month).filter(date__year=emp_date.year).order_by('balance')
            remaining_salary = crane_operators[0] if crane_operators else ""
        else:
            crane_operators = CraneOperatorDetailsModel.objects.filter(date__month=date.today().month).filter(date__year=date.today().year)[::-1]

        datas = {
            "employees": employees,
            "leave_advance": leave_advance,
            "crane_operators": crane_operators,
            "employee_names": employee_names,
            "remaining_salary": remaining_salary,
            "emp_name": emp_name,
        }
        return render(request, template_name=self.template_name, context=datas)

    def post(self, request):
        name = request.POST.get("name")
        leave_advance = request.POST.get("leave_advance")
        get_date = request.POST.get("date")
        get_date = datetime.strptime(get_date, "%Y-%m-%d")
        amount = request.POST.get("amount")

        name, salary = name.split("-")[0].strip(), name.split("-")[1][2:-1]
        details = CraneOperatorDetailsModel.objects.filter(name=name).filter(date__month=get_date.month).filter(date__year=get_date.year)
        
        if details:
            minus_amt = float(salary) - (sum([ detail.amount for detail in details if detail.leave_advance != "Salary" ]) + float(amount))
            operator = CraneOperatorDetailsModel(name=name, leave_advance=leave_advance, date=get_date, amount=amount, balance=minus_amt)
            operator.save()
        else:
            minus_amt = float(salary) - float(amount)
            operator = CraneOperatorDetailsModel(name=name, leave_advance=leave_advance, date=get_date, amount=amount, balance=minus_amt)
            operator.save()

        return redirect("/dinesh/CraneOperatorDetails")

class CraneOperatorDetailsEdit(View):
    template_name = "CraneOperatorDetails.html"
    def get(self, request, pk):
        crane_operator_data = CraneOperatorDetailsModel.objects.get(pk=pk)
        employees = ['Srinivasan - (16000)', 'Rathanam - (15000)']
        leave_advance = ['Leave', 'Advance', 'Salary']
        crane_operator_data_date = crane_operator_data.date.strftime('%Y-%m-%d')

        datas = {
            "crane_operator_data": crane_operator_data,
            "employees": employees,
            "leave_advance": leave_advance,
            "crane_operator_data_date": crane_operator_data_date,
        }

        return render(request, template_name=self.template_name, context=datas)
    
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
        return redirect("/dinesh/CraneOperatorDetails")

class CraneOperatorDetailsDelete(View):
    template_name = "CraneOperatorDetails.html"
    def get(self, request, pk):
        crane_operator_data = CraneOperatorDetailsModel.objects.get(pk=pk)
        crane_operator_data.delete()
        return redirect("/dinesh/CraneOperatorDetails")

class CraneCompanyBill(View):
    template_name = "crane-company-bill.html"
    def get(self, request):
        forms = CraneCompanyBillForm()
        company = CompanyMasterModel.objects.all()

        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")
        
        if from_date is not None and to_date is not None:
            main_date = CraneBillMainDate.objects.filter(main_date__range=(from_date, to_date))
            main_date = ( (md, CraneBillSubDate.objects.filter(main_date=md).aggregate(Sum("amount"))['amount__sum']) for md in main_date )
        else:
            main_date = CraneBillMainDate.objects.filter(main_date__month=date.today().month).filter(main_date__year=date.today().year)
            main_date = ( (md, CraneBillSubDate.objects.filter(main_date=md).aggregate(Sum("amount"))['amount__sum']) for md in main_date )
        
        datas = {
            "forms": forms,
            "main_date": main_date,
            "company": company,
        }
        return render(request, template_name=self.template_name, context=datas)

    def post(self, request):
        company = request.POST.get("company")
        main_date = request.POST.get("main_date")
        bill_number = request.POST.get("bill_number")
        md = CraneBillMainDate(company=company, main_date=main_date, bill_number=bill_number)
        md.save()

        cnt = 0
        
        while True:
            data1, data2, data3 = "sub_date"+'0'*cnt, "hours"+'0'*cnt, "amount"+'0'*cnt
            sub_date = request.POST.get(data1)
            hours = request.POST.get(data2)
            amount = request.POST.get(data3)

            if sub_date is None:
                break
            
            sd = CraneBillSubDate(main_date=md, sub_date=sub_date, hours=hours, amount=amount)
            sd.save()
            cnt = cnt + 1
        return redirect("/dinesh/CraneCompanyBill")

class CraneMoreDetails(View):
    template_name = "crane_bill_more.html"
    def get(self, request, pk):
        main_date = CraneBillMainDate.objects.get(id=pk)
        sub_dates = CraneBillSubDate.objects.filter(main_date=main_date)

        datas = {
            "company": main_date.company,
            "sub_dates": sub_dates,
        }
        return render(request, template_name=self.template_name, context=datas)

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class CraneBillDelete(View):
    def get(self, request, pk):
        crane = CraneBillMainDate.objects.get(id=pk)
        crane.delete()
        return redirect("/dinesh/CraneCompanyBill")

pdf_datas = {}

class IGPCalculation(View):
    template_name = 'igp.html'
    def get(self, request):
        forms = IGPForm()
        search_date = request.GET.get("search-date")

        if search_date is not None:
            search_date = datetime.strptime(search_date, "%Y-%m-%d")
            igp = IGPModel.objects.filter(date__month=search_date.month, date__year=search_date.year)
            bill_number = igp[0].seq_bill.seq_bill if igp else ""
            total_amount = sum([ ig.amount for ig in igp ])
            initial_date = date(year=search_date.year, month=search_date.month, day=1)
            pdf_datas["month"] = search_date.month
            pdf_datas["year"] = search_date.year
        else:
            igp = IGPModel.objects.filter(date__month=date.today().month, date__year=date.today().year)
            bill_number = igp[0].seq_bill.seq_bill if igp else ""
            total_amount = sum([ ig.amount for ig in igp ])
            initial_date = date(year=date.today().year, month=date.today().month, day=1)
            pdf_datas["month"] = date.today().month
            pdf_datas["year"] = date.today().year

        datas = {
            "forms": forms,
            "igp_data": igp,
            "bill_number": bill_number,
            "total_amount": total_amount,
            "initial_date": initial_date,
        }
        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request):
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        in_time = request.POST.get("in_time")
        out_time = request.POST.get("out_time")
        
        for io_time in (in_time, out_time):
            hh, mi = io_time.split(":")
            if int(hh) >= 24 or int(mi) > 60:
                messages.info(request, "Please provide a valid Hour/Minutes.")
                return redirect("/dinesh/IGPCalculation")

        day1 = datetime.strptime(start_date, '%Y-%m-%d').day
        day2 = datetime.strptime(end_date, '%Y-%m-%d').day
        
        hour1, minute1 = int(in_time.split(":")[0]), int(in_time.split(":")[1])
        hour2, minute2 = int(out_time.split(":")[0]), int(out_time.split(":")[1])
        
        t1 = timedelta(days=day1, hours=hour1, minutes=minute1)
        t2 = timedelta(days=day2, hours=hour2, minutes=minute2)
        day_diff = t2 - t1

        total_second = day_diff.total_seconds()
        
        hours = int(total_second/3600)
        minutes = int(total_second % 3600/60)

        if hours <= 2:
            if hours == 2 and minutes < 15:
                hours, minutes = 2, 0
            elif hours == 2 and (minutes >= 15 and minutes < 30):
                hours, minutes = 2, 30
            elif hours == 2 and (minutes >= 30 and minutes < 45):
                hours, minutes = 2, 30
            elif hours == 2 and minutes >= 45:
                hours = hours + 1
                minutes = 0
            else:
                hours = 2
                minutes = 0

        elif minutes >=15 and minutes < 30:
            minutes = 30
        elif minutes < 15:
            minutes = 0
        elif minutes >= 30 and minutes < 45:
            minutes = 30
        elif minutes >= 45:
            hours = hours + 1
            minutes = 0

        minimum_amount, hours_amount = 1300, 500

        if hours == 2 and minutes == 0:
            total_amount = minimum_amount
        elif hours == 2 and minutes == 30:
            total_amount = minimum_amount + (hours_amount/2)
        else:
            if hours > 2 and minutes == 0:
                total_amount = minimum_amount + ((hours - 2) * hours_amount)
            else:
                total_amount = minimum_amount + ((hours - 2) * hours_amount) + (hours_amount/2)

        start_day = datetime.strptime(start_date, '%Y-%m-%d')
        total_hours_minutes = str(hours) + '.' + str(minutes)
        igp_seq = IGPModelSequence.objects.filter(date__month=start_day.month).filter(date__year=start_day.year)
        igp_all_seq = IGPModelSequence.objects.all()
        
        if igp_all_seq:
            if igp_seq:
                igp = IGPModel(date=start_day, seq_bill=igp_seq[0], tot_hours=total_hours_minutes, amount=total_amount)
                igp.save()
            else:
                max_seq_bill_no = IGPModelSequence.objects.all().order_by('-seq_bill')[0].seq_bill + 3
                create_seq = IGPModelSequence(date=start_day, seq_bill=max_seq_bill_no)
                create_seq.save()
                new_seq_bill = IGPModelSequence.objects.all().order_by('-seq_bill')[0]
                igp = IGPModel(date=start_day, seq_bill=new_seq_bill, tot_hours=total_hours_minutes, amount=total_amount)
                igp.save()
        else:
            start_sequence = 7600
            create_seq = IGPModelSequence(date=start_day, seq_bill=start_sequence)
            create_seq.save()
            initial_create = IGPModelSequence.objects.all()[0]
            igp = IGPModel(date=start_day, seq_bill=initial_create, tot_hours=total_hours_minutes, amount=total_amount)
            igp.save()

        return redirect("/dinesh/IGPCalculation")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class IGPCalculationEdit(View):
    template_name = "igp_edit.html"
    def get(self, request, pk):
        igp = IGPModel.objects.get(id=pk)
        date = igp.date.strftime("%Y-%m-%d")
        
        datas = {
            "igp": igp,
            "date": date,
        }
        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request, pk):
        date = request.POST.get("date")
        hours = request.POST.get("hours")
        amount = request.POST.get("amount")

        igp = IGPModel.objects.get(id=pk)

        igp.date = date
        igp.tot_hours = hours
        igp.amount = amount
        igp.save()
        return redirect("/dinesh/IGPCalculation")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class IGPCalculationDelete(View):
    def get(self, request, pk):
        igp = IGPModel.objects.get(id=pk)
        igp.delete()
        return redirect("/dinesh/IGPCalculation")

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

class GeneratePDF(View):
    template_name = "pdf.html"
    def get(self, request):
        month, year = pdf_datas.get("month"), pdf_datas.get("year")
        igp_datas = IGPModel.objects.filter(date__month=month).filter(date__year=year)
        total = IGPModel.objects.filter(date__month=month).filter(date__year=year).aggregate(Sum("amount"))['amount__sum']
        generate_date = date(year=year, month=month, day=1)
        if igp_datas:
            bill_no = igp_datas.first().seq_bill.seq_bill
        datas = {
            "igp_datas": igp_datas,
            "total": total,
            "generate_date": generate_date,
            "bill_no": bill_no,
        }

        # pdf = render_to_pdf('pdf.html', datas)
        # return HttpResponse(pdf, content_type='application/pdf')
        return render(request, template_name=self.template_name, context=datas)

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class NotePad(View):
    template_name = "notepad.html"
    def get(self, request):
        get_date = request.GET.get("date")
        
        if get_date is None:
            notes = NotePadModel.objects.filter(date__month=date.today().month).filter(date__year=date.today().year)
        else:
            get_date = datetime.strptime(get_date, '%Y-%m-%d')
            notes = NotePadModel.objects.filter(date__month=get_date.month).filter(date__year=get_date.year)
        
        datas = {
            "notes": notes,
        }
        return render(request, template_name=self.template_name, context=datas)

    def post(self, request):
        notepad = request.POST.get("notepad")
        notes = NotePadModel(notes=notepad)
        notes.save()
        return redirect("/dinesh/notepad")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class NotePadDelete(View):
    def get(self, request, pk):
        notes = NotePadModel.objects.get(id=pk)
        notes.delete()
        return redirect("/dinesh/notepad")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class PrivateAccountDetails(View):
    template_name = "private_account_details.html"
    def get(self, request):
        private_accounts = ["Indian Bank", "IDFC",]
        recieved_expense = ["Recieved", "Expense"]
        
        search_bank_name = request.GET.get("bank-name")
        from_date = request.GET.get("from-date")
        to_date = request.GET.get("to-date")

        indian_balance = PrivatePublicAccount.objects.filter(bank_name="Indian Bank")
        idfc_balance = PrivatePublicAccount.objects.filter(bank_name="IDFC")

        indian_balance = indian_balance.first() if indian_balance else ""
        idfc_balance = idfc_balance.first() if idfc_balance else ""
        
        if from_date is None:
            pri_acc_det = PrivateAccountDetailsModel.objects.all()[::-1][:10]
            first_data = pri_acc_det[0] if pri_acc_det else ""
        else:
            pri_acc_det = PrivateAccountDetailsModel.objects.filter(bank_name=search_bank_name).filter(date__range=(from_date, to_date)).order_by('date')
            first_data = ""

        datas = {
            "private_accounts": private_accounts,
            "recieved_expense": recieved_expense,
            "pri_acc_det": pri_acc_det,
            "first_data": first_data,
            "indian_balance": indian_balance,
            "idfc_balance": idfc_balance,
        }

        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request):
        account = request.POST.get("account")
        date = request.POST.get("date")
        recieved_expense = request.POST.get("recieved_expense")
        amount = float(request.POST.get('amount'))
        description = request.POST.get("description")

        check = PrivatePublicAccount.objects.filter(bank_name=account)

        if check:
            if recieved_expense == "Recieved":
                current_balance = PrivatePublicAccount.objects.filter(bank_name=account).first()
                recieve_amt = current_balance.balance + amount
                current_balance.balance = recieve_amt
                current_balance.save()

                pub_acc_det = PrivateAccountDetailsModel(bank_name=account, date=date, recieved=amount, description=description, balance_history=recieve_amt)
                pub_acc_det.save()
            else:
                current_balance = PrivatePublicAccount.objects.filter(bank_name=account).first()
                recieve_amt = current_balance.balance - amount
                current_balance.balance = recieve_amt
                current_balance.save()

                pub_acc_det = PrivateAccountDetailsModel(bank_name=account, date=date, expense=amount, description=description, balance_history=recieve_amt)
                pub_acc_det.save()
        else:
            messages.info(request, "Please Add Initial Amount")

        return redirect('/dinesh/PrivateAccountDetails')        

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class PrivateAccountDetailsDelete(View):
    def get(self, request, pk):
        pub_acc_det = PrivateAccountDetailsModel.objects.get(id=pk)
        bank_name = pub_acc_det.bank_name
        pub_acc_det.delete()
        
        pub_acc_det = PrivateAccountDetailsModel.objects.filter(bank_name=bank_name)

        if pub_acc_det:
            pub_acc_det = PrivateAccountDetailsModel.objects.filter(bank_name=bank_name).first()
            pa = PrivatePublicAccount.objects.filter(bank_name=bank_name).first()
            pa.balance = pub_acc_det.balance_history
            pa.save()
        return redirect("/dinesh/PrivateAccountDetails")

common_bill_pdf = {}

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class CommonBillCalculation(View):
    template_name = "common-bill-calculation.html"
    def get(self, request):
        company_name = request.GET.get("comp-name")
        search_date = request.GET.get("search-date")
        company = ( com for com in set(( comp.company_name for comp in CommonBillCalculationModel.objects.all() )) )

        if company_name is not None:
            pdf = 1
            bill_calculate = CommonBillCalculationModel.objects.filter(company_name=company_name).filter(bill_date=search_date)
            bill_num = bill_calculate.first().bill_number if bill_calculate else ""
            common_bill_pdf["company"] = company_name
            common_bill_pdf["date"] = search_date
        else:
            pdf = 0
            bill_calculate = CommonBillCalculationModel.objects.filter(bill_date__month=date.today().month).filter(bill_date__year=date.today().year)[::-1]
            bill_num = ""

        datas = {
            "bill_calculate": bill_calculate,
            "show_pdf": pdf,
            "company": company,
            "bill_num": bill_num,
            "search_date": search_date,
        }
        return render(request, template_name=self.template_name, context=datas)

    def post(self, request):
        company_name = request.POST.get("name")
        bill_date = request.POST.get("bill_date")
        bill_number = request.POST.get("bill_number")
        start_date = request.POST.get("start_date")
        in_time = request.POST.get("in_time")
        end_date = request.POST.get("end_date")
        out_time = request.POST.get("out_time") 

        for io_time in (in_time, out_time):
            hh, mi = io_time.split(":")
            if int(hh) >= 24 or int(mi) > 60:
                messages.info(request, "Please provide a valid Hour/Minutes.")
                return redirect("/dinesh/CommonBillCalculation")

        day1 = datetime.strptime(start_date, '%Y-%m-%d').day
        day2 = datetime.strptime(end_date, '%Y-%m-%d').day
        
        hour1, minute1 = int(in_time.split(":")[0]), int(in_time.split(":")[1])
        hour2, minute2 = int(out_time.split(":")[0]), int(out_time.split(":")[1])
        
        t1 = timedelta(days=day1, hours=hour1, minutes=minute1)
        t2 = timedelta(days=day2, hours=hour2, minutes=minute2)
        day_diff = t2 - t1

        total_second = day_diff.total_seconds()
        
        hours = int(total_second/3600)
        minutes = int(total_second % 3600/60)

        if hours <= 2:
            if hours == 2 and minutes < 15:
                hours, minutes = 2, 0
            elif hours == 2 and (minutes >= 15 and minutes < 30):
                hours, minutes = 2, 30
            elif hours == 2 and (minutes >= 30 and minutes < 45):
                hours, minutes = 2, 30
            elif hours == 2 and minutes >= 45:
                hours = hours + 1
                minutes = 0
            else:
                hours = 2
                minutes = 0

        elif minutes >=15 and minutes < 30:
            minutes = 30
        elif minutes < 15:
            minutes = 0
        elif minutes >= 30 and minutes < 45:
            minutes = 30
        elif minutes >= 45:
            hours = hours + 1
            minutes = 0

        minimum_amount, hours_amount = 1300, 500

        if hours == 2 and minutes == 0:
            total_amount = minimum_amount
        elif hours == 2 and minutes == 30:
            total_amount = minimum_amount + (hours_amount/2)
        else:
            if hours > 2 and minutes == 0:
                total_amount = minimum_amount + ((hours - 2) * hours_amount)
            else:
                total_amount = minimum_amount + ((hours - 2) * hours_amount) + (hours_amount/2)
        
        start_day = datetime.strptime(start_date, '%Y-%m-%d')
        total_hours_minutes = str(hours) + '.' + str(minutes)
       
        bill_calculate = CommonBillCalculationModel(company_name=company_name, bill_date=bill_date, bill_number=bill_number, tot_hours=total_hours_minutes, amount=total_amount)
        bill_calculate.save()
        return redirect("/dinesh/CommonBillCalculation")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class CommonBillCalculationEdit(View):
    template_name = "common_calculation_edit.html"
    def get(self, request, pk):
        company_details = CommonBillCalculationModel.objects.get(id=pk)
        bill_date = company_details.bill_date.strftime("%Y-%m-%d")
        
        data = {
            "company_details": company_details,
            "bill_date": bill_date,
        }
        return render(request, template_name=self.template_name, context=data)

    def post(self, request, pk):
        bill_number = request.POST.get("bill_number")
        bill_date = request.POST.get("bill_date")
        company_name = request.POST.get("comp_name")
        tot_hours = request.POST.get("tot_hours")
        amount = request.POST.get("amount")
        company_details = CommonBillCalculationModel.objects.get(id=pk)

        company_details.bill_number = bill_number
        company_details.bill_date = bill_date
        company_details.company_name = company_name
        company_details.tot_hours = tot_hours
        company_details.amount = amount
        company_details.save()
        return redirect("/dinesh/CommonBillCalculation")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class CommonBillCalculationDelete(View):
    def get(self, request, pk):
        company = CommonBillCalculationModel.objects.get(id=pk)
        company.delete()
        return redirect("/dinesh/CommonBillCalculation")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class CommonBillPDF(View):
    template_name = "common-bill-pdf.html"
    def get(self, request):
        company_name, date = common_bill_pdf.get("company"), common_bill_pdf.get("date")
        company = CommonBillCalculationModel.objects.filter(company_name=company_name, bill_date=date) 
        total = CommonBillCalculationModel.objects.filter(company_name=company_name, bill_date=date).aggregate(Sum("amount"))['amount__sum']
        bill_no = company.first().bill_number if company else ""
        datas = {
            "company": company,
            "total": total,
            "generate_date": date,
            "bill_no": bill_no,
            "company_name": company_name,
        }     
        return render(request, template_name=self.template_name, context=datas)       

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class CompanyMaster(View):
    template_name = "company_master.html"
    def get(self, request):
        companies = CompanyMasterModel.objects.all()
        datas = {
            "companies": companies,
        }
        return render(request, template_name=self.template_name, context=datas)
    
    def post(self, request):
        company_name = request.POST.get("company_name")
        company = CompanyMasterModel(company_name=company_name)
        company.save()
        return redirect("/dinesh/CompanyMaster")

@method_decorator(login_required(login_url="/dinesh/login"), name='dispatch')
class CompanyMasterDelete(View):
    def get(self, request, pk):
        company = CompanyMasterModel.objects.get(id=pk)
        company.delete()
        return redirect("/dinesh/CompanyMaster") 

class AdminLogin(View):
    template_name = "login.html"
    def get(self, request):
        return render(request, template_name=self.template_name)
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/dinesh")
        else:
            data = {"error": "Username [or] Password Incorrect"}
            return render(request, "login.html", context=data)
        
class AdminLogout(View):
    def get(self, request):
        logout(request)
        return redirect("/")
