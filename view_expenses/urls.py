from django.urls import path
from view_expenses import views
import inspect

# print(inspect.getsource(views.ViewAccountDetails))

urlpatterns = [
    path('', views.ViewHouseRent.as_view()),
    path('ViewAccountDetails', views.ViewAccountDetails.as_view()),
    path('ViewEBBill', views.ViewEBBill.as_view()),
    path('ViewIGPCalculation', views.ViewIGPCalculation.as_view()),
    path('ViewCraneOperatorDetails', views.ViewCraneOperatorDetails.as_view()),
    path('ViewCraneCompanyBill', views.ViewCraneCompanyBill.as_view()),
    path('ViewCraneMoreDetails/<int:pk>', views.ViewCraneMoreDetails.as_view()),
    path('ViewCraneOperatorDetailsEdit/<int:pk>', views.ViewCraneOperatorDetailsEdit.as_view()),
    path('ViewCraneOperatorDetailsDelete/<int:pk>', views.ViewCraneOperatorDetailsDelete.as_view()),
]