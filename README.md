# Starnavi project

#### Prerequisites
- Docker ([Docker installation guide](https://docs.docker.com/install/#supported-platforms));
- Docker Compose ([Docker Compose installation guide](https://docs.docker.com/compose/install/)).
- pre-commit ([pre-commit installation document](https://pre-commit.com/#install)).

#### Install pre-commit hooks
Install `pre-commit` into your git hooks:
```bash
$ pre-commit install
```
You can read more about `pre-commit` usage: https://pre-commit.com/#usage 

#### Configuring Local Environment
Build container
```bash
$ docker build -f ./environment/local/Dockerfile -t starnavi_project .
```

Run application
```bash
$ docker-compose -f environment/local/docker-compose.yml up
```

Run application detached console
```bash
$ docker-compose -f environment/local/docker-compose.yml up -d
```

#### Alembic (migrations)
Generate empty migration file
```bash
$ docker exec -it starnavi_project_app alembic revision -m "create dummy table"
```

Autogenerate
```bash
$ docker exec -it starnavi_project_app alembic revision --autogenerate -m "Added dummy table"
```

Run migrations
```bash
$ docker exec -it starnavi_project_app alembic upgrade head
```

Downgrade migrations (-1 - how many revisions downgrade)
```bash
$ docker exec -it starnavi_project_app alembic downgrade -1
```

#### Pytest
Same container
```bash
$ docker exec -it starnavi_project_app pytest .
```

#### Linters

Flake8
```bash
$ docker-compose -f environment/local/docker-compose.yml run --rm starnavi_project flake8 --statistics --show-source
```

Pylint
```bash
$ docker-compose -f environment/local/docker-compose.yml run --rm starnavi_project pylint app
```