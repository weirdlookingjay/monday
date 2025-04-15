from django.db import models
from accounts.models import User, Team

# Create your models here.

class Workspace(models.Model):
    """Workspace model for organizing boards."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='workspaces')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    icon = models.CharField(max_length=50, blank=True)  # For storing icon identifier
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']

class WorkspaceFolder(models.Model):
    """Folder for organizing boards within a workspace."""
    name = models.CharField(max_length=100)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='folders')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
