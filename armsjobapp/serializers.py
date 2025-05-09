from rest_framework import serializers
from .models import AgentSupplier,AgentSupplierRemarks
from .models import Candidate,CandidateRemarks
from .models import ManpowerSupplier,ManpowerSupplierRemarks
from .models import OverseasRecruitment
from .models import ClientEnquiry
from .models import OverseasRecruitmentRemarks

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
            'quantity_estimates',
            'areas_covered',
            'additional_notes',
            'is_deleted',
            'status',
            'created_at',
            'agent_remarks',  # Include related remarks here
        ]


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
            'categories_available',
            'quantity_per_category',
            'trade_license',
            'company_license',
            'previous_experience',
            'worked_with_arms_before',
            'comments',
            'is_deleted',
            'status',
            'created_at',
            'manpower_remarks'  # Include related remarks
        ]

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
            'categories_you_can_provide',
            'nationality_of_workers',
            'mobilization_time',
            'uae_deployment_experience',
            'relevant_docs',
            'comments',
            'status',
            'is_deleted',
            'created_at',
            'recruitment_remarks'  # related remarks
        ]

#OverseasRecruitment nameslist
class OverseasRecruitmentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverseasRecruitment
        fields = ['id','contact_person_name']
        

#ClientEnquiry
class ClientEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientEnquiry
        fields = '__all__'

class ClientEnquiryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientEnquiry
        fields = ['id','contact_person_name']