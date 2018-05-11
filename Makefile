all:
	python manage.py migrate
	python manage.py runserver

launch_pg:
	docker-compose up -d db

kill_pg:
	docker-compose kill db

refresh_pg:
	$(MAKE) kill_pg
	rm -rf .pgdata
	$(MAKE) launch_pg
