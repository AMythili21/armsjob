from rest_framework import serializers
from .models import AgentSupplier
from .models import Candidate
from .models import CandidateRemarks


#Agent
class AgentSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSupplier
        fields = '__all__'

#Remarks create and update
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
            'status',
            'is_deleted',
            'created_at',
            'remarks',  # <-- added this
        ]

#Candidate name list
class CandidateNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['full_name']  # Only show name

