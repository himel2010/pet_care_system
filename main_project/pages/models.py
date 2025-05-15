# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # This properly hashes the password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # Email is automatically required
    
    def __str__(self):
        return self.email


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


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Daycare(models.Model):
    id = models.OneToOneField('User', models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    indoor = models.CharField(max_length=20, blank=True, null=True)
    pet_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daycare'


class Diseases(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    treatment = models.CharField(max_length=255, blank=True, null=True)
    medicine_name = models.CharField(max_length=50, blank=True, null=True)
    dosage = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diseases'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class appointvOwneret(models.Model):
    petid = models.OneToOneField('Pet', models.DO_NOTHING, db_column='petID', primary_key=True)  # Field name made lowercase.
    ownerid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='ownerID')  # Field name made lowercase.
    vid = models.ForeignKey('Vet', models.DO_NOTHING, db_column='vID')  # Field name made lowercase.
    time = models.CharField(max_length=255, blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    prescription = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ownerappointvet'
        unique_together = (('petid', 'vid', 'ownerid'),)


class Packages(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Add unique=True
    ratings = models.IntegerField(blank=True, null=True)
    fee = models.IntegerField(blank=True, null=True)
    number_of_walks = models.IntegerField(blank=True, null=True)
    grooming = models.CharField(max_length=30, blank=True, null=True)
    emergency_transport = models.CharField(max_length=30, blank=True, null=True)
    # Rename 'id' to 'daycare_id' to avoid the reserved name conflict
    daycare_id = models.ForeignKey(Daycare, models.DO_NOTHING, db_column='ID')  

    class Meta:
        managed = False
        db_table = 'packages'
        unique_together = (('name', 'daycare_id'),)  # Update the reference here too

class Ownerbookpackage(models.Model):
    petid = models.OneToOneField('Pet', models.DO_NOTHING, db_column='petID', primary_key=True)
    pkname = models.ForeignKey('Packages', models.DO_NOTHING, 
                              db_column='pkName',
                              related_name='package_bookings',
                              to_field='name')
    # Update field reference to match the renamed field
    dyid = models.ForeignKey('Daycare', models.DO_NOTHING,
                            db_column='dyID',
                            related_name='daycare_bookings')
    ownerid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='ownerID')
    activity_log = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ownerbookpackage'
        unique_together = (('petid', 'pkname', 'dyid', 'ownerid'),)


class Ownerdaycarechat(models.Model):
    pid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='pID')  # Field name made lowercase.
    did = models.ForeignKey(Daycare, models.DO_NOTHING, db_column='dID')  # Field name made lowercase.
    receiver = models.CharField(max_length=255, blank=True, null=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    message_no = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'ownerdaycarechat'
        unique_together = (('message_no', 'did', 'pid'),)


class Ownerratesvet(models.Model):
    vid = models.OneToOneField('Vet', models.DO_NOTHING, db_column='vID', primary_key=True)  # Field name made lowercase.
    pid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='pID')  # Field name made lowercase.
    review = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ownerratesvet'
        unique_together = (('vid', 'pid'),)


class Ownervetchat(models.Model):
    vid = models.ForeignKey('Vet', models.DO_NOTHING, db_column='vID')  # Field name made lowercase.
    pid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='pID')  # Field name made lowercase.
    receiver = models.CharField(max_length=255, blank=True, null=True)
    sender = models.CharField(max_length=255, blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    message_no = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'ownervetchat'
        unique_together = (('message_no', 'vid', 'pid'),)




class Pet(models.Model):
    type = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    breed = models.CharField(max_length=20, blank=True, null=True)
    allergy = models.CharField(max_length=50, blank=True, null=True)
    last_visit = models.DateField(blank=True, null=True)
    test_result = models.CharField(max_length=255, blank=True, null=True)
    vaccine_name = models.CharField(max_length=30, blank=True, null=True)
    vaccine_date = models.DateField(blank=True, null=True)
    ownerid = models.ForeignKey('Petowner', models.DO_NOTHING, db_column='OwnerID', blank=True, null=True)  # Field name made lowercase.
    age = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Pet'


class Pethassymptom(models.Model):
    petid = models.OneToOneField(Pet, models.DO_NOTHING, db_column='petID', primary_key=True)  # Field name made lowercase.
    sid = models.ForeignKey('Symptom', models.DO_NOTHING, db_column='sID')  # Field name made lowercase.
    days_since_onset = models.IntegerField(blank=True, null=True)
    previously_seen = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pethassymptom'
        unique_together = (('petid', 'sid'),)


class Petowner(models.Model):
    userid = models.OneToOneField('User', models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.
    emergency_contact = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'petowner'


class Symptom(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    physical = models.CharField(max_length=50, blank=True, null=True)
    behavioural = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'symptom'


class Symptomindicatesdiseases(models.Model):
    sid = models.OneToOneField(Symptom, models.DO_NOTHING, db_column='sID', primary_key=True)  # Field name made lowercase.
    did = models.ForeignKey(Diseases, models.DO_NOTHING, db_column='dID')  # Field name made lowercase.
    importance = models.IntegerField(blank=True, null=True)
    probablity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'symptomindicatesdiseases'
        unique_together = (('sid', 'did'),)


class User(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


class Vet(models.Model):
    userid = models.OneToOneField(User, models.DO_NOTHING, db_column='UserID', primary_key=True)  # Field name made lowercase.
    specialization = models.CharField(db_column='Specialization', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'vet'
