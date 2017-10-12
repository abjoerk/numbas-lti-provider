# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-09 14:08
from __future__ import unicode_literals

from django.db import migrations, models
import re
import django.db.models.deletion

def calculate_num_questions(resource, ScormElement):
    re_objective_id_key = r'^cmi.objectives.([0-9]+).id$'
    top_key = ScormElement.objects.filter(attempt__resource=resource,key__regex=re_objective_id_key).aggregate(models.Max('key'))['key__max']
    if top_key is None:
        return 0
    else:
        n = re.match(re_objective_id_key,top_key).group(1)
        return int(n)+1

def set_num_questions(apps, schema_editor):
    Resource = apps.get_model('numbas_lti','Resource')
    ScormElement = apps.get_model('numbas_lti','ScormElement')

    for r in Resource.objects.all():
        r.num_questions = calculate_num_questions(r, ScormElement)
        r.save()

class Migration(migrations.Migration):

    dependencies = [
        ('numbas_lti', '0033_remove_resource_show_incomplete_marks'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='num_questions',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='scormelement',
            name='attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scormelements', to='numbas_lti.Attempt'),
        ),
        migrations.RunPython(set_num_questions,migrations.RunPython.noop),
    ]