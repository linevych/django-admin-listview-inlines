from django.db import models


class ParentModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, default='')


class ChildModel(models.Model):
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE, null=True)
    field1 = models.CharField(max_length=255, null=False, blank=False, default='')
    field2 = models.CharField(max_length=255, null=False, blank=False, default='')
    field3 = models.CharField(max_length=255, null=False, blank=False, default='')
