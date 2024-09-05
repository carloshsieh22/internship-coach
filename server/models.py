from django.db import models

class Business(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)  # Adjust max_length as per your needs
    website = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'businesses'