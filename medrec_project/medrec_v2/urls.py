from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from medrec_v2.views import MedInputView, postMedRec, AddMedView, MedicationList, MedicationDetail, MedDbUpload


app_name="medrec_v2"
urlpatterns = [
    path('', MedInputView.as_view(), name="med_input"),
    path('post/ajax/med_rec/', postMedRec.as_view(), name="post_medrec"),
    path('meds/', MedicationList.as_view(), name="med_list"),
    path('meds/<int:pk>/', MedicationDetail.as_view(), name="med_detail"),
    path('meds/add/', AddMedView.as_view(), name="add_med"),
    path('med_upload/', MedDbUpload.as_view(), name="med_upload"),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)