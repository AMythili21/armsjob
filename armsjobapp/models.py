from django.db import models
from django.core.exceptions import ValidationError

def generate_agent_supplier_id():
    # Get the last agent supplier created
    last_supplier = AgentSupplier.objects.exclude(agent_supplier_id__isnull=True).order_by('-created_at').first()
    if last_supplier and last_supplier.agent_supplier_id.startswith("AGT"):
        try:
            # Extract the number after 'AGT' and convert it to an integer
            last_id = int(last_supplier.agent_supplier_id[3:])
            # Increment by 1 and return without zero-padding
            return f"AGT{last_id + 1}"
        except ValueError:
            return "AGT1"  # If there's a ValueError, return 'AGT1'
    return "AGT1"  # Default to 'AGT1' if no record exists


# Create your models here.
class AgentSupplier(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    agent_supplier_id = models.CharField(max_length=10, editable=False, unique=True)   # Set as primary key
    name = models.CharField(max_length=255, null=False, blank=False)
    mobile_no = models.CharField(max_length=20, null=False, blank=False)
    whatsapp_no = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)

    can_recruit = models.CharField(max_length=255, null=True, blank=True)
    associated_earlier = models.CharField(max_length=255, null=True, blank=True)
    can_supply_manpower = models.CharField(max_length=255, null=True, blank=True)
    supply_categories = models.CharField(max_length=255, null=True, blank=True)
    quantity_estimates = models.CharField(max_length=255, null=True, blank=True)
    areas_covered = models.CharField(max_length=255, null=True, blank=True)
    additional_notes = models.CharField(max_length=500, null=True, blank=True)

    remarks = models.TextField(null=True, blank=True) 
    is_deleted = models.BooleanField(default=False)   

    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.agent_supplier_id:  # If no agent_supplier_id is set, generate it
            self.agent_supplier_id = generate_agent_supplier_id()
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'agent_supplier'

#Agent Remarks
class AgentSupplierRemarks(models.Model):
    id = models.AutoField(primary_key=True)
    agent_supplier = models.ForeignKey(AgentSupplier, related_name='agent_remarks', on_delete=models.CASCADE)
    remark = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agent_supplier_remarks'  # Set custom table name
        ordering = ['-updated_at']  # Ordering by 'updated_at' descending

    def __str__(self):
        return f'Remark for {self.agent_supplier.name}'



#candidate
def validate_file_size(value):
    filesize = value.size
    if filesize > 512000:  # 500 KB = 500 * 1024 = 512000 bytes
        raise ValidationError("Max file size 500KB")
    return value

def generate_candidate_id():
    last_candidate = Candidate.objects.exclude(candidate_id__isnull=True).order_by('-created_at').first()
    if last_candidate and last_candidate.candidate_id and last_candidate.candidate_id.startswith("AJ"):
        try:
            last_id = int(last_candidate.candidate_id[2:])
            return f"AJ{last_id + 1}"
        except ValueError:
            return "AJ1"  # Starting point
    return "AJ1"  # Starting point


class Candidate(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    candidate_id = models.CharField(max_length=10, editable=False, unique=True)  # Non-primary field
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15)
    email = models.EmailField(254)
    nationality = models.CharField(max_length=255)
    current_location = models.CharField(max_length=255)

    visa_type = models.CharField(max_length=255)
    visa_expiry_date = models.DateField(null=True, blank=True)
    availability_to_join = models.CharField(max_length=255)

    position_applying_for = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    other_category = models.CharField(max_length=255, null=True, blank=True)
    uae_experience_years = models.CharField(max_length=255)
    skills_tasks = models.TextField()
    preferred_work_location = models.CharField(max_length=255)
    expected_salary = models.CharField(max_length=255)

    upload_cv = models.FileField(upload_to='candidates/cv/', null=True, blank=True,validators=[validate_file_size])
    photo_upload = models.ImageField(upload_to='candidates/photos/', null=True, blank=True, validators=[validate_file_size])
    relevant_docs1 = models.FileField(upload_to='candidates/docs/', null=True, blank=True,validators=[validate_file_size])
    relevant_docs2 = models.FileField(upload_to='candidates/docs/', null=True, blank=True, validators=[validate_file_size])
    relevant_docs3 = models.FileField(upload_to='candidates/docs/', null=True, blank=True, validators=[validate_file_size])
    languages_spoken = models.CharField(max_length=255, null=True, blank=True)
    preferred_work_type = models.CharField(max_length=255, null=True, blank=True)  # e.g., Full-time, Part-time
    currently_employed = models.BooleanField(default=False)
    additional_notes = models.TextField(null=True, blank=True)
    referral_name = models.CharField(max_length=255, null=True, blank=True)
    referral_contact = models.CharField(max_length=255, null=True, blank=True)


    status = models.CharField(max_length=20, default='Active')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.candidate_id:
            self.candidate_id = generate_candidate_id()
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'candidate'

#Candidate Remarks

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

#Manpowersupplier

class ManpowerSupplier(models.Model):
    id= models.AutoField(primary_key=True)
    supplier_id = models.CharField(max_length=10, editable=False, unique=True)  # Non-primary field
    company_name = models.CharField(max_length=255)
    contact_person_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=20)
    whatsapp_no = models.CharField(max_length=20)
    email = models.EmailField()
    office_location = models.CharField(max_length=255)

    categories_available = models.TextField()
    quantity_per_category = models.TextField()

    trade_license = models.FileField(upload_to='documents/trade_licenses/',null=True, blank=True)
    company_license = models.FileField(upload_to='documents/company_licenses/',null=True, blank=True)

    previous_experience = models.BooleanField(default=False)
    worked_with_arms_before = models.BooleanField(default=False)

    comments = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.supplier_id:
            last = ManpowerSupplier.objects.exclude(supplier_id__isnull=True).order_by('-id').first()
            if last and last.supplier_id.startswith("MPS"):
                try:
                    last_id = int(last.supplier_id.replace("MPS", ""))
                    new_id = last_id + 1
                except ValueError:
                    new_id = 1
            else:
                new_id = 1
            self.supplier_id = f"MPS{new_id}"
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'manpower_supplier'
        ordering = ['-created_at']

#Manpowersupplier remarks
class ManpowerSupplierRemarks(models.Model):
    id = models.AutoField(primary_key=True)
    manpower_supplier = models.ForeignKey(ManpowerSupplier, related_name='manpower_remarks', on_delete=models.CASCADE)
    remark = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'manpower_supplier_remarks'
        ordering = ['-updated_at']

    def __str__(self):
        return f'Remark for {self.manpower_supplier.name}'
    
