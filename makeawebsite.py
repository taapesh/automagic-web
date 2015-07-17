'''
Created on Jul 16, 2015

@author: taapesh
'''
import os
import subprocess

# Testing
VENV_NAME		= "testvenv"
PROJECT_NAME	= "proj"
APP_NAME 		= "app"

# Project paths
VENV_ROOT 		= "~/Desktop/" + VENV_NAME + "/"
PROJECT_ROOT 	= "~/Desktop/" + VENV_NAME + "/" + PROJECT_NAME + "/"
PROJECT_PATH 	= PROJECT_ROOT + PROJECT_NAME + "/"
APP_PATH 		= PROJECT_ROOT + APP_NAME + "/"
SETTINGS_PATH	= PROJECT_PATH + "settings/"

# File names to copy
COPY_FOLDER					= "copy_files/"
COPY_BASE_SETTINGS			= COPY_FOLDER + "base_settings.txt"
COPY_PRODUCTION_SETTINGS	= COPY_FOLDER + "production_settings.txt"
COPY_INIT_SETTINGS			= COPY_FOLDER + "init_settings.txt"
COPY_WSGI					= COPY_FOLDER + "wsgi.txt"
COPY_VIEWS					= COPY_FOLDER + "views.txt"
COPY_URLS					= COPY_FOLDER + "urls.txt"
GITIGNORE_SAMPLE			= COPY_FOLDER + "gitignore_sample.txt"
ORIGINAL_GITIGNORE			= "gitignore.txt"

# Names of settings files in django project
DJANGO_SETTINGS_FNAME 		= "settings.py"
BASE_SETTINGS_FNAME 		= "base_settings.py"
LOCAL_SETTINGS_FNAME 		= "local_settings.py"
PRODUCTION_SETTINGS_FNAME 	= "production_settings.py"

# Script names
SCRIPT_FOLDER			= "bash_scripts/"
INIT_SCRIPT 			= SCRIPT_FOLDER + "init_setup.sh"
CREATE_PROCFILE_SCRIPT 	= SCRIPT_FOLDER + "create_procfile.sh"
REQUIREMENTS_SCRIPT 	= SCRIPT_FOLDER + "setup_requirements.sh"
TEMPLATES_SCRIPT 		= SCRIPT_FOLDER + "setup_templates.sh"
SETTINGS_SCRIPT			= SCRIPT_FOLDER + "modify_settings.sh"
GITIGNORE_SCRIPT		= SCRIPT_FOLDER + "finalize_gitignore.sh"
GIT_SETUP_SCRIPT		= SCRIPT_FOLDER + "git_setup.sh"
HEROKU_CREATE_SCRIPT	= SCRIPT_FOLDER + "heroku_create.sh"
STATIC_SCRIPT			= SCRIPT_FOLDER + "staticfiles_setup.sh"

# Settings replace text
REPLACE_SECRET_KEY 		= "<REPLACE_SECRET_KEY>"
REPLACE_PROJECT_NAME 	= "<REPLACE_PROJECT_NAME>"
REPLACE_APP_NAME 		= "<REPLACE_APP_NAME>"

# CDNs for popular js and css
JQUERY_CDN			= "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"
BOOTSTRAP_CSS_CDN	= "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"
BOOTSTRAP_JS_CDN	= "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"
FONT_AWESOME_CDN	= "https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css"


# Create virtualenv and django project/app
def initsetup():
    command = "source " + INIT_SCRIPT + " " + VENV_NAME + " " + PROJECT_NAME + " " + APP_NAME
    subprocess.call(command, shell=True)

