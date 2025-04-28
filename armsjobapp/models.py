from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class AgentSupplier(models.Model):
    agent_supplier_id = models.CharField(max_length=20, primary_key=True)  # Set this field as primary key
    name = models.CharField(max_length=255, null=False, blank=False)
    mobile_no = models.CharField(max_length=20, null=False, blank=False)
    whatsapp_no = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)

    can_recruit = models.CharField(max_length=50, null=True, blank=True)
    associated_earlier = models.CharField(max_length=50, null=True, blank=True)
    can_supply_manpower = models.CharField(max_length=50, null=True, blank=True)
    supply_categories = models.CharField(max_length=255, null=True, blank=True)
    quantity_estimates = models.CharField(max_length=255, null=True, blank=True)
    areas_covered = models.CharField(max_length=255, null=True, blank=True)
    additional_notes = models.CharField(max_length=500, null=True, blank=True)

    remarks = models.TextField(null=True, blank=True) 
    is_deleted = models.BooleanField(default=False)   

    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agent_supplier'

#candidate
def validate_file_size(value):
    filesize = value.size
    if filesize > 512000:  # 500 KB = 500 * 1024 = 512000 bytes
        raise ValidationError("Max file size 500KB")
    return value

class Candidate(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    email = models.EmailField()
    nationality = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)

    visa_type = models.CharField(max_length=255)
    visa_expiry_date = models.DateField(null=True, blank=True)
    availability_to_join = models.CharField(max_length=255)

    position_applying_for = models.CharField(max_length=100)
    category = models.CharField(max_length=255)
    other_category = models.CharField(max_length=255, null=True, blank=True)
    uae_experience_years = models.CharField(max_length=255)
    skills_tasks = models.TextField()
    preferred_work_location = models.CharField(max_length=255)
    expected_salary = models.CharField(max_length=255)

    upload_cv = models.FileField(upload_to='candidates/cv/', validators=[validate_file_size])
    photo_upload = models.ImageField(upload_to='candidates/photos/', null=True, blank=True, validators=[validate_file_size])
    relevant_docs1 = models.FileField(upload_to='candidates/docs/', validators=[validate_file_size])
    relevant_docs2 = models.FileField(upload_to='candidates/docs/', null=True, blank=True, validators=[validate_file_size])
    relevant_docs3 = models.FileField(upload_to='candidates/docs/', null=True, blank=True, validators=[validate_file_size])

    status = models.CharField(max_length=20, default='Active')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'candidate'

#Remarks

class CandidateRemarks(models.Model):
    id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='remarks')
    remark = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'candidate_remarks'
        ordering = ['-updated_at']

    def __str__(self):
        return f'Remark for {self.candidate.full_name}'
