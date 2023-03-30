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

## Installation

Before installation, make sure that you have [Python](https://www.python.org/) and [Poetry](https://python-poetry.org/) installed.

1. Clone this repository

    ```bash
    >> git clone https://github.com/ratushnyyvm/python-project-52.git && cd python-project-52
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

---

## Demonstration

The demo version is available on Railway platform: https://python-project-52-production-3063.up.railway.app/

---
