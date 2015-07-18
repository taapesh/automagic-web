"""
It's magic...
"""
# Imports
import os
import subprocess

# Testing
DEMO            = True
VENV_NAME       = "testvenv"
PROJECT_NAME    = "proj2"
APP_NAME        = "app2"

# Project paths
VENV_ROOT           = "~/" + VENV_NAME + "/"
PROJECT_ROOT        = "~/" + VENV_NAME + "/" + PROJECT_NAME + "/"
PROJECT_PATH        = PROJECT_ROOT + PROJECT_NAME + "/"
APP_PATH            = PROJECT_ROOT + APP_NAME + "/"
SETTINGS_PATH       = PROJECT_PATH + "settings/"
STATIC_PATH         = APP_PATH + "static"
TEMPLATES_PATH      = PROJECT_ROOT + "templates"

# File names to copy
COPY_FOLDER                 = "copy_files/"
COPY_BASE_SETTINGS          = COPY_FOLDER + "base_settings.txt"
COPY_PRODUCTION_SETTINGS    = COPY_FOLDER + "production_settings.txt"
COPY_INIT_SETTINGS          = COPY_FOLDER + "init_settings.txt"
COPY_WSGI                   = COPY_FOLDER + "wsgi.txt"
COPY_VIEWS                  = COPY_FOLDER + "views.txt"
COPY_URLS                   = COPY_FOLDER + "urls.txt"
GITIGNORE_SAMPLE            = COPY_FOLDER + "gitignore_sample.txt"
ORIGINAL_GITIGNORE          = "gitignore.txt"
COPY_STATIC_FOLDER          = "template_builders/demo/static"
COPY_TEMPLATES_FOLDER       = "template_builders/demo/templates"

# Names of settings files in django project
DJANGO_SETTINGS_FNAME       = "settings.py"
BASE_SETTINGS_FNAME         = "base_settings.py"
LOCAL_SETTINGS_FNAME        = "local_settings.py"
PRODUCTION_SETTINGS_FNAME   = "production_settings.py"

# Script names
SCRIPT_FOLDER           = "bash_scripts/"
BASH_COMMAND            = "bash ./"
INIT_SCRIPT             = SCRIPT_FOLDER + "init_setup.sh"
CREATE_PROCFILE_SCRIPT  = SCRIPT_FOLDER + "create_procfile.sh"
REQUIREMENTS_SCRIPT     = SCRIPT_FOLDER + "setup_requirements.sh"
TEMPLATES_SCRIPT        = SCRIPT_FOLDER + "setup_templates.sh"
SETTINGS_SCRIPT         = SCRIPT_FOLDER + "modify_settings.sh"
GITIGNORE_SCRIPT        = SCRIPT_FOLDER + "finalize_gitignore.sh"
GIT_SETUP_SCRIPT        = SCRIPT_FOLDER + "git_setup.sh"
HEROKU_CREATE_SCRIPT    = SCRIPT_FOLDER + "heroku_create.sh"
STATIC_SCRIPT           = SCRIPT_FOLDER + "staticfiles_setup.sh"
COPY_STATIC_SCRIPT      = SCRIPT_FOLDER + "copy_static.sh"
INIT_VENV_SCRIPT        = SCRIPT_FOLDER + "init_venv.sh"
START_DJANGO_SCRIPT     = SCRIPT_FOLDER + "start_django.sh"
CLEANUP_SCRIPT          = SCRIPT_FOLDER + "cleanup.sh"

# Settings replace text
REPLACE_SECRET_KEY      = "<REPLACE_SECRET_KEY>"
REPLACE_PROJECT_NAME    = "<REPLACE_PROJECT_NAME>"
REPLACE_APP_NAME        = "<REPLACE_APP_NAME>"

# CDNs for popular js and css, use these when possible, local versions as a backup
JQUERY_CDN          = "https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"
BOOTSTRAP_CSS_CDN   = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"
BOOTSTRAP_JS_CDN    = "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"
FONT_AWESOME_CDN    = "https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css"


