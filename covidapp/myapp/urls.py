from django.urls import path
from . import views

urlpatterns = [
   
    path('', views.render_data_view, name = 'covid_data'),
    path('export_data_to_csv/', views.export_data_to_csv, name='export_data_to_csv')
    
    
]