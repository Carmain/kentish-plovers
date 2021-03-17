# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class KentishPlover(models.Model):
    id_kentish_plover = models.AutoField(primary_key=True)
    year = models.IntegerField(blank=True, null=True)
    banding_year = models.IntegerField(blank=True, null=True)
    action = models.CharField(max_length=6, blank=True, null=True)
    metal_ring = models.CharField(max_length=12, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    color = models.CharField(max_length=12, blank=True, null=True)
    sex = models.CharField(max_length=4, blank=True, null=True)
    age = models.CharField(max_length=3, blank=True, null=True)
    date = models.CharField(max_length=10, blank=True, null=True)
    banding_time = models.CharField(max_length=5, blank=True, null=True)
    town = models.CharField(max_length=27, blank=True, null=True)
    department = models.IntegerField(blank=True, null=True)
    locality = models.CharField(max_length=30, blank=True, null=True)
    bander = models.CharField(max_length=7, blank=True, null=True)
    observer = models.CharField(max_length=13, blank=True, null=True)
    first_name_observer = models.CharField(max_length=8, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kentish_plover'


class Observations(models.Model):
    id_observations = models.AutoField(primary_key=True)
    fk_plover = models.IntegerField()
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    date = models.DateField()
    town = models.CharField(max_length=250)
    department = models.CharField(max_length=250)
    locality = models.CharField(max_length=200, blank=True, null=True)
    map_x = models.CharField(max_length=250, blank=True, null=True)
    map_y = models.CharField(max_length=250, blank=True, null=True)
    sex = models.CharField(max_length=20, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'observations'


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'users'
