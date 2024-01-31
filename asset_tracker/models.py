from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid 
# Create your models here.

# Allocation status
ALLOCATION_STATUS = {
    ('ALLOCATED', 'Allocated'),
    ('UNALLOCATED', 'Unallocated')
}

class User(AbstractUser):
    employee_code = models.CharField(max_length=10, unique=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.employee_code})"


class AssetType(models.Model):
    type = models.TextField(unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type}"
    

class Asset(models.Model):
    name = models.TextField()
    alloted_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assets_allocated", null=True) #since one user can have many assets allocated
    current_allocation_status = models.CharField(max_length=15, choices=ALLOCATION_STATUS, default="UNALLOCATED")
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    type = models.ForeignKey(AssetType, on_delete=models.CASCADE, related_name="assets")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

 
class AssetImage(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="asset_images/")

    def __str__(self):
        return f"{self.image.name} ({self.asset.name})"



