<div align="center">

<img src="https://raw.githubusercontent.com/ivnvxd/ivnvxd/master/img/h_task_manager.png" alt="logo" width="270" height="auto" />
<h1>Task Manager</h1>

<p>
A simple and flexible task management web application
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
  * [Details](#details)
* [Installation](#installation)
  * [Easy Mode](#easy-mode)
  * [Manual Install](#manual-install)
    * [Prerequisites](#prerequisites)
    * [Application](#application)
* [Usage](#usage)
  * [Available Actions](#available-actions-)
* [Demo](#demo)
* [Additionally](#additionally)
  * [Dependencies](#dependencies)
  * [Dev Dependencies](#dev-dependencies)
  * [Makefile Commands](#makefile-commands)
  * [Project Tree](#project-tree)

</details>

## About

A task management web application built with Python and [Django](https://www.djangoproject.com/) framework. It allows you to set tasks, assign performers and change their statuses. Registration and authentication are required to work with the system.

To provide users with a convenient, adaptive, modern interface, the project uses the [Bootstrap](https://getbootstrap.com/) framework.

The frontend is rendered on the backend. This means that the page is built by the DjangoTemplates backend, which returns prepared HTML. And this HTML is rendered by the server.

[PostgreSQL](https://www.postgresql.org/) is used as the object-relational database system.

#### --> [Demo](https://python-task-manager.up.railway.app/) <--

### Features

* [x] Set tasks;
* [x] Assign performers;
* [x] Change task statuses;
* [x] Set multiple tasks labels;
* [x] Filter the tasks displayed;
* [x] User authentication and registration;

### Built With

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Bootstrap 4](https://getbootstrap.com/)
* [PostgreSQL](https://www.postgresql.org/)
* [Poetry](https://python-poetry.org/)
* [Gunicorn](https://gunicorn.org/)
* [Docker](https://www.docker.com/)
* [Whitenoise](http://whitenoise.evans.io/en/latest/)
* [Rollbar](https://rollbar.com/)
* [Flake8](https://flake8.pycqa.org/en/latest/)

### Details

For **_user_** authentication, the standard Django tools are used. In this project, users will be authorized for all actions, that is, everything is available to everyone.

Each task in the task manager usually has a **_status_**. With its help you can understand what is happening to the task, whether it is done or not. Tasks can be, for example, in the following statuses: _new, in progress, in testing, completed_.

**_Tasks_** are the main entity in any task manager. A task consists of a name and a description. Each task can have a person to whom it is assigned. It is assumed that this person performs the task. Also, each task has mandatory fields - author (set automatically when creating the task) and status.

**_Labels_** are a flexible alternative to categories. They allow you to group the tasks by different characteristics, such as bugs, features, and so on. Labels are related to the task of relating many to many.

When the tasks become numerous, it becomes difficult to navigate through them. For this purpose, a **_filtering mechanism_** has been implemented, which has the ability to filter tasks by status, performer, label presence, and has the ability to display tasks whose author is the current user.

---

## Installation

### _Easy Mode:_

Why not just let [Docker Compose](https://docs.docker.com/compose/) do all the work, right? Of course, for the magic to happen, [Docker](https://docs.docker.com/desktop/) must be installed and running. 

Clone the project:
```bash
>> git clone https://github.com/ivnvxd/python-project-52.git && cd python-project-52
```

Create `.env` file in the root folder and add following variables:
```dotenv
DATABASE_URL=postgresql://postgres:password@db:5432/postgres
SECRET_KEY={your secret key} # Django will refuse to start if SECRET_KEY is not set
LANGUAGE=en-us # By default the app will use ru-ru locale
```

And run:
```shell
>> docker-compose up
```

Voila! The server is running at http://0.0.0.0:8000 and you can skip directly to [Available Actions](#available-actions-) section.

### _Manual Install:_

There is always an option for those who like to do everything by themselves.

### Prerequisites

#### Python

Before installing the package make sure you have Python version 3.8 or higher installed:

```bash
>> python --version
Python 3.8+
```

#### Poetry

The project uses the Poetry dependency manager. To install Poetry use its [official instruction](https://python-poetry.org/docs/#installation).

#### PostgreSQL / SQLite

There are two main options for using a database management system for this project: **PostgreSQL** and **SQLite**.

PostgreSQL is used as the main database management system. You have to install it first. It can be downloaded from [official website](https://www.postgresql.org/download/) or installed using Homebrew:
```shell
>> brew install postgresql
```

_Alternatively you can skip this step and use **SQLite** database locally._

### Application

To use the application, you need to clone the repository to your computer. This is done using the `git clone` command. Clone the project:

```bash
>> git clone https://github.com/ivnvxd/python-project-52.git && cd python-project-52
```

After that install all necessary dependencies:

```bash
>> make install
```

Create `.env` file in the root folder and add following variables:
```dotenv
DATABASE_URL=postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
SECRET_KEY={your secret key} # Django will refuse to start if SECRET_KEY is not set
LANGUAGE=en-us # By default the app will use ru-ru locale
```
_If you choose to use **SQLite** DBMS, do not add `DATABASE_URL` variable._

To create the necessary tables in the database, start the migration process:
```bash
>> make migrate
```

---

## Usage

Start the Gunicorn Web-server by running:

```shell
>> make start
```

By default, the server will be available at http://0.0.0.0:8000.

It is also possible to start it local in development mode using:

```shell
>> make dev
```

The dev server will be at http://127.0.0.1:8000.

### Available Actions:

- **_Registration_** — First, you need to register in the application using the registration form provided;
- **_Authentication_** — To view the list of tasks and create new ones, you need to log in using the information from the registration form;
- **_Users_** — You can see the list of all registered users on the corresponding page. It is available without authorization. You can change or delete information only about yourself. If a user is the author or performer of a task, it cannot be deleted;
- **_Statuses_** — You can view, add, update, and delete task statuses if you are logged in. Statuses corresponding to any tasks cannot be deleted;
- **_Tasks_** — You can view, add, and update tasks if you are logged in. Only the task creator can delete tasks. You can also filter tasks on the corresponding page with specified statuses, performers, and labels;
- **_Labels_** — You can view, add, update, and delete task labels if you are logged in. Labels matching any tasks cannot be deleted.

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
* psycopg2 = "^2.9.5"

### Dev Dependencies

* flake8 = "^6.0.0"
* coverage = "^7.0.5"
* ipython = "^8.8.0"

### Makefile Commands

<dl>
    <dt><code>make install</code></dt>
    <dd>Install all dependencies of the package.</dd>
    <dt><code>make migrate</code></dt>
    <dd>Generate and apply database migrations.</dd>
    <dt><code>make dev</code></dt>
    <dd>Run Django development server at http://127.0.0.1:8000/</dd>
    <dt><code>make start</code></dt>
    <dd>Start the Gunicorn web server at http://0.0.0.0:8000 if no port is specified in the environment variables.</dd>
    <dt><code>make lint</code></dt>
    <dd>Check code with flake8 linter.</dd>
    <dt><code>make test</code></dt>
    <dd>Run tests.</dd>
    <dt><code>make check</code></dt>
    <dd>Validate structure of <code>pyproject.toml</code> file, check code with tests and linter.</dd>
    <dt><code>make shell</code></dt>
    <dd>Start Django shell (iPython REPL).</dd>
</dl>

---

<a name="project-tree"></a>
<details><summary style="font-size:larger;"><b>Project Tree</b></summary>

```bash
.              
├── Dockerfile
├── Makefile
├── README.md
├── coverage.xml
├── db.sqlite3
├── docker-compose.yml
├── locale
│   └── ru
│       └── LC_MESSAGES
│           ├── django.mo
│           └── django.po
├── manage.py
├── poetry.lock
├── pyproject.toml
├── requirements.txt
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
