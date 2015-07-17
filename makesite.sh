# Automate django web site creation

# ===================================================
# initialize virtualenv
virtualenv $1		# create virtualenv
cd $1				# cd into virtualenv directory
source bin/activate			# activate virtualenv

# dependencies
pip install django-toolbelt		# install dependencies
pip freeze						# view dependencies

# create django project and app
django-admin.py startproject $2	# start new django project
cd $2							# cd into django project directory
python manage.py migrate		# run first migration
python manage.py startapp $3	# start new django app
# ====================================================


# files for heroku
pip freeze > requirements.txt		# freeze requirements to requirements.txt
printf "web: gunicorn " > Procfile	# setup Procfile
printf $3 >> Procfile
printf ".wsgi" >> Procfile
# ========================

# bootstrap stuff
mkdir templates		# create directory for templates
cd templates		# cd into templates
> home.html			# create home template
printf "<h1>HELLO WORLD THIS WAS GENERATED AUTOMATICALLY</h1>" >> home.html

# modify urls.py to include home url
cd ..
cd $2
printf "from django.conf.urls import include, url\n" > urls.py
printf "from django.contrib import admin\n\n" >> urls.py
printf "urlpatterns = [\n" >> urls.py
printf "\turl(r'^admin/', include(admin.site.urls)),\n" >> urls.py
printf "\turl(r'^$', '" >> urls.py
printf $3 >> urls.py
printf ".views.home', name='home'),\n" >> urls.py
printf "]\n" >> urls.py

# modify views.py to include home view
cd ..
cd $3
printf "from django.shortcuts import render\n\n" > views.py
printf "# Create your views here.\n" >> views.py
printf "def home(request):\n" >> views.py
printf "\treturn render(request, 'home.html', {})\n" >> views.py
cd ..

# git stuff
printf $2 > .gitignore			# setup .gitignore
printf "/settings/local.py\n" >> .gitignore
printf ".DS_Store\ndb.sqlite3\n\n# Byte-compiled / optimized / DLL files\n__pycache__/\n*.py[cod]\n*$py.class\n\n# C extensions\n*.so\n\n# Distribution / packaging\n.Python\nenv/\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\n*.egg-info/\n.installed.cfg\n*.egg\n\n# PyInstaller\n#  Usually these files are written by a python script from a template\n#  before PyInstaller builds the exe, so as to inject date/other infos into it.\n*.manifest\n*.spec\n\n# Installer logs\npip-log.txt\npip-delete-this-directory.txt\n\n# Unit test / coverage reports\nhtmlcov/\n.tox/\n.coverage\n.coverage.*\n.cache\nnosetests.xml\ncoverage.xml\n*,cover\n\n# Translations\n*.mo\n*.pot\n\n# Django stuff:\n*.log\n\n# Sphinx documentation\ndocs/_build/\n\n# PyBuilder\ntarget/" >> .gitignore
git init						# initialize git repository
git add .						# add all files
git commit -m "First commit"	# make first commit

python manage.py runserver

# clean up
deactivate						# deactivate virtualenv
cd ~
cd desktop
