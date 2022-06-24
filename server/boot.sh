source /home/ubuntu/projects/cms-flask/venv/bin/activate

source config.conf

export APP_CONFIG=$config_name

export FLASK_APP=./manage.py

gunicorn -w 4 -b $gunicorn_ip:$gunicorn_port -t 160 manage:app --log-level DEBUG
