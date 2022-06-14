#! /bin/bash

sudo rm /etc/supervisor/conf.d/cms.conf
sudo supervisorctl reload

sudo rm -rf cms-flask/venv/

sudo rm server/cms-dev.sqlite
