# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WorkoutType'
        db.create_table(u'fitgoals_workouttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workout_type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('has_distance_component', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'fitgoals', ['WorkoutType'])

        # Adding model 'WorkoutLog'
        db.create_table(u'fitgoals_workoutlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('workout_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('workout_duration_hours', self.gf('django.db.models.fields.IntegerField')()),
            ('workout_duration_minutes', self.gf('django.db.models.fields.IntegerField')()),
            ('workout_distance_miles', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('workout_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('workout_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fitgoals.WorkoutType'])),
        ))
        db.send_create_signal(u'fitgoals', ['WorkoutLog'])

        # Adding model 'Event'
        db.create_table(u'fitgoals_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('event_description', self.gf('django.db.models.fields.TextField')()),
            ('event_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('event_location', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('event_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal(u'fitgoals', ['Event'])

        # Adding model 'Team'
        db.create_table(u'fitgoals_team', (
            (u'group_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.Group'], unique=True, primary_key=True)),
            ('team_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'fitgoals', ['Team'])

        # Adding model 'EventTeam'
        db.create_table(u'fitgoals_eventteam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_for_this_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fitgoals.Event'])),
            ('team_for_this_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fitgoals.Team'])),
        ))
        db.send_create_signal(u'fitgoals', ['EventTeam'])


    def backwards(self, orm):
        # Deleting model 'WorkoutType'
        db.delete_table(u'fitgoals_workouttype')

        # Deleting model 'WorkoutLog'
        db.delete_table(u'fitgoals_workoutlog')

        # Deleting model 'Event'
        db.delete_table(u'fitgoals_event')

        # Deleting model 'Team'
        db.delete_table(u'fitgoals_team')

        # Deleting model 'EventTeam'
        db.delete_table(u'fitgoals_eventteam')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fitgoals.event': {
            'Meta': {'object_name': 'Event'},
            'event_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event_description': ('django.db.models.fields.TextField', [], {}),
            'event_location': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'event_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'event_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'fitgoals.eventteam': {
            'Meta': {'object_name': 'EventTeam'},
            'event_for_this_team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fitgoals.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team_for_this_event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fitgoals.Team']"})
        },
        u'fitgoals.team': {
            'Meta': {'object_name': 'Team', '_ormbases': [u'auth.Group']},
            u'group_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True', 'primary_key': 'True'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'fitgoals.workoutlog': {
            'Meta': {'object_name': 'WorkoutLog'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'workout_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'workout_distance_miles': ('django.db.models.fields.IntegerField', [], {}),
            'workout_duration_hours': ('django.db.models.fields.IntegerField', [], {}),
            'workout_duration_minutes': ('django.db.models.fields.IntegerField', [], {}),
            'workout_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'workout_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fitgoals.WorkoutType']"})
        },
        u'fitgoals.workouttype': {
            'Meta': {'object_name': 'WorkoutType'},
            'has_distance_component': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'workout_type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['fitgoals']