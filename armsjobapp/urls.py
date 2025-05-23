from django.urls import path
from .views import AgentSupplierListCreateView,AgentSupplierUpdateView,AgentSupplierDeleteView,AgentNameListView,AgentSupplierRemarksCreateView,AgentSupplierDetailView,AgentSupplierStatusUpdateView
from .views import CandidateListCreateView, CandidateUpdateView, CandidateDeleteView,CandidateNameListView,CandidateDetailView,CandidateRemarksCreateView,CandidateStatusUpdateView
from armsjob.urls import api_root
from .views import ManpowerSupplierListCreateView, ManpowerSupplierRetrieveUpdateDeleteView,ManpowerSupplierRemarksCreateView,ManpowerSupplierDetailView,ManpowerSupplierNameListView,ManpowerSupplierStatusUpdateView
from .views import OverseasRecruitmentListCreateView,OverseasRecruitmentDeleteView,OverseasRecruitmentDetailView,OverseasRecruitmentUpdateView,OverseasRecruitmentNameListView,OverseasRecruitmentRemarksCreateView,OverseasRecruitmentStatusUpdateView
from .views import ClientEnquiryListCreateView,ClientEnquiryUpdateView,ClientEnquiryDeleteView,ClientEnquiryDetailView,ClientEnquiryNameListView,ClientEnquiryStatusUpdateView
from .views import CategoryListCreateAPIView,CategoryRetrieveAPIView,CategoryUpdateAPIView,CategoryDeleteAPIView,CategoryDropdownListAPIView

urlpatterns = [
    path('', api_root),  # Handles root `/`
    path('agents/',AgentSupplierListCreateView.as_view()),
    path('agents/update/<int:id>/', AgentSupplierUpdateView.as_view(), name='agent-supplier-update'),
    path('agents/delete/', AgentSupplierDeleteView.as_view(), name='agent-supplier-delete'),
    path('agents/name-list/', AgentNameListView.as_view(), name='agent-name-list'),
    path('agents/<int:id>/', AgentSupplierDetailView.as_view(), name='agent-detail'),
    path('agents/remarks/create/', AgentSupplierRemarksCreateView.as_view(), name='agent-remark-create'),
    path('agents/update-status/', AgentSupplierStatusUpdateView.as_view(), name='agent-update-status'),
    path('candidates/', CandidateListCreateView.as_view(), name='candidate-list-create'),
    path('candidates/update/<int:id>/', CandidateUpdateView.as_view(), name='candidate-update'),
    path('candidates/delete/<int:id>/', CandidateDeleteView.as_view(), name='candidate-delete'),
    path('candidates/names/', CandidateNameListView.as_view(), name='candidate-name-list'),
    path('candidates/<int:id>/', CandidateDetailView.as_view(), name='candidate-detail'),
    path('candidates/update-status/', CandidateStatusUpdateView.as_view(), name='candidate-update-status'),
    path('remarks/create/', CandidateRemarksCreateView.as_view(), name='candidate-remark-create'),
    path('manpower-suppliers/', ManpowerSupplierListCreateView.as_view(), name='manpower-supplier-list-create'),
    path('manpower-suppliers/<int:id>/', ManpowerSupplierRetrieveUpdateDeleteView.as_view(), name='manpower-supplier-detail'),
    path('manpower/<int:id>/', ManpowerSupplierDetailView.as_view(), name='manpower-detail'),
    path('manpower-suppliers/remarks/create/', ManpowerSupplierRemarksCreateView.as_view(), name='manpower-remark-create'),
    path('manpower-suppliers/names-list/', ManpowerSupplierNameListView.as_view(), name='manpower-names-list'),
    path('manpower-suppliers/update-status/', ManpowerSupplierStatusUpdateView.as_view(), name='manpower-supplier-update-status'),
    path('recruitments/', OverseasRecruitmentListCreateView.as_view()),
    path('recruitments/update/<int:id>/', OverseasRecruitmentUpdateView.as_view(), name='recruitment-update'),
    path('recruitments/delete/', OverseasRecruitmentDeleteView.as_view(), name='recruitment-delete'),
    path('recruitments/<int:id>/', OverseasRecruitmentDetailView.as_view(), name='recruitment-detail'),
    path('recruitments/names/', OverseasRecruitmentNameListView.as_view(), name='recruitment-names'),
    path('recruitments/remarks/create/', OverseasRecruitmentRemarksCreateView.as_view(), name='recruitment-remarks-create'),
    path('recruitments/update-status/', OverseasRecruitmentStatusUpdateView.as_view(), name='overseas-recruitment-update-status'),
    path('client-enquiries/', ClientEnquiryListCreateView.as_view()),
    path('client-enquiries/update/<int:id>/', ClientEnquiryUpdateView.as_view(), name='client-enquiry-update'),
    path('client-enquiries/delete/', ClientEnquiryDeleteView.as_view(), name='client-enquiry-delete'),
    path('client-enquiries/<int:id>/', ClientEnquiryDetailView.as_view(), name='client-enquiry-detail'),
    path('client-enquiries/names/', ClientEnquiryNameListView.as_view(), name='client-enquiry-names'),
    path('client-enquiries/update-status/', ClientEnquiryStatusUpdateView.as_view(), name='client-enquiry-update-status'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveAPIView.as_view(), name='category-detail'),
    path('categories/update/<int:pk>/', CategoryUpdateAPIView.as_view(), name='category-update'),
    path('categories/delete/<int:pk>/', CategoryDeleteAPIView.as_view(), name='category-delete'),
    path('categories/dropdown/', CategoryDropdownListAPIView.as_view(), name='category-dropdown-list'),

]
