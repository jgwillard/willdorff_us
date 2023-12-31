# Generated by Django 4.2.7 on 2023-11-25 02:21

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
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
                ("name", models.CharField(max_length=200)),
                ("description", models.CharField(max_length=200)),
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("location", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Invitation",
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
                    "unique_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("is_sent", models.BooleanField(default=False)),
                ("is_attending", models.BooleanField(default=None, null=True)),
                (
                    "num_guests",
                    models.IntegerField(
                        default=0, verbose_name="number of extra guests"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="events.event"
                    ),
                ),
                (
                    "invitee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.contact"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="invitees",
            field=models.ManyToManyField(
                through="events.Invitation", to="core.contact"
            ),
        ),
    ]
