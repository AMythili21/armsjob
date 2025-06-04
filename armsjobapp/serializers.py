from rest_framework import serializers
from .models import AgentSupplier,AgentSupplierRemarks
from .models import Candidate,CandidateRemarks
from .models import ManpowerSupplier,ManpowerSupplierRemarks
from .models import OverseasRecruitment
from .models import ClientEnquiry
from .models import OverseasRecruitmentRemarks
from .models import Category

#AgentRemarks create 

class AgentSupplierRemarksSerializer(serializers.ModelSerializer):
    agent_supplier_id = serializers.IntegerField(write_only=True)
    agent_supplier_name = serializers.CharField(source='agent_supplier.name', read_only=True)

    class Meta:
        model = AgentSupplierRemarks
        fields = ['id', 'agent_supplier_id', 'remark', 'agent_supplier_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        agent_supplier_id = validated_data.pop('agent_supplier_id')
        remark_instance = AgentSupplierRemarks.objects.create(agent_supplier_id=agent_supplier_id, **validated_data)
        return remark_instance


#Agent
class AgentSupplierSerializer(serializers.ModelSerializer):
    agent_remarks = AgentSupplierRemarksSerializer(many=True, read_only=True)
    status = serializers.BooleanField(default=True)
    # <-- Must declare this before class Meta!
    supply_category_names = serializers.SerializerMethodField()

    class Meta:
        model = AgentSupplier
        fields = [
            'id',
            'agent_supplier_id',
            'name',
            'mobile_no',
            'whatsapp_no',
            'email',
            'can_recruit',
            'associated_earlier',
            'can_supply_manpower',
            'supply_categories',
            'supply_category_names',
            'quantity_estimates',
            'areas_covered',
            'additional_notes',
            'is_deleted',
            'status',
            'created_at',
            'agent_remarks',
        ]

    def create(self, validated_data):
        # force status=True on create
        validated_data['status'] = True
        return super().create(validated_data)

    def get_supply_category_names(self, obj):
        """
        Reads the CSV in obj.supply_categories,
        looks up active, non-deleted Category rows,
        and returns a comma-joined string of their .category values.
        """
        s = obj.supply_categories or ""
        # split on commas, filter out non-digits, convert to ints
        try:
            ids = [int(pk) for pk in s.split(',') if pk.strip().isdigit()]
        except ValueError:
            return ""
        # query the Category table
        qs = Category.objects.filter(id__in=ids, status=True, is_deleted=False).order_by('id')
        names = qs.values_list('category', flat=True)
        return ", ".join(names)

class AgentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSupplier
        fields = ['id','name']



#Remarks create 
class CandidateRemarksSerializer(serializers.ModelSerializer):
    candidate_id = serializers.IntegerField(write_only=True)
    candidate_full_name = serializers.CharField(source='candidate.full_name', read_only=True)


    class Meta:
        model = CandidateRemarks
        fields = ['id', 'candidate_id','remark', 'candidate_full_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        candidate_id = validated_data.pop('candidate_id')
        remark_instance = CandidateRemarks.objects.create(candidate_id=candidate_id, **validated_data)
        return remark_instance


#Candidate
class CandidateSerializer(serializers.ModelSerializer):
    remarks = CandidateRemarksSerializer(many=True, read_only=True)
    status = serializers.BooleanField(default=True)
    # <-- Declare before Meta
    category_names = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = [
            'id',
            'candidate_id',
            'full_name',
            'mobile_number',
            'whatsapp_number',
            'email',
            'nationality',
            'current_location',
            'visa_type',
            'visa_expiry_date',
            'availability_to_join',
            'position_applying_for',
            'category',
            'category_names',       # ← NEW field
            'other_category',
            'uae_experience_years',
            'skills_tasks',
            'preferred_work_location',
            'expected_salary',
            'upload_cv',
            'photo_upload',
            'relevant_docs1',
            'relevant_docs2',
            'relevant_docs3',
            'languages_spoken',
            'preferred_work_type',
            'currently_employed',
            'additional_notes',
            'referral_name',
            'referral_contact',
            'status',
            'is_deleted',
            'created_at',
            'remarks',
        ]
        read_only_fields = ['candidate_id']

    def create(self, validated_data):
        validated_data['status'] = True
        return super().create(validated_data)

    def get_category_names(self, obj):
        """
        If obj.category is a CSV of IDs (e.g. "1,2,3"), split it,
        look up active/non-deleted Category rows, and join their
        .category strings into one comma-separated result.
        """
        raw = obj.category or ""
        ids = [int(pk) for pk in raw.split(',') if pk.strip().isdigit()]
        qs = Category.objects.filter(
            id__in=ids,
            status=True,
            is_deleted=False
        ).order_by('id')
        names = qs.values_list('category', flat=True)
        return ", ".join(names)


#Candidate name list
class CandidateNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id','full_name']  # Only show name
  

#ManpowerSupplierRemarksSerializer
class ManpowerSupplierRemarksSerializer(serializers.ModelSerializer):
    manpower_supplier_id = serializers.IntegerField(write_only=True)
    manpower_supplier_name = serializers.CharField(source='manpower_supplier.name', read_only=True)

    class Meta:
        model = ManpowerSupplierRemarks
        fields = ['id', 'manpower_supplier_id', 'remark', 'manpower_supplier_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        manpower_supplier_id = validated_data.pop('manpower_supplier_id')
        return ManpowerSupplierRemarks.objects.create(manpower_supplier_id=manpower_supplier_id, **validated_data)


#Manpower

class ManpowerSupplierSerializer(serializers.ModelSerializer):
    manpower_remarks = ManpowerSupplierRemarksSerializer(many=True, read_only=True)
    status = serializers.BooleanField(default=True)
    # declare before Meta
    categories_available_names = serializers.SerializerMethodField()

    class Meta:
        model = ManpowerSupplier
        fields = [
            'id',
            'supplier_id',
            'company_name',
            'contact_person_name',
            'mobile_no',
            'whatsapp_no',
            'email',
            'office_location',
            'categories_available',        # original CSV field
            'categories_available_names',  # ← new
            'quantity_per_category',
            'trade_license',
            'company_license',
            'previous_experience',
            'worked_with_arms_before',
            'comments',
            'is_deleted',
            'status',
            'created_at',
            'manpower_remarks',
        ]

    def create(self, validated_data):
        validated_data['status'] = True
        return super().create(validated_data)

    def get_categories_available_names(self, obj):
        """
        Reads obj.categories_available (e.g. "1,2,3"),
        looks up active/non-deleted Category rows,
        and returns their .category values joined by commas.
        """
        raw = obj.categories_available or ""
        # split IDs, filter, cast to int
        ids = [int(pk) for pk in raw.split(',') if pk.strip().isdigit()]
        qs = Category.objects.filter(
            id__in=ids,
            status=True,
            is_deleted=False
        ).order_by('id')
        names = qs.values_list('category', flat=True)
        return ", ".join(names)


#Manpowernamelist
class ManpowerSupplierNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManpowerSupplier
        fields = ['id','contact_person_name']  # Include only what's needed

#OverseasRecruitment Remarks
class OverseasRecruitmentRemarksSerializer(serializers.ModelSerializer):
    overseas_recruitment_id = serializers.IntegerField(write_only=True)
    company_name = serializers.CharField(source='overseas_recruitment.company_name', read_only=True)

    class Meta:
        model = OverseasRecruitmentRemarks
        fields = ['id', 'overseas_recruitment_id', 'remark', 'company_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        recruitment_id = validated_data.pop('overseas_recruitment_id')
        return OverseasRecruitmentRemarks.objects.create(overseas_recruitment_id=recruitment_id, **validated_data)

#OverseasRecruitment
class OverseasRecruitmentSerializer(serializers.ModelSerializer):
    recruitment_remarks = OverseasRecruitmentRemarksSerializer(many=True, read_only=True)
    status = serializers.BooleanField(default=True)
    categories_you_can_provide_names = serializers.SerializerMethodField()  # New field

    class Meta:
        model = OverseasRecruitment
        fields = [
            'id',
            'overseas_recruitment_id',
            'company_name',
            'country',
            'contact_person_name',
            'mobile_no',
            'whatsapp_no',
            'email_address',
            'categories_you_can_provide',         # CSV of IDs
            'categories_you_can_provide_names',   # readable names
            'nationality_of_workers',
            'mobilization_time',
            'uae_deployment_experience',
            'relevant_docs',
            'comments',
            'status',
            'is_deleted',
            'created_at',
            'recruitment_remarks'
        ]

    def create(self, validated_data):
        validated_data['status'] = True
        return super().create(validated_data)

    def get_categories_you_can_provide_names(self, obj):
        """
        Parses the CSV of category IDs in `categories_you_can_provide`,
        fetches active/non-deleted Category names,
        and returns them as a single comma-separated string.
        """
        raw = obj.categories_you_can_provide or ""
        try:
            ids = [int(pk) for pk in raw.split(',') if pk.strip().isdigit()]
        except ValueError:
            return ""
        qs = Category.objects.filter(
            id__in=ids,
            status=True,
            is_deleted=False
        ).order_by('id')
        names = qs.values_list('category', flat=True)
        return ", ".join(names)

#OverseasRecruitment nameslist
class OverseasRecruitmentNameSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)  # <-- Add this line

    class Meta:
        model = OverseasRecruitment
        fields = ['id','contact_person_name']
        
        def create(self, validated_data):
            validated_data['status'] = True  # Force status True
            return super().create(validated_data)
        

#ClientEnquiry
class ClientEnquirySerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)
    categories_required_names = serializers.SerializerMethodField()

    class Meta:
        model = ClientEnquiry
        fields = [
            'id',
            'client_enquiry_id',
            'company_name',
            'email',
            'contact_person_name',
            'mobile_number',
            'nature_of_work',
            'project_location',
            'project_duration',
            'categories_required',          # CSV string
            'categories_required_names',    # readable string
            'quantity_required',
            'project_start_date',
            'kitchen_facility',
            'transportation_provided',
            'accommodation_provided',
            'remarks',
            'query_type',
            'status',
            'is_deleted',
            'created_at',
        ]

    def create(self, validated_data):
        validated_data['status'] = True
        return super().create(validated_data)

    def get_categories_required_names(self, obj):
        """
        Parses the CSV in categories_required, looks up active/non-deleted
        Category rows, and returns a comma-separated string of names.
        """
        raw = obj.categories_required or ""
        try:
            ids = [int(pk) for pk in raw.split(',') if pk.strip().isdigit()]
        except ValueError:
            return ""
        qs = Category.objects.filter(id__in=ids, status=True, is_deleted=False).order_by('id')
        return ", ".join(qs.values_list('category', flat=True))
        

class ClientEnquiryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientEnquiry
        fields = ['id','contact_person_name']


class CategorySerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(default=True)  # <-- Add this line

    class Meta:
        model = Category
        fields = '__all__'
        
        def create(self, validated_data):
            validated_data['status'] = True  # Force status True
            return super().create(validated_data)
