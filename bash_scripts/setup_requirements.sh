cd $1
source bin/activate
cd $2
pip freeze > requirements.txt
cat requirements.txt
deactivate