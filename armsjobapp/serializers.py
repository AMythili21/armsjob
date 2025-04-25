from rest_framework import serializers
from .models import AgentSupplier
from .models import Candidate

#Agent
class AgentSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSupplier
        fields = '__all__'

#Candidate
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'