# Modify django settings to match Heroku requirements
def modify_settings():
	settings_file = open(os.path.expanduser(PROJECT_PATH + DJANGO_SETTINGS_FNAME), "r")
	lines = settings_file.readlines()
	settings_file.close()
	
	SECRET_KEY = ""
	# Obtain project secret key
	for line in lines:
		if "SECRET_KEY" in line:
			line = line.rstrip()
			SECRET_KEY = line.split(" = ")[1]
			break

	# Open new settings file and fill it in with project specs
	copy_file = open(COPY_BASE_SETTINGS, "r")
	new_settings = copy_file.read()
	copy_file.close()
	new_settings = new_settings.replace(REPLACE_SECRET_KEY, SECRET_KEY)
	new_settings = new_settings.replace(REPLACE_APP_NAME, APP_NAME)
	new_settings = new_settings.replace(REPLACE_PROJECT_NAME, PROJECT_NAME)

	# Write new settings to settings file
	settings_file = open(os.path.expanduser(PROJECT_PATH + DJANGO_SETTINGS_FNAME), "w")
	settings_file.write(new_settings)
	settings_file.close()

	# Build command to setup new settings directory
	command = "source " + SETTINGS_SCRIPT + " " + PROJECT_PATH + " " + BASE_SETTINGS_FNAME + " " + LOCAL_SETTINGS_FNAME + " " + PRODUCTION_SETTINGS_FNAME
	subprocess.call(command, shell=True)

	# Write base settings file
	base_settings_file = open(os.path.expanduser(SETTINGS_PATH + BASE_SETTINGS_FNAME), "w")
	base_settings_file.write(new_settings)
	base_settings_file.close()

	# Write local settings file
	local_settings_file = open(os.path.expanduser(SETTINGS_PATH + LOCAL_SETTINGS_FNAME), "w")
	local_settings_file.write(new_settings)
	local_settings_file.close()
	
	# Write production settings file
	production_settings_file = open(os.path.expanduser(SETTINGS_PATH + PRODUCTION_SETTINGS_FNAME), "w")
	copy_file = open(COPY_PRODUCTION_SETTINGS, "r")
	new_settings = copy_file.read().replace(REPLACE_SECRET_KEY, SECRET_KEY)
	new_settings = new_settings.replace(REPLACE_PROJECT_NAME, PROJECT_NAME)
	new_settings = new_settings.replace(REPLACE_APP_NAME, APP_NAME)
	production_settings_file.write(new_settings)
	copy_file.close()
	production_settings_file.close()

	# Write __init__.py file
	init_file = open(os.path.expanduser(SETTINGS_PATH + "__init__.py"), "w")
	copy_file = open(COPY_INIT_SETTINGS, "r")
	init_file.write(copy_file.read())
	copy_file.close()
	init_file.close()

# Create and write a Procfile for Heroku
def create_procfile():
	procfile = open(os.path.expanduser(PROJECT_ROOT + "Procfile"), "w+")
	procfile.write("web: gunicorn " + PROJECT_NAME + ".wsgi")
	procfile.close()

# Modify wsgi to include dj_static for serving static files in production
def modify_wsgi():
	wsgi_file = open(os.path.expanduser(PROJECT_PATH + "wsgi.py"), "w")
	copy_file = open(COPY_WSGI, "r")
	wsgi_file.write(copy_file.read().replace(REPLACE_PROJECT_NAME, PROJECT_NAME))
	copy_file.close()
	wsgi_file.close()

# Create a gitignore file
def create_gitignore():
	gitignore = open(os.path.expanduser(PROJECT_ROOT + ORIGINAL_GITIGNORE), "w+")
	copy_file = open(GITIGNORE_SAMPLE, "r")
	gitignore.write(copy_file.read().replace(REPLACE_PROJECT_NAME, PROJECT_NAME))
	command = "source " + GITIGNORE_SCRIPT + " " + PROJECT_ROOT + " " + ORIGINAL_GITIGNORE
	subprocess.call(command, shell=True)
	copy_file.close()
	gitignore.close()

# Freeze project dependencies into requirements.txt
def setup_requirements():
	command = "source " + REQUIREMENTS_SCRIPT + " " + VENV_ROOT + " " + PROJECT_ROOT
	subprocess.call(command, shell=True)

# Create templates directory and create initial home.html template
def create_templates():
	command = "source " + TEMPLATES_SCRIPT + " " + PROJECT_ROOT
	subprocess.call(command, shell=True)

# Setup static directory and subdirectories
def setup_static():
	command = "source " + STATIC_SCRIPT + " " + APP_PATH
	subprocess.call(command, shell=True)

# Add new views to views.py
def add_views():
	views_file = open(os.path.expanduser(APP_PATH + "views.py"), "w")
	copy_file = open(COPY_VIEWS, "r")
	views_file.write(copy_file.read())
	copy_file.close()
	views_file.close()
	
# Add new urls to urls.py
def add_urls():
	urls_file = open(os.path.expanduser(PROJECT_PATH + "urls.py"), "w")
	copy_file = open(COPY_URLS, "r")
	urls_file.write(copy_file.read().replace(REPLACE_APP_NAME, APP_NAME))
	copy_file.close()
	urls_file.close()

# Initialize git repository, add files, and make first commit
def setup_git():
	command = "source " + GIT_SETUP_SCRIPT + " " + PROJECT_ROOT
	subprocess.call(command, shell=True)

# Create a heroku app and deploy using git
def heroku_create():
	command = "source " + HEROKU_CREATE_SCRIPT + " " + PROJECT_ROOT
	subprocess.call(command, shell=True)

def main():
	print "Setting things up."
	initsetup()
	modify_settings()
	create_procfile()
	modify_wsgi()
	setup_requirements()
	create_templates()
	setup_static()
	add_views()
	add_urls()
	create_gitignore()
	setup_git()
	heroku_create()
	print "Done."

if __name__ == "__main__":
    main()
