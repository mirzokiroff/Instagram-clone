mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
unmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
stop:
	docker stop postgres_container

start:
	docker start postgres_container

exec:
	docker exec -it -u postgres postgres_container psql
