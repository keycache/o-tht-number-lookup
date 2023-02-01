db-reset: 
	find . -path "*/migrations/*.py" -not -name "__init__.py" | grep modules | xargs rm -f
	find . -path "*/migrations/*.pyc"  -delete
	rm -rf db.sqlite3

# Not needed
# db-migrate:
# 	python manage.py makemigrations
# 	python manage.py migrate

server-run-local:
	docker build -t o-number-lookup:latest -f ./Dockerfile .
	docker run -p 8006:8006 --name c-o-number-lookup --rm o-number-lookup:latest

run-tests:
	python manage.py test modules.phonenumber.tests.test_all

