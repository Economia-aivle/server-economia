# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Blank(models.Model):
    id = models.IntegerField(primary_key=True)
    characters = models.ForeignKey('Characters', models.DO_NOTHING)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    correct_answer = models.CharField(max_length=10, blank=True, null=True)
    chapter = models.IntegerField()
    explanation = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blank'


class Characters(models.Model):
    id = models.IntegerField(primary_key=True)
    player = models.ForeignKey('Player', models.DO_NOTHING)
    exp = models.IntegerField()
    last_quiz = models.IntegerField()
    kind = models.IntegerField(blank=True, null=True)
    kind_url = models.CharField(max_length=500, blank=True, null=True)
    score1 = models.TextField(blank=True, null=True)
    score2 = models.TextField(blank=True, null=True)
    score3 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'characters'


class ChildComments(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey('Comments', models.DO_NOTHING)
    player = models.ForeignKey('Player', models.DO_NOTHING)
    texts = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'child_comments'


class Comments(models.Model):
    id = models.IntegerField(primary_key=True)
    player = models.ForeignKey('Player', models.DO_NOTHING)
    texts = models.CharField(max_length=500, blank=True, null=True)
    like_cnt = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class Multiple(models.Model):
    id = models.IntegerField(primary_key=True)
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    stage = models.IntegerField()
    question_text = models.CharField(max_length=500, blank=True, null=True)
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=1, blank=True, null=True)
    chapter = models.IntegerField()
    explanation = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'multiple'


class NoticeBoard(models.Model):
    id = models.IntegerField(primary_key=True)
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
    email = models.CharField(unique=True, max_length=255)
    school = models.CharField(max_length=255)
    pwd = models.CharField(max_length=255)
    admin_tf = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'player'


class Rules(models.Model):
    id = models.IntegerField(primary_key=True)
    communit_rule = models.CharField(max_length=500, blank=True, null=True)
    personal_rule = models.CharField(max_length=500, blank=True, null=True)
    youth_protection_rule = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rules'


class Scenario(models.Model):
    id = models.IntegerField(primary_key=True)
    subjects = models.CharField(max_length=5)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    characters_id = models.IntegerField()
    start_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'scenario'


class ScenarioPersonal(models.Model):
    id = models.IntegerField(primary_key=True)
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    scenario = models.ForeignKey(Scenario, models.DO_NOTHING, blank=True, null=True)
    correct_answer = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scenario_personal'


class Stage(models.Model):
    id = models.IntegerField(primary_key=True)
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    subject = models.CharField(max_length=5, blank=True, null=True)
    chapter = models.IntegerField(blank=True, null=True)
    chapter_sub = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stage'


class Tf(models.Model):
    id = models.IntegerField(primary_key=True)
    characters = models.ForeignKey(Characters, models.DO_NOTHING)
    question_text = models.CharField(max_length=500, blank=True, null=True)
    correct_answer = models.CharField(max_length=1, blank=True, null=True)
    chapter = models.IntegerField()
    explanation = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tf'
