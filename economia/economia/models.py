# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Player(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    player_id = models.CharField(max_length=20, unique=True)
    player_name = models.CharField(max_length=5, blank=True, null=True)
    nickname = models.CharField(unique=True, max_length=255)
    last_login = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255)
    school = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'player_id'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.player_id

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        managed = False
        db_table = 'player'
        
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


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField('Player', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Blank(models.Model):
    characters = models.ForeignKey('Characters', models.DO_NOTHING)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    correct_answer = models.CharField(max_length=10, blank=True, null=True)
    subjects = models.ForeignKey('Subjects', models.DO_NOTHING)
    chapter = models.IntegerField()
    explanation = models.CharField(max_length=500, blank=True, null=True)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'blank'


class Characters(models.Model):
    player = models.ForeignKey('Player', models.DO_NOTHING)
    exp = models.IntegerField()
    last_quiz = models.IntegerField()
    kind = models.IntegerField(blank=True, null=True)
    kind_url = models.CharField(max_length=500, blank=True, null=True)
    score = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'characters'


class ChildComments(models.Model):
    parent = models.ForeignKey('Comments', models.DO_NOTHING)
    player = models.ForeignKey('Player', models.DO_NOTHING)
    texts = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'child_comments'


class Comments(models.Model):
    scenario = models.ForeignKey('Scenario', models.DO_NOTHING)
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    percents = models.IntegerField()
    texts = models.CharField(max_length=500, blank=True, null=True)
    like_cnt = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comments'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Player', models.DO_NOTHING)

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


class Multiple(models.Model):
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=1, blank=True, null=True)
    subjects = models.ForeignKey('Subjects', models.DO_NOTHING)
    chapter = models.IntegerField()
    explanation = models.CharField(max_length=500, blank=True, null=True)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'multiple'


class NoticeBoard(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    texts = models.CharField(max_length=500, blank=True, null=True)
    write_time = models.DateTimeField()
    admin = models.ForeignKey('Player', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'notice_board'



class Qna(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    admin_answer = models.CharField(max_length=500, blank=True, null=True)
    player = models.ForeignKey(Player, models.DO_NOTHING)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'qna'


class Scenario(models.Model):
    subjects = models.ForeignKey('Subjects', models.DO_NOTHING)
    title = models.CharField(max_length=100, blank=True, null=True)
    question_text = models.CharField(max_length=1000, blank=True, null=True)
    start_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'scenario'


class Stage(models.Model):
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    subjects = models.ForeignKey('Subjects', models.DO_NOTHING)
    chapter = models.IntegerField(blank=True, null=True)
    chapter_sub = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stage'


class Subjects(models.Model):
    subjects = models.CharField(max_length=20, blank=True, null=True)
    chapters = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subjects'


class SubjectsScore(models.Model):
    subjects = models.ForeignKey(Subjects, models.DO_NOTHING)
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    score = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subjects_score'


class Tf(models.Model):
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    correct_answer = models.CharField(max_length=1, blank=True, null=True)
    subjects = models.ForeignKey(Subjects, models.DO_NOTHING)
    chapter = models.IntegerField()
    explanation = models.CharField(max_length=500, blank=True, null=True)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tf'


class TokenBlacklistBlacklistedtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(Player, models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'
