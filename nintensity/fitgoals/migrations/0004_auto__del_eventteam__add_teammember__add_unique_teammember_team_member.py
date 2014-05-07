# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'EventTeam'
        db.delete_table(u'fitgoals_eventteam')

        # Adding model 'TeamMember'
        db.create_table(u'fitgoals_teammember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fitgoals.Team'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'fitgoals', ['TeamMember'])

        # Adding unique constraint on 'TeamMember', fields ['team', 'member']
        db.create_unique(u'fitgoals_teammember', ['team_id', 'member_id'])

        # Adding field 'Event.event_creator'
        db.add_column(u'fitgoals_event', 'event_creator',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='admin', to=orm['auth.User']),
                      keep_default=False)


        # Changing field 'Event.event_name'
        db.alter_column(u'fitgoals_event', 'event_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100))
        # Adding unique constraint on 'Event', fields ['event_name']
        db.create_unique(u'fitgoals_event', ['event_name'])


        # Changing field 'Event.event_location'
        db.alter_column(u'fitgoals_event', 'event_location', self.gf('django.db.models.fields.CharField')(max_length=150))
        # Deleting field 'Team.group_ptr'
        db.delete_column(u'fitgoals_team', u'group_ptr_id')

        # Adding field 'Team.id'
        db.add_column(u'fitgoals_team', u'id',
                      self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True),
                      keep_default=False)

        # Adding field 'Team.event'
        db.add_column(u'fitgoals_team', 'event',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['fitgoals.Event']),
                      keep_default=False)

        # Adding field 'Team.team_creator'
        db.add_column(u'fitgoals_team', 'team_creator',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='admin', to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Team.date_created'
        db.add_column(u'fitgoals_team', 'date_created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 5, 7, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Team.team_name'
        db.alter_column(u'fitgoals_team', 'team_name', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Adding unique constraint on 'Team', fields ['event', 'team_name']
        db.create_unique(u'fitgoals_team', ['event_id', 'team_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Team', fields ['event', 'team_name']
        db.delete_unique(u'fitgoals_team', ['event_id', 'team_name'])

        # Removing unique constraint on 'Event', fields ['event_name']
        db.delete_unique(u'fitgoals_event', ['event_name'])

        # Removing unique constraint on 'TeamMember', fields ['team', 'member']
        db.delete_unique(u'fitgoals_teammember', ['team_id', 'member_id'])

        # Adding model 'EventTeam'
        db.create_table(u'fitgoals_eventteam', (
            ('event_for_this_team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fitgoals.Event'])),
            ('team_for_this_event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fitgoals.Team'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'fitgoals', ['EventTeam'])

        # Deleting model 'TeamMember'
        db.delete_table(u'fitgoals_teammember')

        # Deleting field 'Event.event_creator'
        db.delete_column(u'fitgoals_event', 'event_creator_id')


        # Changing field 'Event.event_name'
        db.alter_column(u'fitgoals_event', 'event_name', self.gf('django.db.models.fields.CharField')(max_length=128))

        # Changing field 'Event.event_location'
        db.alter_column(u'fitgoals_event', 'event_location', self.gf('django.db.models.fields.CharField')(max_length=128))
        # Adding field 'Team.group_ptr'
        db.add_column(u'fitgoals_team', u'group_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=None, to=orm['auth.Group'], unique=True, primary_key=True),
                      keep_default=False)

        # Deleting field 'Team.id'
        db.delete_column(u'fitgoals_team', u'id')

        # Deleting field 'Team.event'
        db.delete_column(u'fitgoals_team', 'event_id')

        # Deleting field 'Team.team_creator'
        db.delete_column(u'fitgoals_team', 'team_creator_id')

        # Deleting field 'Team.date_created'
        db.delete_column(u'fitgoals_team', 'date_created')


        # Changing field 'Team.team_name'
        db.alter_column(u'fitgoals_team', 'team_name', self.gf('django.db.models.fields.CharField')(max_length=128))

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
            'event_creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'event_date': ('django.db.models.fields.DateTimeField', [], {}),
            'event_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_location': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'event_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'event_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'fitgoals.team': {
            'Meta': {'unique_together': "(('event', 'team_name'),)", 'object_name': 'Team'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fitgoals.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team_creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fitgoals.teammember': {
            'Meta': {'unique_together': "(('team', 'member'),)", 'object_name': 'TeamMember'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fitgoals.Team']"})
        },
        u'fitgoals.workoutlog': {
            'Meta': {'object_name': 'WorkoutLog'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'workout_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'workout_distance_miles': ('django.db.models.fields.DecimalField', [], {'max_digits': '4', 'decimal_places': '2'}),
            'workout_duration': ('django.db.models.fields.TimeField', [], {'blank': 'True'}),
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