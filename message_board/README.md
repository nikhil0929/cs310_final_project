# Message Board

## Message Board Applications

Authentication: This application handles user registration, login, logout, and authentication-related functionality. It can utilize Django's built-in authentication system or a third-party library like Django Allauth.

Topics: This application manages the topics of the message board. It includes functionality for creating, viewing, and subscribing to topics. It can handle CRUD operations related to topics, including creating, updating, and deleting topics.

Posts: This application focuses on managing the messages within the topics. It handles creating, viewing, and posting messages. It includes features like attaching messages to specific topics, allowing users to create, edit, and delete their messages, and implementing the ability to like and comment on messages.

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
