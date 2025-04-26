from django.urls import path
from .views import AgentSupplierListCreateView,AgentSupplierUpdateView,AgentSupplierDeleteView
from .views import CandidateListCreateView, CandidateUpdateView, CandidateDeleteView,CandidateNameListView,CandidateDetailView


urlpatterns = [
    path('agents/',AgentSupplierListCreateView.as_view()),
    path('agents/update/', AgentSupplierUpdateView.as_view(), name='agent-supplier-update'),
    path('agents/delete/', AgentSupplierDeleteView.as_view(), name='agent-supplier-delete'),
    path('candidates/', CandidateListCreateView.as_view(), name='candidate-list-create'),
    path('candidates/update/<int:candidate_id>/', CandidateUpdateView.as_view(), name='candidate-update'),
    path('candidates/delete/<int:candidate_id>/', CandidateDeleteView.as_view(), name='candidate-delete'),
    path('candidates/names/', CandidateNameListView.as_view(), name='candidate-name-list'),
     path('candidates/<int:candidate_id>/', CandidateDetailView.as_view(), name='candidate-detail'),


]
