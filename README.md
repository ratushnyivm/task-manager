<div align="center">

# Task Manager

[![Actions Status](https://github.com/ratushnyyvm/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/ratushnyyvm/python-project-52/actions)
[![linter-check](https://github.com/ratushnyyvm/python-project-52/actions/workflows/linter-check.yml/badge.svg)](https://github.com/ratushnyyvm/python-project-52/actions/workflows/linter-check.yml)
[![test-check](https://github.com/ratushnyyvm/python-project-52/actions/workflows/test-check.yml/badge.svg)](https://github.com/ratushnyyvm/python-project-52/actions/workflows/test-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/c030b35154e03f634490/maintainability)](https://codeclimate.com/github/ratushnyyvm/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/c030b35154e03f634490/test_coverage)](https://codeclimate.com/github/ratushnyyvm/python-project-52/test_coverage)

</div>

---

## Description

Task manager is a web application that allows managing tasks. Users can create, edit and track tasks, assign performers, and change their statuses. Registration and authentication are required to work with the system.

Tasks are the main entity of the application and consist of a name and description. A performer can be assigned to each task to complete it. Additionally, each task has mandatory fields: author (set automatically when the task is created) and status.

The status indicates what is happening with the task, whether it is done or not. Tasks can be in the following statuses: "new", "in progress", "in testing", "completed", etc.

Each task can also have a set of labels that allow grouping tasks by different characteristics such as bugs, features, etc.

---

## Dependencies

| Tool              | Version         |
|-------------------|-----------------|
| python            | "^3.10.0"       |
| django            | "4.1.7"         |
| python-dotenv     | "^0.21.1"       |
| gunicorn          | "^20.1.0"       |
| whitenoise        | "^6.3.0"        |
| django-bootstrap4 | "^22.3"         |
| dj-database-url   | "^0.5.0"        |
| psycopg2-binary   | "^2.9.5"        |
| django-filter     | "^22.1"         |
| rollbar           | "^0.16.3"       |

---

## Installation

Before installation, make sure that you have [Python](https://www.python.org/) and [Poetry](https://python-poetry.org/) installed.

1. Clone this repository

    ```bash
    >> git clone https://github.com/ratushnyyvm/task-manager.git && cd task-manager
    ```

2. Install all necessary dependencies:

    ```bash
    >> make install
    ```

3. Create .env file in the root folder and add following variables:

    ```dotenv
    SECRET_KEY={your secret key}
    DATABASE_URL=postgresql://{provider}://{user}:{password}@{host}:{port}/{db}
    ROLLBAR_ACCESS_TOKEN={your secret key}
    ```

    _If you choose to use **SQLite** DBMS, do not add `DATABASE_URL` variable._

4. To create the necessary tables in the database, start the migration process:

    ```bash
    >> make migrate
    ```

5. Start developer server by running:

    ```shell
    >> make start
    ```

    _The dev server will be at http://127.0.0.1:8000._

---

## Usage

For unregistered and non-logged-in users, the following options are available:

- homepage with a brief instruction on how to use the application
![home page](/docs/images/home.png)

- page with a list of all registered users
![user list](/docs/images/user_list.png)

- user registration
![create user](/docs/images/user_create.png)

- login to the system
![login](/docs/images/login.png)

After logging in, the user will have access to three additional tabs: "Statuses", "Labels", and "Tasks".

The "Tasks" tab allows the following actions:

- viewing the list of tasks and filtering, editing, and deleting tasks
![task list](/docs/images/task_list.png)

- creating a new task
![task create](/docs/images/task_create.png)

- viewing a specific task
![task detail](/docs/images/task_detail.png)

To customize tasks, the "Statuses" and "Labels" tabs are available:

- creating, listing, editing, and deleting statuses
![status list](/docs/images/status_list.png)

- creating, listing, editing, and deleting labels
![label list](/docs/images/label_list.png)

Limitations:

- only the user themselves can edit or delete their account
- it is not possible to delete a user, status, or label that is referenced in a task
- only the author of a task can delete it

---

## Demonstration

The demo version is available on Railway platform: https://python-project-52-production-3063.up.railway.app/

---
