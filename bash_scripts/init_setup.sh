# initialize virtualenv and create django project and app

# initialize virtualenv
cd ~/Desktop
virtualenv $1           # create virtualenv
cd $1                   # cd into virtualenv directory
source bin/activate     # activate virtualenv

# dependencies
pip install django-toolbelt		# install dependencies
pip freeze						# view dependencies

# create django project and app
django-admin.py startproject $2	# start new django project
cd $2							# cd into django project directory
python manage.py migrate		# run first migration
python manage.py startapp $3	# start new django app

# clean up
deactivate