def init_venv():
    """ Create virtualenv and activate it """
    command = BASH_COMMAND + INIT_VENV_SCRIPT + " " + VENV_NAME
    subprocess.call(command, shell=True)

def start_django():
    """ Start django project + app """
    command = BASH_COMMAND + START_DJANGO_SCRIPT + " " + PROJECT_NAME + " "  + APP_NAME + " " + VENV_NAME
    subprocess.call(command, shell=True)

def modify_settings():
    """ Modify django settings to match Heroku requirements """
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
    command = BASH_COMMAND + SETTINGS_SCRIPT + " " + PROJECT_PATH + " " + BASE_SETTINGS_FNAME + " " + LOCAL_SETTINGS_FNAME + " " + PRODUCTION_SETTINGS_FNAME
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

def create_procfile():
    """ Create and write a Procfile for Heroku """
    procfile = open(os.path.expanduser(PROJECT_ROOT + "Procfile"), "w+")
    procfile.write("web: gunicorn " + PROJECT_NAME + ".wsgi")
    procfile.close()

def modify_wsgi():
    """ Modify wsgi to include dj_static for serving static files in production """
    wsgi_file = open(os.path.expanduser(PROJECT_PATH + "wsgi.py"), "w")
    copy_file = open(COPY_WSGI, "r")
    wsgi_file.write(copy_file.read().replace(REPLACE_PROJECT_NAME, PROJECT_NAME))
    copy_file.close()
    wsgi_file.close()

def create_gitignore():
    """ Create a gitignore file """
    gitignore = open(os.path.expanduser(PROJECT_ROOT + ORIGINAL_GITIGNORE), "w+")
    copy_file = open(GITIGNORE_SAMPLE, "r")
    gitignore.write(copy_file.read().replace(REPLACE_PROJECT_NAME, PROJECT_NAME))
    command = BASH_COMMAND + GITIGNORE_SCRIPT + " " + PROJECT_ROOT + " " + ORIGINAL_GITIGNORE
    subprocess.call(command, shell=True)
    copy_file.close()
    gitignore.close()

def setup_requirements():
    """ Freeze project dependencies into requirements.txt """
    command = BASH_COMMAND + REQUIREMENTS_SCRIPT + " " + VENV_ROOT + " " + PROJECT_ROOT
    subprocess.call(command, shell=True)

def create_templates():
    """ Create templates directory and create initial home.html template """
    command = BASH_COMMAND + TEMPLATES_SCRIPT + " " + PROJECT_ROOT
    subprocess.call(command, shell=True)

def setup_static():
    """ Setup static directory and subdirectories """
    command = BASH_COMMAND + STATIC_SCRIPT + " " + APP_PATH
    subprocess.call(command, shell=True)

    if DEMO:
        command = BASH_COMMAND + COPY_STATIC_SCRIPT + " " + COPY_STATIC_FOLDER + " " + STATIC_PATH + " " + COPY_TEMPLATES_FOLDER + " " + TEMPLATES_PATH
        subprocess.call(command, shell=True)

def add_views():
    """ Add new views to views.py """
    views_file = open(os.path.expanduser(APP_PATH + "views.py"), "w")
    copy_file = open(COPY_VIEWS, "r")
    views_file.write(copy_file.read())
    copy_file.close()
    views_file.close()

def add_urls():
    """ Add new urls to urls.py """
    urls_file = open(os.path.expanduser(PROJECT_PATH + "urls.py"), "w")
    copy_file = open(COPY_URLS, "r")
    urls_file.write(copy_file.read().replace(REPLACE_APP_NAME, APP_NAME))
    copy_file.close()
    urls_file.close()

def setup_git():
    """ Initialize git repository, add files, and make first commit """
    command = BASH_COMMAND + GIT_SETUP_SCRIPT + " " + PROJECT_ROOT
    subprocess.call(command, shell=True)

def heroku_create():
    """ Create a heroku app and deploy using git """
    command = BASH_COMMAND + HEROKU_CREATE_SCRIPT + " " + PROJECT_ROOT
    subprocess.call(command, shell=True)

def main():
    print "Setting things up."
    init_venv()
    start_django()
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
