FitGoals Implementation
***********************

Overview of FitGoals app
========================
- Leverage Django framework

- Create two seperated admin sites
  
  - Default admin sites for admin users and staff users

    - Auth, Group, User, Workout Type admin

  - Customized user admin site for registered FitGoals users

    - It allows non-staff admin users to login.

    - It provides automated registration for new user.

    - It uses basic Django constructs to interface with database:
   
       - Add a new table entry

       - List exiting table entries such as events and workout logs

       - Delete selected entries

    - Models managed by User Admin Site:

       - Workout Log

       - Event 

       - Team


Data models
===========

WorkoutLog Table
~~~~~~~~~~~~~~~~

+-----------------+--------------------+------------------------+------+--------------+--------------+--------------+
|  workout_name   | workout_duration   | workout_distance_miles | user | created_data | workout_date | workout_type |
+=================+====================+========================+======+==============+==============+==============+
| CharField       | TimeField          | DecimalField           | User | DateTimeField| DateTimeField| WorkoutType  |
+-----------------+--------------------+------------------------+------+--------------+--------------+--------------+

WorkoutType Table
~~~~~~~~~~~~~~~~~

+-----------------+--------------------------+
|  workout_type   | has_distance_component   | 
+=================+==========================+
|    CharField    | BooleanField             |
+-----------------+--------------------------+

Views
=====

- Workouts View

  - It uses the change list view of registered WorkoutLogAdmin in user admin site

- Events View

- Profile/Settings View

Backend Database
=================

- PostgreSQL

