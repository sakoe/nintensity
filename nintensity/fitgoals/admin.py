from django.contrib import admin
from fitgoals.models import WorkoutLog

class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'workout_name',
        'workout_units',
        'workout_date',
        'created_date')
    readonly_fields = ['created_date']

admin.site.register(WorkoutLog, WorkoutLogAdmin)
