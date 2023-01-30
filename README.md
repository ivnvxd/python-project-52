<div align="center">

<img src="https://raw.githubusercontent.com/ivnvxd/ivnvxd/master/img/h_task_manager.png" alt="logo" width="270" height="auto" />
<h1>Task Manager</h1>

<p>
A flexible task management web application
</p>

[![Actions Status](https://github.com/ivnvxd/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/ivnvxd/python-project-52/actions)
![Run Tests](https://github.com/ivnvxd/python-project-52/actions/workflows/run_tests.yml/badge.svg)
![Lint Check](https://github.com/ivnvxd/python-project-52/actions/workflows/lint_check.yml/badge.svg)
[![Maintainability](https://api.codeclimate.com/v1/badges/3bee6db92c7ac49d0729/maintainability)](https://codeclimate.com/github/ivnvxd/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/3bee6db92c7ac49d0729/test_coverage)](https://codeclimate.com/github/ivnvxd/python-project-52/test_coverage)

<p>

<a href="#about">About</a> •
<a href="#installation">Installation</a> •
<a href="#usage">Usage</a> •
<a href="#demo">Demo</a> •
<a href="#additionally">Additionally</a> 

</p>

</div>

<details><summary style="font-size:larger;"><b>Table of Contents</b></summary>

* [About](#about)
  * [Features](#features)
  * [Built With](#built-with)
* [Installation](#installation)
  * [Prerequisites](#prerequisites)
  * [Application](#application)
* [Usage](#usage)
* [Demo](#demo)
* [Additionally](#additionally)
  * [Dependencies](#dependencies)
  * [Dev Dependencies](#dev-dependencies)
  * [Makefile Commands](#makefile-commands)
  * [Project Tree](#project-tree)

</details>

## About

### Features

### Built With

---

## Installation

### Prerequisites

#### Python

#### Poetry

#### PostgreSQL

### Application

---

## Usage

---

## Demo

The demo version is available on Railway platform:
[https://python-task-manager.up.railway.app/](https://python-task-manager.up.railway.app/)

---

## Additionally

### Dependencies

* python = "^3.8.1"
* Django = "^4.1.5"
* python-dotenv = "^0.21.0"
* dj-database-url = "^0.5.0"
* gunicorn = "^20.1.0"
* django-bootstrap4 = "^22.3"
* whitenoise = "^6.3.0"
* django-extensions = "^3.2.1"
* django-filter = "^22.1"
* rollbar = "^0.16.3"
* psycopg2-binary = "^2.9.5"

### Dev Dependencies

* flake8 = "^6.0.0"
* coverage = "^7.0.5"
* ipython = "^8.8.0"

### Makefile Commands

<dl>
    <dt><code>make install</code></dt>
    <dd>Install all dependencies of the package.</dd>
    <dt><code>make lint</code></dt>
    <dd>Check code with flake8 linter.</dd>
    <dt><code>make test</code></dt>
    <dd>Run tests.</dd>
    <dt><code>make check</code></dt>
    <dd>Validate structure of <code>pyproject.toml</code> file, check code with tests and linter.</dd>
</dl>

---

<a name="project-tree"></a>
<details><summary style="font-size:larger;"><b>Project Tree</b></summary>

```bash
.
├── Makefile
├── README.md
├── coverage.xml
├── db.sqlite3
├── locale
│   └── ru
│       └── LC_MESSAGES
│           ├── django.mo
│           └── django.po
├── manage.py
├── poetry.lock
├── pyproject.toml
├── setup.cfg
├── static
└── task_manager
    ├── __init__.py
    ├── asgi.py
    ├── fixtures
    │   ├── label.json
    │   ├── status.json
    │   ├── task.json
    │   ├── test_label.json
    │   ├── test_status.json
    │   ├── test_task.json
    │   ├── test_user.json
    │   └── user.json
    ├── helpers.py
    ├── labels
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── test_forms.py
    │   │   ├── test_models.py
    │   │   ├── test_post.py
    │   │   ├── test_view.py
    │   │   └── testcase.py
    │   ├── urls.py
    │   └── views.py
    ├── mixins.py
    ├── settings.py
    ├── statuses
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── test_forms.py
    │   │   ├── test_models.py
    │   │   ├── test_post.py
    │   │   ├── test_view.py
    │   │   └── testcase.py
    │   ├── urls.py
    │   └── views.py
    ├── tasks
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── filters.py
    │   ├── forms.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   ├── 0002_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── test_forms.py
    │   │   ├── test_models.py
    │   │   ├── test_post.py
    │   │   ├── test_view.py
    │   │   └── testcase.py
    │   ├── urls.py
    │   └── views.py
    ├── templates
    │   ├── 404.html
    │   ├── base.html
    │   ├── footer.html
    │   ├── form.html
    │   ├── index.html
    │   ├── labels
    │   │   ├── delete.html
    │   │   └── labels.html
    │   ├── navbar.html
    │   ├── statuses
    │   │   ├── delete.html
    │   │   └── statuses.html
    │   ├── tasks
    │   │   ├── delete.html
    │   │   ├── task_show.html
    │   │   └── tasks.html
    │   └── users
    │       ├── delete.html
    │       └── users.html
    ├── tests.py
    ├── urls.py
    ├── users
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── models.py
    │   ├── tests
    │   │   ├── __init__.py
    │   │   ├── test_forms.py
    │   │   ├── test_models.py
    │   │   ├── test_post.py
    │   │   ├── test_view.py
    │   │   └── testcase.py
    │   ├── urls.py
    │   └── views.py
    ├── views.py
    └── wsgi.py
```

</details>

---

:octocat: This is the fourth and **final** training project of the ["Python Developer"](https://ru.hexlet.io/programs/python) course on [Hexlet.io](https://hexlet.io)

> GitHub [@ivnvxd](https://github.com/ivnvxd) &nbsp;&middot;&nbsp;
> LinkedIn [@Andrey Ivanov](https://www.linkedin.com/in/abivanov/)
