from django.shortcuts import render
from rest_framework import generics,filters
from .models import AgentSupplier
from .serializers import AgentSupplierSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import Candidate
from .serializers import CandidateSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CandidateNameSerializer
from rest_framework.pagination import PageNumberPagination
from .models import CandidateRemarks
from .serializers import CandidateRemarksSerializer



class AgentSupplierListCreateView(generics.ListCreateAPIView):
    queryset = AgentSupplier.objects.all().order_by('-created_at')
    serializer_class = AgentSupplierSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['agent_supplier_id', 'name', 'mobile_no', 'whatsapp_no', 'email']

    def get_queryset(self):
        queryset = AgentSupplier.objects.filter(is_deleted=False).order_by('-created_at')
        filter_by = self.request.query_params.get('filter_by', 'all')

        today = now().date()

        if filter_by == 'today':
            queryset = queryset.filter(created_at__date=today)

        elif filter_by == 'yesterday':
            queryset = queryset.filter(created_at__date=today - timedelta(days=1))

        elif filter_by == 'last_7_days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=7))

        elif filter_by == 'last_30_days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=30))

        elif filter_by == 'this_month':
            queryset = queryset.filter(
                created_at__year=today.year,
                created_at__month=today.month
            )

        elif filter_by == 'last_year':
            queryset = queryset.filter(
                created_at__year=today.year - 1
            )

        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())  # Apply search filter here
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "success",
                "message": "Agent/Supplier list fetched successfully",
                "data": serializer.data
            })
    
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Agent/Supplier list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Agent/Supplier created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Required Fields",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    
class AgentSupplierUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        agent_supplier_id = request.data.get('agent_supplier_id')

        if not agent_supplier_id:
            return Response({
                "status": "error",
                "message": "agent_supplier_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = AgentSupplier.objects.get(agent_supplier_id=agent_supplier_id)
        except AgentSupplier.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Agent/Supplier not found"
            }, status=status.HTTP_404_NOT_FOUND)

        # Partial update: only update fields provided
        serializer = AgentSupplierSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Agent/Supplier updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class AgentSupplierDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        agent_supplier_id = request.data.get('agent_supplier_id')

        if not agent_supplier_id:
            return Response({
                "status": "error",
                "message": "agent_supplier_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = AgentSupplier.objects.get(agent_supplier_id=agent_supplier_id)
        except AgentSupplier.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Agent/Supplier not found"
            }, status=status.HTTP_404_NOT_FOUND)

        instance.is_deleted = True
        instance.save()

        return Response({
            "status": "success",
            "message": "Agent/Supplier deleted successfully"
        }, status=status.HTTP_200_OK)


#candidate
class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = CandidateSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Candidate created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class CandidateUpdateView(generics.UpdateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    lookup_field = 'candidate_id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # for PATCH support
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({
            "status": "success",
            "message": "Candidate updated successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)



class CandidateDeleteView(generics.DestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    lookup_field = 'candidate_id'

    def destroy(self, request, *args, **kwargs):
        candidate = self.get_object()
        candidate.is_deleted = True
        candidate.save()
        return Response({
            "status": "success",
            "message": "Candidate deleted successfully"
        }, status=status.HTTP_200_OK)
    
class CandidatePagination(PageNumberPagination):
    page_size = 10  # Number of candidates per page
    page_size_query_param = 'page_size'  # Optional: allows frontend to set size
    max_page_size = 100  # Optional: max limit

class CandidateNameListView(generics.ListAPIView):
    queryset = Candidate.objects.all().order_by('candidate_id')
    serializer_class = CandidateNameSerializer
    pagination_class = CandidatePagination  # Optional if you want pagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                "status": "success",
                "message": "Candidate name list fetched successfully",
                "data": paginated_response.data.get('results', []),
                "count": paginated_response.data.get('count', 0),
                "next": paginated_response.data.get('next', None),
                "previous": paginated_response.data.get('previous', None)
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Candidate name list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class CandidateDetailView(generics.RetrieveAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    lookup_field = 'candidate_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the candidate object
        serializer = self.get_serializer(instance)  # Serialize the object
        return Response({
            "status": "success",
            "message": "Candidate details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

#CandidateRemarks
    
class CandidateRemarksCreateView(generics.CreateAPIView):
    queryset = CandidateRemarks.objects.all()
    serializer_class = CandidateRemarksSerializer

