import os
from jinja2 import Template


def user_list(): 
    pass


def user_create():    
    pass


def user_detail():
    cwd = os.getcwd()
    path = os.path.join(cwd, 'templates/user_detail.html')   
    html = open(path).read()
    template = Template(html)
    context = {
        'name': 'Valera', 
        'surname': 'Nagan', 
        'birth_date': '1672-02-11', 
        'gender': 'men', 
        'profession': 'knight', 
        'autobiography': 'fights fights fights'
    }

    return template.render(context)
