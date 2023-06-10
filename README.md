# Message Board

This is a message board where users can log in/sign up and post messages to a public message board. Each message must be a part of a specific topic which other users can subscribe to to view the messages posted under the topic. Users that subscribe to a topic can create their own messages to post or view other peoples posted messages.

Users can like and comment on other peoples messages.

## Message Board Applications

Authentication: This application handles user registration, login, logout, and authentication-related functionality.

Topics: This application manages the topics of the message board. It includes functionality for creating, viewing, and subscribing to topics. It can handle CRUD operations related to topics, including creating, updating, and deleting topics.

Posts: This application focuses on managing the messages within the topics. It handles creating, viewing, and posting messages. It includes features like attaching messages to specific topics, allowing users to create, edit, and delete their messages, and implementing the ability to like and comment on messages.

# Software Design and Architecture

I have written the entire backend in django python.

The data is stored in an AWS RDS Postgres instance. The main tables in my database are Topics, Messages and Users.

I have deployed my django appliction to AWS Beanstalk after developing it first on my local machine.

The backend exposes functionality using REST APIs and a text based client to interact with the API endpoints. The sample output from the client in the file `sample_output.txt`.

# Installation

The django application is running in beanstalk at this url:

The client can be downloaded from github using this url:

You can run the client by doing:

```python
python client.py
```

The beanstalk URL is embedded in the client code.

## Django Notes:

```python
django-admin startproject project_name
```

Creates a new Django project with the specified project name.

```python
python manage.py runserver
```

Starts the development server for the Django project, allowing you to view the application in your browser.

```python
python manage.py startapp app_name
```

Creates a new Django application within the project with the specified app name.

```python
python manage.py makemigrations
```

Creates new database migration files based on the changes detected in your models.

```python
python manage.py migrate
```

Applies any pending database migrations to synchronize the database schema with the current set of models.

# EC2

```bash
ssh -i "message_board.pem" ubuntu@ec2-3-129-72-202.us-east-2.compute.amazonaws.com
```
