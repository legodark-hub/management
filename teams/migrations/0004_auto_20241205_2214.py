# Generated by Django 5.1.3 on 2024-12-05 17:14

import uuid
from django.db import migrations

def gen_uuid(apps, schema_editor):
    Team = apps.get_model("teams", "Team")
    for team in Team.objects.all():
        team.invitation_code = uuid.uuid4()
        team.save(update_fields=["invitation_code"])

class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_team_invitation_code'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]