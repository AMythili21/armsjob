from django.shortcuts import render
from rest_framework import generics,filters
from .models import AgentSupplier
from .serializers import AgentSupplierSerializer
from .serializers import AgentNameSerializer
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
from .models import AgentSupplierRemarks
from .serializers import AgentSupplierRemarksSerializer
from .models import ManpowerSupplier
from .serializers import ManpowerSupplierSerializer
from .models import ManpowerSupplierRemarks
from .serializers import ManpowerSupplierRemarksSerializer,ManpowerSupplierNameSerializer
from .models import OverseasRecruitment,OverseasRecruitmentRemarks
from .serializers import OverseasRecruitmentSerializer,OverseasRecruitmentNameSerializer,OverseasRecruitmentRemarksSerializer
from .models import ClientEnquiry
from .serializers import ClientEnquirySerializer,ClientEnquiryNameSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Category
from .serializers import CategorySerializer

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # default
    page_size_query_param = 'page_size'  # allow client to set page_size
    max_page_size = 100  # optional: limit maximum page_size


class AgentSupplierListCreateView(generics.ListCreateAPIView):
    queryset = AgentSupplier.objects.all().order_by('-created_at')
    serializer_class = AgentSupplierSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['agent_supplier_id', 'name', 'mobile_no', 'whatsapp_no', 'email']
    pagination_class = CustomPageNumberPagination  # use dynamic pagination here

    def get_queryset(self):
        queryset = AgentSupplier.objects.filter(is_deleted=False).order_by('-created_at')
        filter_by = self.request.query_params.get('filter_by', 'all')

        today = now().date()

        if filter_by == 'today':
            queryset = queryset.filter(created_at__date=today)

        elif filter_by == 'yesterday':
            queryset = queryset.filter(created_at__date=today - timedelta(days=1))

        elif filter_by == 'last7days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=7))

        elif filter_by == 'last30days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=30))

        elif filter_by == 'thismonth':
            queryset = queryset.filter(
                created_at__year=today.year,
                created_at__month=today.month
            )

        elif filter_by == 'lastyear':
            queryset = queryset.filter(
                created_at__year=today.year - 1
            )

        # Status filter: true for active, false for inactive
        status_filter = self.request.query_params.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(status=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(status=False)


        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if not serializer.data:
                return Response({
                    "status": "error",
                    "message": "No records found for the selected filter",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

            return self.get_paginated_response({
                "status": "success",
                "message": "Agent/Supplier list fetched successfully",
                "data": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({
                "status": "error",
                "message": "No records found for the selected filter",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

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

    
class AgentSupplierUpdateView(generics.UpdateAPIView):
    queryset = AgentSupplier.objects.all()
    serializer_class = AgentSupplierSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Supports PATCH
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
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
        id = request.data.get('id')

        if not id:
            return Response({
                "status": "error",
                "message": "id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = AgentSupplier.objects.get(id=id)
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
    
class AgentPagination(PageNumberPagination):
    page_size = 10  # Number of candidates per page
    page_size_query_param = 'page_size'  # Optional: allows frontend to set size
    max_page_size = 100  # Optional: max limit
    

class AgentNameListView(generics.ListAPIView):
    queryset = AgentSupplier.objects.filter(is_deleted=False, status=True).order_by('id')
    serializer_class = AgentNameSerializer
    pagination_class = AgentPagination  # Optional

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']  # Enable search by name

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                "status": "success",
                "message": "Agent name list fetched successfully",
                "data": paginated_response.data.get('results', []),
                "count": paginated_response.data.get('count', 0),
                "next": paginated_response.data.get('next', None),
                "previous": paginated_response.data.get('previous', None)
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Agent name list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
#Agent remarks    
class AgentSupplierRemarksCreateView(generics.CreateAPIView):
    queryset = AgentSupplierRemarks.objects.all()
    serializer_class = AgentSupplierRemarksSerializer

#AgentDetails
class AgentSupplierDetailView(generics.RetrieveAPIView):
    queryset = AgentSupplier.objects.all()
    serializer_class = AgentSupplierSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Agent details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

#candidate
class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = CandidateSerializer
    parser_classes = (MultiPartParser, FormParser)
    search_fields = ['full_name','mobile_number','whatsapp_number','email']  # Customize as needed
    pagination_class = CustomPageNumberPagination  # use dynamic pagination here


    def get_queryset(self):
        queryset = Candidate.objects.filter(is_deleted=False).order_by('-created_at')
        filter_by = self.request.query_params.get('filter_by', 'all')

        today = now().date()

        if filter_by == 'today':
            queryset = queryset.filter(created_at__date=today)

        elif filter_by == 'yesterday':
            queryset = queryset.filter(created_at__date=today - timedelta(days=1))

        elif filter_by == 'last7days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=7))

        elif filter_by == 'last30days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=30))

        elif filter_by == 'thismonth':
            queryset = queryset.filter(
                created_at__year=today.year,
                created_at__month=today.month
            )

        elif filter_by == 'lastyear':
            queryset = queryset.filter(
                created_at__year=today.year - 1
            )

        
        # Status filtering (active/inactive)
        status_filter = self.request.query_params.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(status=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(status=False)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if not serializer.data:
                return Response({
                    "status": "error",
                    "message": "No candidates found for the selected filter",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

            return self.get_paginated_response({
                "status": "success",
                "message": "Candidate list fetched successfully",
                "data": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({
                "status": "error",
                "message": "No candidates found for the selected filter",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": "success",
            "message": "Candidate list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


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
    lookup_field = 'id'

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
    lookup_field = 'id'

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
    queryset = Candidate.objects.all().order_by('id')
    serializer_class = CandidateNameSerializer
    pagination_class = CandidatePagination  # Optional

    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name']  # Replace with the actual name field in your Candidate model

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
    lookup_field = 'id'

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
    

#Manpowersupplier

class ManpowerSupplierListCreateView(generics.ListCreateAPIView):
    queryset = ManpowerSupplier.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ManpowerSupplierSerializer
    parser_classes = (MultiPartParser, FormParser)
    search_fields = ['contact_person_name', 'mobile_no', 'email','company_name','whatsapp_no']  # Customize as needed
    pagination_class = CustomPageNumberPagination  # use dynamic pagination here

    def get_queryset(self):
        queryset = ManpowerSupplier.objects.filter(is_deleted=False).order_by('-created_at')
        filter_by = self.request.query_params.get('filter_by', 'all')
        today = now().date()

        if filter_by == 'today':
            queryset = queryset.filter(created_at__date=today)

        elif filter_by == 'yesterday':
            queryset = queryset.filter(created_at__date=today - timedelta(days=1))

        elif filter_by == 'last7days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=7))

        elif filter_by == 'last30days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=30))

        elif filter_by == 'thismonth':
            queryset = queryset.filter(
                created_at__year=today.year,
                created_at__month=today.month
            )

        elif filter_by == 'lastyear':
            queryset = queryset.filter(
                created_at__year=today.year - 1
            )

        # Status filtering (active/inactive)
        status_filter = self.request.query_params.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(status=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(status=False)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            if not serializer.data:
                return Response({
                    "status": "error",
                    "message": "No manpower suppliers found for the selected filter",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

            return self.get_paginated_response({
                "status": "success",
                "message": "Manpower supplier list fetched successfully",
                "data": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({
                "status": "error",
                "message": "No manpower suppliers found for the selected filter",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "status": "success",
            "message": "Manpower supplier list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Manpower supplier created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ManpowerSupplierRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ManpowerSupplier.objects.all()
    serializer_class = ManpowerSupplierSerializer
    lookup_field = 'id'  # Or 'supplier_id' if you prefer


    def update(self, request, *args, **kwargs):
        partial = True  # Force partial update regardless of request method
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'status': 'success',
                'message': 'Manpower supplier updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'failure',
                'message': f'Error updating supplier: {str(e)}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return Response({
                'status': 'success',
                'message': 'Manpower supplier deleted successfully (soft delete).',
                'data': None
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'failure',
                'message': f'Error deleting supplier: {str(e)}',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)


#manpowerremarks
class ManpowerSupplierRemarksCreateView(generics.CreateAPIView):
    queryset = ManpowerSupplierRemarks.objects.all()
    serializer_class = ManpowerSupplierRemarksSerializer

#Manpowerdetails
class ManpowerSupplierDetailView(generics.RetrieveAPIView):
    queryset = ManpowerSupplier.objects.all()
    serializer_class = ManpowerSupplierSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Manpower supplier details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

#manpowernamelist
class ManpowerSupplierPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ManpowerSupplierNameListView(generics.ListAPIView):
    queryset = ManpowerSupplier.objects.filter(is_deleted=False, status=True).order_by('id')
    serializer_class = ManpowerSupplierNameSerializer
    pagination_class = ManpowerSupplierPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['contact_person_name']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                "status": "success",
                "message": "Manpower supplier name list fetched successfully",
                "data": paginated_response.data.get('results', []),
                "count": paginated_response.data.get('count', 0),
                "next": paginated_response.data.get('next', None),
                "previous": paginated_response.data.get('previous', None)
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Manpower supplier name list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    

#OverseasRecruitment
class OverseasRecruitmentListCreateView(generics.ListCreateAPIView):
    queryset = OverseasRecruitment.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = OverseasRecruitmentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['overseas_recruitment_id', 'company_name', 'mobile_no', 'email_address','whatsapp_no']
    pagination_class = CustomPageNumberPagination  # use dynamic pagination here

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_by = self.request.query_params.get('filter_by', 'all')
        today = now().date()

        if filter_by == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif filter_by == 'yesterday':
            queryset = queryset.filter(created_at__date=today - timedelta(days=1))
        elif filter_by == 'last7days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=7))
        elif filter_by == 'last30days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=30))
        elif filter_by == 'thismonth':
            queryset = queryset.filter(created_at__year=today.year, created_at__month=today.month)
        elif filter_by == 'lastyear':
            queryset = queryset.filter(created_at__year=today.year - 1)
        
        # Status filtering (active/inactive)
        status_filter = self.request.query_params.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(status=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(status=False)


        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
    
        if not queryset.exists():
            return Response({
                "status": "error",
                "message": "No Overseas recruitment found for the selected filter.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)


        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "success",
                "message": "Overseas recruitment list fetched successfully",
                "data": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Overseas recruitment list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Overseas recruitment entry created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Required fields missing",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class OverseasRecruitmentUpdateView(generics.UpdateAPIView):
    queryset = OverseasRecruitment.objects.all()
    serializer_class = OverseasRecruitmentSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Overseas recruitment updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class OverseasRecruitmentDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        if not id:
            return Response({"status": "error", "message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = OverseasRecruitment.objects.get(id=id)
        except OverseasRecruitment.DoesNotExist:
            return Response({"status": "error", "message": "Recruitment entry not found"}, status=status.HTTP_404_NOT_FOUND)
        instance.is_deleted = True
        instance.save()
        return Response({"status": "success", "message": "Recruitment entry deleted successfully"}, status=status.HTTP_200_OK)


class OverseasRecruitmentDetailView(generics.RetrieveAPIView):
    queryset = OverseasRecruitment.objects.all()
    serializer_class = OverseasRecruitmentSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Recruitment entry fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

#OverseasRecruitment names list
class OverseasRecruitmentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class OverseasRecruitmentNameListView(generics.ListAPIView):
    queryset = OverseasRecruitment.objects.filter(is_deleted=False, status=True).order_by('id')
    serializer_class = OverseasRecruitmentNameSerializer
    pagination_class = OverseasRecruitmentPagination  # or AgentPagination if reusing

    filter_backends = [filters.SearchFilter]
    search_fields = ['contact_person_name']  # Allow search by name

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                "status": "success",
                "message": "Overseas recruitment list fetched successfully",
                "data": paginated_response.data.get('results', []),
                "count": paginated_response.data.get('count', 0),
                "next": paginated_response.data.get('next', None),
                "previous": paginated_response.data.get('previous', None)
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Overseas recruitment list fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

#OverseasRecruitmentRemarks
class OverseasRecruitmentRemarksCreateView(generics.CreateAPIView):
    queryset = OverseasRecruitmentRemarks.objects.all()
    serializer_class = OverseasRecruitmentRemarksSerializer

#ClientEnquiry
class ClientEnquiryListCreateView(generics.ListCreateAPIView):
    queryset = ClientEnquiry.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = ClientEnquirySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['client_enquiry_id', 'company_name', 'mobile_number', 'email']
    pagination_class = CustomPageNumberPagination  # use dynamic pagination here

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_by = self.request.query_params.get('filter_by', 'all')
        today = now().date()

        if filter_by == 'today':
            queryset = queryset.filter(created_at__date=today)
        elif filter_by == 'yesterday':
            queryset = queryset.filter(created_at__date=today - timedelta(days=1))
        elif filter_by == 'last7days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=7))
        elif filter_by == 'last30days':
            queryset = queryset.filter(created_at__date__gte=today - timedelta(days=30))
        elif filter_by == 'thismonth':
            queryset = queryset.filter(created_at__year=today.year, created_at__month=today.month)
        elif filter_by == 'lastyear':
            queryset = queryset.filter(created_at__year=today.year - 1)
        
        # Status filtering (active/inactive)
        status_filter = self.request.query_params.get('status')
        if status_filter == 'active':
            queryset = queryset.filter(status=True)
        elif status_filter == 'inactive':
            queryset = queryset.filter(status=False)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response({
                "status": "error",
                "message": "No client enquiries found for the selected filter.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "success",
                "message": "Client enquiries fetched successfully",
                "data": serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Client enquiries fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Client enquiry created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Required fields missing",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ClientEnquiryUpdateView(generics.UpdateAPIView):
    queryset = ClientEnquiry.objects.all()
    serializer_class = ClientEnquirySerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Client enquiry updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ClientEnquiryDeleteView(APIView):
    def post(self, request, *args, **kwargs):
        id = request.data.get('id')
        if not id:
            return Response({"status": "error", "message": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = ClientEnquiry.objects.get(id=id)
        except ClientEnquiry.DoesNotExist:
            return Response({"status": "error", "message": "Client enquiry not found"}, status=status.HTTP_404_NOT_FOUND)
        instance.is_deleted = True
        instance.save()
        return Response({"status": "success", "message": "Client enquiry deleted successfully"}, status=status.HTTP_200_OK)


class ClientEnquiryDetailView(generics.RetrieveAPIView):
    queryset = ClientEnquiry.objects.all()
    serializer_class = ClientEnquirySerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "message": "Client enquiry fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class ClientEnquiryPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ClientEnquiryNameListView(generics.ListAPIView):
    queryset = ClientEnquiry.objects.filter(is_deleted=False).order_by('id')
    serializer_class = ClientEnquiryNameSerializer
    pagination_class = ClientEnquiryPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['contact_person_name']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(serializer.data)
            return Response({
                "status": "success",
                "message": "Client enquiry names fetched successfully",
                "data": paginated_response.data.get('results', []),
                "count": paginated_response.data.get('count', 0),
                "next": paginated_response.data.get('next', None),
                "previous": paginated_response.data.get('previous', None)
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "Client enquiry names fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

#Agentupdatestatus

@method_decorator(csrf_exempt, name='dispatch')
class AgentSupplierStatusUpdateView(APIView):
    """
    Accepts form-data: id (int), boolean_value (true/false as string or boolean)
    """

    def post(self, request):
        agent_id = request.data.get('id')
        boolean_value = request.data.get('boolean_value')

        if agent_id is None or boolean_value is None:
            return Response({
                "status": "error",
                "message": "Both 'id' and 'boolean_value' are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            agent = AgentSupplier.objects.get(id=agent_id, is_deleted=False)

            # Convert boolean_value to proper boolean if it's a string
            if str(boolean_value).lower() in ['true', '1']:
                agent.status = True
            elif str(boolean_value).lower() in ['false', '0']:
                agent.status = False
            else:
                return Response({
                    "status": "error",
                    "message": "'boolean_value' must be true, false, 1, or 0."
                }, status=status.HTTP_400_BAD_REQUEST)

            agent.save()

            return Response({
                "status": "success",
                "message": f"Status updated to {'Active' if agent.status else 'Inactive'} successfully.",
                "data": {
                    "id": agent.id,
                    "name": agent.name,
                    "status": agent.status
                }
            }, status=status.HTTP_200_OK)

        except AgentSupplier.DoesNotExist:
            return Response({
                "status": "error",
                "message": "AgentSupplier not found."
            }, status=status.HTTP_404_NOT_FOUND)

#candidateupdatestatus

class CandidateStatusUpdateView(APIView):
    """
    Accepts form-data: id (int), boolean_value (true/false as string or boolean)
    Updates the 'status' field of the Candidate model.
    """

    def post(self, request):
        candidate_id = request.data.get('id')
        boolean_value = request.data.get('boolean_value')

        if candidate_id is None or boolean_value is None:
            return Response({
                "status": "error",
                "message": "Both 'id' and 'boolean_value' are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            candidate = Candidate.objects.get(id=candidate_id, is_deleted=False)

            # Convert boolean_value to proper boolean if it's a string
            if str(boolean_value).lower() in ['true', '1']:
                candidate.status = True
            elif str(boolean_value).lower() in ['false', '0']:
                candidate.status = False
            else:
                return Response({
                    "status": "error",
                    "message": "'boolean_value' must be true, false, 1, or 0."
                }, status=status.HTTP_400_BAD_REQUEST)

            candidate.save()

            return Response({
                "status": "success",
                "message": f"Status updated to {'Active' if candidate.status else 'Inactive'} successfully.",
                "data": {
                    "id": candidate.id,
                    "name": candidate.full_name,
                    "status": candidate.status
                }
            }, status=status.HTTP_200_OK)

        except Candidate.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Candidate not found."
            }, status=status.HTTP_404_NOT_FOUND)

#manpowerupdatestatus

class ManpowerSupplierStatusUpdateView(APIView):
    """
    Accepts form-data: id (int), boolean_value (true/false or 1/0 as string or boolean)
    Updates the 'status' field of the ManpowerSupplier model.
    """

    def post(self, request):
        supplier_id = request.data.get('id')
        boolean_value = request.data.get('boolean_value')

        if supplier_id is None or boolean_value is None:
            return Response({
                "status": "error",
                "message": "Both 'id' and 'boolean_value' are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            supplier = ManpowerSupplier.objects.get(id=supplier_id, is_deleted=False)

            if str(boolean_value).lower() in ['true', '1']:
                supplier.status = True
            elif str(boolean_value).lower() in ['false', '0']:
                supplier.status = False
            else:
                return Response({
                    "status": "error",
                    "message": "'boolean_value' must be true, false, 1, or 0."
                }, status=status.HTTP_400_BAD_REQUEST)

            supplier.save()

            return Response({
                "status": "success",
                "message": f"Status updated to {'Active' if supplier.status else 'Inactive'} successfully.",
                "data": {
                    "id": supplier.id,
                    "contact_person_name": supplier.contact_person_name,
                    "status": supplier.status
                }
            }, status=status.HTTP_200_OK)

        except ManpowerSupplier.DoesNotExist:
            return Response({
                "status": "error",
                "message": "ManpowerSupplier not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
#OverseasRecruitmentStatusUpdate

class OverseasRecruitmentStatusUpdateView(APIView):
    """
    Accepts form-data: id (int), boolean_value (true/false or 1/0 as string or boolean)
    Updates the 'status' field of the OverseasRecruitment model.
    """

    def post(self, request):
        recruitment_id = request.data.get('id')
        boolean_value = request.data.get('boolean_value')

        if recruitment_id is None or boolean_value is None:
            return Response({
                "status": "error",
                "message": "Both 'id' and 'boolean_value' are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            recruitment = OverseasRecruitment.objects.get(id=recruitment_id, is_deleted=False)

            if str(boolean_value).lower() in ['true', '1']:
                recruitment.status = True
            elif str(boolean_value).lower() in ['false', '0']:
                recruitment.status = False
            else:
                return Response({
                    "status": "error",
                    "message": "'boolean_value' must be true, false, 1, or 0."
                }, status=status.HTTP_400_BAD_REQUEST)

            recruitment.save()

            return Response({
                "status": "success",
                "message": f"Status updated to {'Active' if recruitment.status else 'Inactive'} successfully.",
                "data": {
                    "id": recruitment.id,
                    "contact_person_name": recruitment.contact_person_name,
                    "status": recruitment.status
                }
            }, status=status.HTTP_200_OK)

        except OverseasRecruitment.DoesNotExist:
            return Response({
                "status": "error",
                "message": "OverseasRecruitment not found."
            }, status=status.HTTP_404_NOT_FOUND)
        
#ClientEnquiryupdatestatus

class ClientEnquiryStatusUpdateView(APIView):
    """
    POST API to update the status field of ClientEnquiry
    Accepts form-data: id (int), boolean_value (true/false or 1/0)
    """

    def post(self, request):
        enquiry_id = request.data.get('id')
        boolean_value = request.data.get('boolean_value')

        if enquiry_id is None or boolean_value is None:
            return Response({
                "status": "error",
                "message": "Both 'id' and 'boolean_value' are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            enquiry = ClientEnquiry.objects.get(id=enquiry_id, is_deleted=False)

            # Convert boolean string to actual boolean
            if str(boolean_value).lower() in ['true', '1']:
                enquiry.status = True
            elif str(boolean_value).lower() in ['false', '0']:
                enquiry.status = False
            else:
                return Response({
                    "status": "error",
                    "message": "'boolean_value' must be true, false, 1, or 0."
                }, status=status.HTTP_400_BAD_REQUEST)

            enquiry.save()

            return Response({
                "status": "success",
                "message": f"Status updated to {'Active' if enquiry.status else 'Inactive'} successfully.",
                "data": {
                    "id": enquiry.id,
                    "contact_person_name": enquiry.contact_person_name,
                    "status": enquiry.status
                }
            }, status=status.HTTP_200_OK)

        except ClientEnquiry.DoesNotExist:
            return Response({
                "status": "error",
                "message": "ClientEnquiry not found."
            }, status=status.HTTP_404_NOT_FOUND)
        

#Category
# List & Create API (same as before, with custom response)
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(status=True, is_deleted=False)
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Category created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Required fields are missing or invalid",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# Retrieve API
class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(status=True, is_deleted=False)
    serializer_class = CategorySerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                "status": "success",
                "message": "Category retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "status": "error",
                "message": "Category not found"
            }, status=status.HTTP_404_NOT_FOUND)

# Update API
class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()  # <- allow access to all, not just status=True
    serializer_class = CategorySerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Category updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

# Delete API (soft delete)
class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.filter(status=True, is_deleted=False)
    serializer_class = CategorySerializer

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            return Response({
                "status": "success",
                "message": "Category deleted successfully"
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "status": "error",
                "message": "Category not found or already deleted"
            }, status=status.HTTP_404_NOT_FOUND)
        
# List API for Dropdown (without pagination)
class CategoryDropdownListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(status=True, is_deleted=False)
    serializer_class = CategorySerializer
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            if not queryset.exists():
                return Response({
                    "status": "error",
                    "message": "No categories found",
                    "data": []
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "status": "success",
                "message": "Categories retrieved successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": "Something went wrong",
                "data": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)