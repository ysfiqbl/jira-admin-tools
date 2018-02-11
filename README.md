# JIRA
This is a simple JIRA API client that came about as a result of repetive task I needed to perform.

# Pre-requisites 
* Docker
* Docker Compose

# Usage

## Setup
* Update the contents in the `config.json` file
    - `url`: the Confluence home page
    - `username`: the username of a user that has admin permissions on JIRA
    - `password`: the password of the user
* `docker-compose build`

## Running the Application
* `docker-compose run jira_admin_tools bash`
* `python jira-client.py config.json`


This code was run on `Python 2.7` and `Ubuntu 16.04`. It was tested on `JIRA 7.2.4`

