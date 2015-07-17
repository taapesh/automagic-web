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

# Paths
VENV_ROOT 		= "~/Desktop/" + VENV_NAME
PROJECT_ROOT 	= "~/Desktop/" + VENV_NAME + "/" + PROJECT_NAME + "/"
PROJECT_PATH 	= PROJECT_ROOT + "/" + PROJECT_NAME
APP_PATH 		= PROJECT_ROOT + "/" + APP_NAME

# Script names
INIT_SCRIPT 			= "init_setup.sh"
CREATE_PROCFILE_SCRIPT 	= "create_procfile.sh"
REQUIREMENTS_SCRIPT 	= "setup_requirements.sh"
TEMPLATES_SCRIPT 		= "setup_templates.sh"

def main():
	print "Setting things up."
	initsetup()
	modify_settings()
	create_procfile()
	setup_requirements()
	create_templates()
	print "Done."

# Create virtualenv and django project/app
def initsetup():
    command = "source " + INIT_SCRIPT + " " + VENV_NAME + " " + PROJECT_NAME + " " + APP_NAME
    subprocess.call(command, shell=True)

# Modify django settings to match Heroku requirements
def modify_settings():
	settings_file = open(os.path.expanduser(PROJECT_PATH + "settings.py"), "r")
	lines = settings_file.readlines()
	settings_file.close()
	
	SECRET_KEY = ""
	# Obtain project secret key
	for(line in lines):
		if "SECRET_KEY" in line:
			line = line.rstrip()
			SECRET_KEY = line.split(" = ")[1]

	# Open new settings file and fill it in with project specs
	new_settings = open("copy_settings.txt", "r").read()
	new_settings = new_settings.replace("<REPLACE_SECRET_KEY>", SECRET_KEY)
	new_settings = new_settings.replace("<REPLACE_APP_NAME>", APP_NAME)
	new_settings = new_settings.replace("<REPLACE_PROJECT_NAME>", PROJECT_NAME)

	settings_file = open(os.path.expanduser(PROJECT_PATH + "settings.py"), "w")
	settings_file.write(new_settings)


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

# Modify views to include home view
def write_views():
	return

# Modify URLs to include home url
def write_urls():
	return

def 

main()
