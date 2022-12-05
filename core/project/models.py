from django.db import models

# Create your models here.
class Apps(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    image = models.CharField(max_length=255, null=False, blank=False)
    envs = models.JSONField(null=True, blank=True)
    command = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"App object: id:{self.id} - name:{self.name} - image:{self.image}"