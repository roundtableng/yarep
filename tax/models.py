from django.db import models


class CompanyRegistration(models.Model):
    tax_id = models.CharField(max_length=15, blank=True)
    incorporation_no = models.CharField(max_length=50, blank=True)
    incorporation_date = models.DateField(blank=True, null=True)
    company_name = models.CharField(max_length=50)
    registered_office = models.CharField(max_length=200, blank=True)
    business_address = models.CharField(max_length=200, blank=True)
