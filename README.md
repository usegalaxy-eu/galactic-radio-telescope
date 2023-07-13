# Galactic Radio Telescope

![GRT Logo, an radio telescope with the galaxy logo emitting from the telescope portion](media/grt-small.png)

This is a project to collect metrics from Galaxy servers across the universe,
and aggregate the data for statistical analysis.

The ultimate goal of this project is to have a simple service which, based on
hundreds of thousands of job runs, can help Galaxy administrators answer common questions.

## GRT Questions

GRT needs to be focused on answering interesting questions to its target audience(s):

Users:

- popular Galaxy instances
- which instances have the tools I need
- which tools are popular (recently)
- popular configuration / parameters

Admins:

- common errors
- runtimes of tools
- relationships between runtime parameters and inputs
- instance statistics?

## Structure

This repo will encompass a web service which aggregates data and eventually
statistical methods to make rational decisions about that data.

There will (eventually) be opt-in code in Galaxy to submit that data to this
service.

## Dev Setup

```console
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## LICENSE

The code is licensed under the AGPLv3.
