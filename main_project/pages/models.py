# main_project/pages/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


class Vet(models.Model):
    userid = models.OneToOneField(User, models.DO_NOTHING, db_column='UserID', primary_key=True)
    specialization = models.CharField(db_column='Specialization', max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vet'


class Pet(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    breed = models.CharField(max_length=20, blank=True, null=True)
    allergy = models.CharField(max_length=50, blank=True, null=True)
    last_visit = models.DateField(blank=True, null=True)
    test_result = models.CharField(max_length=255, blank=True, null=True)
    vaccine_name = models.CharField(max_length=30, blank=True, null=True)
    vaccine_date = models.DateField(blank=True, null=True)
    ownerid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='OwnerID', blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pet'


class Petowner(models.Model):
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='UserID', primary_key=True)
    emergency_contact = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'petowner'


class Symptom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    physical = models.CharField(max_length=50, blank=True, null=True)
    behavioural = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Symptom'


class Diseases(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    treatment = models.CharField(max_length=255, blank=True, null=True)
    medicine_name = models.CharField(max_length=50, blank=True, null=True)
    dosage = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Diseases'


class Daycare(models.Model):
    id = models.OneToOneField('User', models.DO_NOTHING, db_column='ID', primary_key=True)
    indoor = models.CharField(max_length=20, blank=True, null=True)
    pet_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daycare'


class appointvOwneret(models.Model):
    petid = models.OneToOneField('Pet', models.DO_NOTHING, db_column='petID', primary_key=True)
    ownerid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='ownerID')
    vid = models.ForeignKey('Vet', models.DO_NOTHING, db_column='vID')
    time = models.CharField(max_length=255, blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    prescription = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)  # Add this field
    accepted = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ownerappointvet'
        unique_together = (('petid', 'vid', 'ownerid'),)

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

class Ownerratesvet(models.Model):
    id = models.AutoField(primary_key=True)
    vid = models.ForeignKey('Vet', models.DO_NOTHING, db_column='vID')
    pid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='pID')
    review = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(default=5)

    class Meta:
        managed = False
        db_table = 'ownerratesvet'
        
class Symptomindicatesdiseases(models.Model):
    sid = models.OneToOneField(Symptom, models.DO_NOTHING, db_column='sID', primary_key=True)
    did = models.ForeignKey(Diseases, models.DO_NOTHING, db_column='dID')
    importance = models.IntegerField(blank=True, null=True)
    probablity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'symptomindicatesdiseases'
        unique_together = (('sid', 'did'),)


# Keep all other models as they are
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)