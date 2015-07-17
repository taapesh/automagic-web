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
COPY_BASE_SETTINGS 			= "base_settings.txt"
COPY_PRODUCTION_SETTINGS 	= "production_settings.txt"
COPY_INIT_SETTINGS 			= "init_settings.txt"
COPY_VIEWS 					= "views.txt"
COPY_URLS 					= "urls.txt"
GITIGNORE_SAMPLE 			= "gitignore_sample.txt"

# Names of settings files in django project
DJANGO_SETTINGS_FNAME 		= "settings.py"
BASE_SETTINGS_FNAME 		= "base_settings.py"
LOCAL_SETTINGS_FNAME 		= "local_settings.py"
PRODUCTION_SETTINGS_FNAME 	= "production_settings.py"

# Script names
INIT_SCRIPT 			= "init_setup.sh"
CREATE_PROCFILE_SCRIPT 	= "create_procfile.sh"
REQUIREMENTS_SCRIPT 	= "setup_requirements.sh"
TEMPLATES_SCRIPT 		= "setup_templates.sh"
SETTINGS_SCRIPT			= "modify_settings.sh"

# Settings replace text
REPLACE_SECRET_KEY 		= "<REPLACE_SECRET_KEY>"
REPLACE_PROJECT_NAME 	= "<REPLACE_PROJECT_NAME>"
REPLACE_APP_NAME 		= "<REPLACE_APP_NAME>"

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
	new_settings = open(COPY_BASE_SETTINGS, "r").read()
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
	production_settings_file.write(open(COPY_PRODUCTION_SETTINGS, "r").read())
	production_settings_file.close()

	# Write __init__.py file
	init_file = open(os.path.expanduser(SETTINGS_PATH + "__init__.py"), "w")
	init_file.write(open(COPY_INIT_SETTINGS, "r").read())
	init_file.close()

# Create and write a Procfile for Heroku
def create_procfile():
	f = open(os.path.expanduser(PROJECT_ROOT + "Procfile"), "w+")
	f.write("web: gunicorn " + APP_NAME + ".wsgi")
	f.close()

# Freeze project dependencies into requirements.txt
def setup_requirements():
	command = "source " + REQUIREMENTS_SCRIPT + " " + VENV_ROOT + " " + PROJECT_ROOT
	subprocess.call(command, shell=True)

# Create templates directory and create initial home.html template
def create_templates():
	command = "source " + TEMPLATES_SCRIPT + " " + PROJECT_ROOT
	subprocess.call(command, shell=True)

# Add new views to views.py
def add_views():
	return

# Add new urls to urls.py
def add_urls():
	return

def main():
	print "Setting things up."
	initsetup()
	modify_settings()
	create_procfile()
	setup_requirements()
	create_templates()
	print "Done."
main()
