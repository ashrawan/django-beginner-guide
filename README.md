### "Django-Beginner-Guide" : This Readme is on the development phase, feel free to leave a feedback or help to contribute.
#### The Source code is more directed towards containing code snippet for understanding Django

[ ] __TODO__ : Django Prerequisite

# Getting Started - Django  
## :star: Setting Up virtual environment :star:

1. You need either "virtual env" or "pipenv" (Recommended) to create virtual env
```
pip install virtualenv
# Or
pip install pipenv
```

2. Now, create a virtual environment  
```
virtualenv -p python3 venv
# Or
pipenv install

# Or install dependencies from existing Pipfile
# pipenv install --dev
```

3. Activate virtualenv  
```
venv\Scripts\activate
# Or
pipenv shell
# pipenv --py (to get python path)
```

4. Setting up as new, Install django in our virtual environment
```
pip install django
```

---

## :star: Initializing project :star:

Initialize django app  
```
django-admin startproject projName
```

Run server  
```
python manage.py runserver
```


### Creating apps in project
 ```
 python manage.py startapp dashapp
 ```
 1. Include the app in settings.py
 ``` 
 INSTALLED_APPS = [  
            ... ,
            'dashapp'
]
```
2. To include the routes in main project (urls.py)
```
path('dash/', include('dashapp.urls'))
```

## :star: Working with Models :star:

[ ] __TODO__ : Model fields, Meta   
[ ] __TODO__ : QuerySet, Query Methods, Pagination, QueryManager   
[ ] __TODO__ : Signaling  
[ ] __TODO__ : Auth User Model 

Example: 
```python
from django.db import models

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=200)
    deadline = models.DateTimeField(blank=True)

    # used for string representation of object
    def __str__(self):
        return self.project_name
```
Relating to other Model:
```python  

class Team(models.Model):
    team_code = models.CharField(primary_key=True, max_length=10, unique=True)
    team_name = models.CharField(max_length=100)
    team_description = models.TextField(null=True)
    total_people = models.IntegerField(default=0)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
```

 ### Migration
 ```
 # Generate migration files
python manage.py makemigrations

# Show migrations, [] - Not Applied, [X]- Applied
python manage.py showmigrations

# Migrate - creates tables and columns
python manage.py migrate
 ```

---

### Setup for Basic CRUD on django admin
1. Create Django Admin credentials
 ```
 python manage.py createsuperuser
 ```

2. Navigate and login to admin dashboard 
``` 
http://localhost:8000/admin 
```

3. Register your models to "admin.py"
```python
admin.site.register(Project)
admin.site.register(Team)
```
( Rerun the server, the crud for Model-(Project, Team) will be available now)


## Django Architecture
- MTV Architecture ( Work on templates- Model, Template, View)
- Rest-framework ( Work on Rest APIs - Representational state transfer)

## :star: Integrating our Models, Views and Templates (MTV architecture) :star:

#### Ways of Writing to Template
- [ ] TODO Returning HTML content itself
- [ ] TODO Loading a template, filling a context and returning rendered template
- [ ] OnProgress Using Generic Class based Views 

1. Setting Up Generic Class based Views
```python
from .models import Project
from django.views.generic import ListView, DetailView

# Project List view
class ProjectsAllView(ListView):
    template_name = 'dashapp/projects.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        return Project.objects.all()


# Project detail view
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'dashapp/project-detail.html'

```

2. Connecting dash urls
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('projects/', views.ProjectsAllView.as_view(), name='projects'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
]
```

3. Setting Up Templates
```
TEMPLATES = [
    {
        ... ,
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]
```
4. Creating Html files
 - Create templates folder in our "dashapp"
 - Lets create "__base.html__" to make it reusable
 ```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CProjects App</title>
</head>
<body>
{% block content %}
{% endblock %}
</body>
</html>
 ```

- Our Project listing page "__projects.html__"
```html
{% extends 'base.html' %}
{% block content %}

    <ul>
        {% for project in project_list %}
            <li><a href="{% url 'detail' project.pk %}">{{ project.project_name }}</a></li>
        {% endfor %}
    </ul>

{% endblock %}
```
- Projects details page "__project-detail.html__"
```html
{% extends 'base.html' %}
{% block content %}
    <b> Project Name </b> : {{ project.project_name }}
    </br>
    <b> Submission Deadline </b> : {{ project.deadline }}
{% endblock %}
```
- [ ] TODO Understanding template tags
- [ ] TODO Working with ModelForm
- [ ] TODO XHR request from our template

## :star: Integrating our Models and Views (REST Pattern) :star:

#### Django REST Framework
```
pip install djangorestframework
```
Configure it on "settings.py"
``` 
INSTALLED_APPS = [  
             ... ,
            'rest_framework'
]
```
1. Now we need a way of serializing and deserializing our model instance into "json"

```python
from rest_framework import serializers
from .models import Project
      
class ProjectSerializer(serializers.ModelSerializer):
  class Meta:
    model = Project
    fields = ('project_id', 'project_name', 'deadline')
```
[ ] __TODO__ : Serializer Options

#### Ways of Creating REST endpoints
- [X] __SOURCE__ : Custom separate view method for each CRUD
- [X] __SOURCE__ : TODO Custom View method that checks the request type and performs required respective logic

- [X] __SOURCE__ : TODO Using View classes provided by rest framework: APIView and classes composed by mixin 

#### Authenticating REST endpoints
- [ ] __TODO__ : Authenticating endpoints
- [ ] __TODO__: Custom user login and registration

2. Setting up "Views.py" (View classe example)
```python
from rest_framework import viewsets
from .models import Project
        
class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()    
```

3. Required setup in 'url.py"
```python
from django.urls import path, include
from rest_framework import routers
from dashapp import views
        
router = routers.DefaultRouter()
router.register(r'projects', views.ProjectView)
        
urlpatterns = [         
    path('api/', include(router.urls))
]
```

4. Check APIs
```
http://127.0.0.1:8000/dash/api/
```

