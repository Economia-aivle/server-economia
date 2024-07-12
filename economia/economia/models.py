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

<<<<<<< HEAD

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)
=======
class Player(AbstractBaseUser):
    player_id = models.CharField(max_length=20, unique=True)
    player_name = models.CharField(max_length=5, blank=True, null=True)
    nickname = models.CharField(unique=True, max_length=255)
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
>>>>>>> 7011c2a3436cdd1982ecee474163ce44e1a2ffd6

    class Meta:
        managed = False
        db_table = 'player'

class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user_id = models.BigIntegerField(unique=True)

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
    scenario = models.ForeignKey('Scenario', models.DO_NOTHING)
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    percents = models.IntegerField()
    texts = models.CharField(max_length=500, blank=True, null=True)
    like_cnt = models.IntegerField(blank=True, null=True)
<<<<<<< HEAD
    time = models.DateTimeField(auto_now_add=True)
=======
    time = models.DateTimeField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
>>>>>>> 7011c2a3436cdd1982ecee474163ce44e1a2ffd6

    class Meta:
        managed = False
        db_table = 'comments'


class CommentsLikes(models.Model):
    comment = models.ForeignKey(Comments, models.DO_NOTHING)
    player = models.ForeignKey('Player', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comments_likes'
        unique_together = (('comment', 'player'),)


<<<<<<< HEAD
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


class EconomiaVerificationcode(models.Model):
    email = models.CharField(unique=True, max_length=254)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'economia_verificationcode'

    def __str__(self):
        return f'{self.email}: {self.code}'

    def is_expired(self):
        # 현재 시간과 생성 시간을 비교하여 3분 이내면 False 반환, 그렇지 않으면 True 반환
        expiration_time = self.created_at + datetime.timedelta(minutes=3)
        now = timezone.now()
        return now > expiration_time


=======
>>>>>>> 7011c2a3436cdd1982ecee474163ce44e1a2ffd6
class Multiple(models.Model):
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
<<<<<<< HEAD
    correct_answer = models.CharField(max_length=1, blank=True, null=True)
=======
    correct_answer = models.CharField(max_length=5, blank=True, null=True)
>>>>>>> 7011c2a3436cdd1982ecee474163ce44e1a2ffd6
    subjects = models.ForeignKey('Subjects', models.DO_NOTHING)
    chapter = models.IntegerField()
    explanation = models.CharField(max_length=500, blank=True, null=True)

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


class Player(models.Model):
    player_id = models.CharField(max_length=20)
    player_name = models.CharField(max_length=5, blank=True, null=True)
    nickname = models.CharField(unique=True, max_length=255)
    last_login = models.DateTimeField()
    email = models.CharField(unique=True, max_length=255)
    school = models.CharField(max_length=255)
    is_superuser = models.IntegerField()
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'player'


class Qna(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    admin_answer = models.CharField(max_length=500, blank=True, null=True)
    player = models.ForeignKey(Player, models.DO_NOTHING)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'qna'


class Rules(models.Model):
    communit_rule = models.CharField(max_length=500, blank=True, null=True)
    personal_rule = models.CharField(max_length=500, blank=True, null=True)
    youth_protection_rule = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rules'


class Scenario(models.Model):
    subjects = models.ForeignKey('Subjects', models.DO_NOTHING)
    title = models.CharField(max_length=100, blank=True, null=True)
    question_text = models.CharField(max_length=1000, blank=True, null=True)
    start_time = models.DateTimeField(auto_now_add=True)

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

    class Meta:
        managed = False
        db_table = 'tf'
