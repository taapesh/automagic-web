# dependencies
pip install django-toolbelt     # install dependencies
pip freeze                      # view dependencies

# create django project and app
cd $3
django-admin.py startproject $1 # start new django project
cd $1                           # cd into django project directory
python manage.py migrate        # run first migration
python manage.py startapp $2    # start new django app

# clean up
deactivate