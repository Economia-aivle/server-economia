# Generated by Django 4.2.13 on 2024-07-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Player",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("player_id", models.CharField(max_length=20, unique=True)),
                ("player_name", models.CharField(blank=True, max_length=5, null=True)),
                ("nickname", models.CharField(max_length=255, unique=True)),
                ("last_login", models.DateTimeField(auto_now_add=True)),
                ("email", models.CharField(max_length=255, unique=True)),
                ("school", models.CharField(max_length=255)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("password", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "player",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AuthGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150, unique=True)),
            ],
            options={
                "db_table": "auth_group",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AuthGroupPermissions",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "auth_group_permissions",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="AuthPermission",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("codename", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "auth_permission",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Blank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question_text",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "correct_answer",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("chapter", models.IntegerField()),
                (
                    "explanation",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("time", models.DateTimeField()),
            ],
            options={
                "db_table": "blank",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Characters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("exp", models.IntegerField()),
                ("last_quiz", models.IntegerField()),
                ("kind", models.IntegerField(blank=True, null=True)),
                ("kind_url", models.CharField(blank=True, max_length=500, null=True)),
                ("score", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "characters",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ChildComments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("texts", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "imgfile",
                    models.ImageField(blank=True, default="", null=True, upload_to=""),
                ),
            ],
            options={
                "db_table": "child_comments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Comments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("percents", models.IntegerField()),
                ("texts", models.CharField(blank=True, max_length=500, null=True)),
                ("like_cnt", models.IntegerField(blank=True, null=True)),
                ("time", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "comments",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="CommentsLikes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
            options={
                "db_table": "comments_likes",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DjangoAdminLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("action_time", models.DateTimeField()),
                ("object_id", models.TextField(blank=True, null=True)),
                ("object_repr", models.CharField(max_length=200)),
                ("action_flag", models.PositiveSmallIntegerField()),
                ("change_message", models.TextField()),
            ],
            options={
                "db_table": "django_admin_log",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DjangoContentType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("app_label", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "django_content_type",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DjangoMigrations",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("app", models.CharField(max_length=255)),
                ("name", models.CharField(max_length=255)),
                ("applied", models.DateTimeField()),
            ],
            options={
                "db_table": "django_migrations",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="DjangoSession",
            fields=[
                (
                    "session_key",
                    models.CharField(max_length=40, primary_key=True, serialize=False),
                ),
                ("session_data", models.TextField()),
                ("expire_date", models.DateTimeField()),
            ],
            options={
                "db_table": "django_session",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="EconomiaVerificationcode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.CharField(max_length=254, unique=True)),
                ("code", models.CharField(max_length=6)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "economia_verificationcode",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Multiple",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question_text",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("option_a", models.CharField(blank=True, max_length=255, null=True)),
                ("option_b", models.CharField(blank=True, max_length=255, null=True)),
                ("option_c", models.CharField(blank=True, max_length=255, null=True)),
                ("option_d", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "correct_answer",
                    models.CharField(blank=True, max_length=1, null=True),
                ),
                ("chapter", models.IntegerField()),
                (
                    "explanation",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("time", models.DateTimeField()),
            ],
            options={
                "db_table": "multiple",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="NoticeBoard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=20, null=True)),
                ("texts", models.CharField(blank=True, max_length=500, null=True)),
                ("write_time", models.DateTimeField()),
            ],
            options={
                "db_table": "notice_board",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Qna",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "question_text",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "admin_answer",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("time", models.DateTimeField()),
            ],
            options={
                "db_table": "qna",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Rules",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "communit_rule",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "personal_rule",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "youth_protection_rule",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
            ],
            options={
                "db_table": "rules",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Scenario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "question_text",
                    models.CharField(blank=True, max_length=1000, null=True),
                ),
                ("start_time", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "scenario",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Stage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("chapter", models.IntegerField(blank=True, null=True)),
                ("chapter_sub", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "stage",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Subjects",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subjects", models.CharField(blank=True, max_length=20, null=True)),
                ("chapters", models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                "db_table": "subjects",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="SubjectsScore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.IntegerField()),
            ],
            options={
                "db_table": "subjects_score",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Tf",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "question_text",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "correct_answer",
                    models.CharField(blank=True, max_length=1, null=True),
                ),
                ("chapter", models.IntegerField()),
                (
                    "explanation",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("time", models.DateTimeField()),
            ],
            options={
                "db_table": "tf",
                "managed": False,
            },
        ),
    ]
