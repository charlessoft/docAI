build:
	docker build -t gptengine-app .
run: stop
	docker run -d --name gptengine-app-test -p 18883:80 --env UWSGI_CHEAPER=4 --env tUWSGI_PROCESSES=64 gptengine-app
run_it: stop
	docker run -it --name gptengine-app-test -p 18883:80 gptengine-app /bin/sh
exec_it:
	docker exec -it gptengine-app-test /bin/bash
stop:
	-docker rm -f gptengine-app-test
	sh ./scripts/stop.sh
run_1: stop
	uwsgi --plugin python --ini ./uwsgi.ini

run_debug: stop
	python3 gptengine/main.py

run_2: stop
	uwsgi --http-socket :8888 --plugin python  --callable app --module app.main

run_3: stop
	cd app;uwsgi --http-socket :8888 --plugin python  --callable app --module app.main

pytest:
	cd tests && \
		pytest -s -q -v

test:
	curl localhost:18883/api/v1/echo
	curl localhost:18883/admin/
run_job:
	python jobs/scheduler.py
run_celery:
	celery -A  gptengine.main:celery worker --loglevel=info
test_addjob:
	curl -H 'Content-Type: application/json' localhost:8888/api/v1/word2vec_train -d '{"id":"123"}'
test_listjob:
	curl -H 'Content-Type: application/json' localhost:8889/scheduler/jobs

# app 是文件夹
# app.main 文件名
