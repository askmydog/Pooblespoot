from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('meds/', views.MedListView.as_view(), name='meds'),
	path('meds/<int:pk>', views.MedDetailView.as_view(), name='med-detail'),
	path('patients/', views.PatientListView.as_view(), name='patients'),
	path('patients/<int:pk>', views.PatientDetailView.as_view(), name='patient-detail'),
	path('myscripts/', views.PrescribedMedsByUserListView.as_view(), name='my-prescribed'),
	path('meds/reconcile/', views.rec_meds_corpsman, name='rec-meds-corpsman'),
]