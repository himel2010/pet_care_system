# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Ownerappointvet(models.Model):
    petid = models.OneToOneField('Pet', models.DO_NOTHING, db_column='petID', primary_key=True)  # Field name made lowercase.
    ownerid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='ownerID')  # Field name made lowercase.
    vid = models.ForeignKey('Vet', models.DO_NOTHING, db_column='vID')  # Field name made lowercase.
    time = models.CharField(max_length=255, blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    prescription = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    accepted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ownerappointvet'
        unique_together = (('petid', 'vid', 'ownerid'),)
