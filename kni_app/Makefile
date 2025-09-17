DOCKER ?= docker
PROJECT_ROOT := $(shell pwd)
PROJECT_NAME ?= $(notdir $(PROJECT_ROOT))
IMAGE ?= $(PROJECT_NAME):latest
CONTAINER_PREFIX ?= $(PROJECT_NAME)
DEV_SETTINGS ?= KNI.settings.dev
DEV_HOST_PORT ?= 8000
PROD_HOST_PORT ?= 8000
ENV_FILE ?=
DEV_RUN_FLAGS ?=
PROD_RUN_FLAGS ?=
MANAGE_RUN_FLAGS ?= -it

ENV_FILE_ARG := $(if $(ENV_FILE),--env-file $(ENV_FILE),)

.PHONY: build dev start load-data migrate collectstatic dump-data reset-db manage shell

build:
	$(DOCKER) build -t $(IMAGE) .

dev: build
	$(DOCKER) run --rm $(DEV_RUN_FLAGS) \
		--name $(CONTAINER_PREFIX)-dev \
		-p $(DEV_HOST_PORT):8000 \
		-v $(PROJECT_ROOT):/app \
		-e DJANGO_SETTINGS_MODULE=$(DEV_SETTINGS) \
		-e PYTHONUNBUFFERED=1 \
		$(ENV_FILE_ARG) \
		$(IMAGE) python manage.py runserver 0.0.0.0:8000

start: build
	$(DOCKER) run --rm $(PROD_RUN_FLAGS) \
		--name $(CONTAINER_PREFIX)-prod \
		-p $(PROD_HOST_PORT):8000 \
		$(ENV_FILE_ARG) \
		$(IMAGE)

manage: build
	@if [ -z "$(CMD)" ]; then \
		echo "Usage: make manage CMD=\"migrate\""; \
		exit 1; \
	fi
	$(DOCKER) run --rm $(MANAGE_RUN_FLAGS) \
		-v $(PROJECT_ROOT):/app \
		-e DJANGO_SETTINGS_MODULE=$(DEV_SETTINGS) \
		-e PYTHONUNBUFFERED=1 \
		$(ENV_FILE_ARG) \
		$(IMAGE) python manage.py $(CMD)

load-data: build
	$(DOCKER) run --rm -v $(PROJECT_ROOT):/app -e DJANGO_SETTINGS_MODULE=$(DEV_SETTINGS) -e PYTHONUNBUFFERED=1 $(ENV_FILE_ARG) $(IMAGE) python manage.py createcachetable
	$(DOCKER) run --rm -v $(PROJECT_ROOT):/app -e DJANGO_SETTINGS_MODULE=$(DEV_SETTINGS) -e PYTHONUNBUFFERED=1 $(ENV_FILE_ARG) $(IMAGE) python manage.py migrate
	$(DOCKER) run --rm -v $(PROJECT_ROOT):/app -e DJANGO_SETTINGS_MODULE=$(DEV_SETTINGS) -e PYTHONUNBUFFERED=1 $(ENV_FILE_ARG) $(IMAGE) python manage.py load_initial_data
	$(DOCKER) run --rm -v $(PROJECT_ROOT):/app -e DJANGO_SETTINGS_MODULE=$(DEV_SETTINGS) -e PYTHONUNBUFFERED=1 $(ENV_FILE_ARG) $(IMAGE) python manage.py collectstatic --noinput

migrate: build
	$(MAKE) manage CMD="migrate"

collectstatic: build
	$(MAKE) manage CMD="collectstatic --noinput"

dump-data: build
	$(DOCKER) run --rm -v $(PROJECT_ROOT):/app -e DJANGO_SETTINGS_MODULE=$(DEV_SETTINGS) -e PYTHONUNBUFFERED=1 $(ENV_FILE_ARG) $(IMAGE) python manage.py dumpdata --natural-foreign --indent 2 -e auth.permission -e contenttypes -e wagtailcore.GroupCollectionPermission -e wagtailimages.rendition -e images.rendition -e sessions -e wagtailsearch.indexentry -e wagtailsearch.sqliteftsindexentry -e wagtailcore.referenceindex -e wagtailcore.pagesubscription > fixtures/demo.json

reset-db:
	rm -f db.sqlite3
	$(MAKE) load-data

shell: build
	$(DOCKER) run --rm -it \
		--name $(CONTAINER_PREFIX)-shell \
		-v $(PROJECT_ROOT):/app \
		-e DJANGO_SETTINGS_MODULE=$(DEV_SETTINGS) \
		-e PYTHONUNBUFFERED=1 \
		$(ENV_FILE_ARG) \
		$(IMAGE) bash
