all:
	python manage.py migrate
	python manage.py runserver

launch_pg:
	sudo docker run -it -p 5432:5432 -v `pwd`/.pgdata:/var/lib/postgres/data -d postgres:9.5

kill_pg:
	sudo docker ps | grep postgres | awk '{print $$1}' | xargs sudo docker kill

refresh_pg:
	$(MAKE) kill_pg
	rm -rf .pgdata
	$(MAKE) launch_pg
