# Galactic Radio Telescope

This is a project to collect metrics from Galaxy servers across the universe,
and aggregate the data for statistical analysis.

The ultimate goal of this project is to have a simple service which, based on
hundreds of thousands of job runs, can help Galaxy administrators design
optimised rules for distribution jobs to available clusters. This service
should answer questions like:

> If I'm mapping a 32 Gb FastQ dataset against a 1Mbp genome, what are the *likely* minimum/optimal compute requirements

## Structure

This repo will encompass a web service which aggregates data and eventually
statistical methods to make rational decisions about that data.

There will (eventually) be opt-in code in Galaxy to submit that data to this
service.

## Dev Setup

```console
sudo apt-get install libffi-dev
pip install -r requirements.txt
pip install -r requirements/local.txt

sudo npm install -g bower
python manage.py bower install
python manage.py syncdb
python manage.py runserver
```


