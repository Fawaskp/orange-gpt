from django.urls import path
from . import views


urlpatterns = [
    path('',views.gpt),
    # path('enquiry',views.enquiry)
]
