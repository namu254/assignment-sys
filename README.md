## Blackboard
A system designed for use in a school setup, by both lecturers and students. It provides a platform where a lecturer can upload student assignment and reading materials. On the other hand, a student is able to access and download materials uploaded by the lecturer, submit assignments as per the specified time, and make enquiries

![Screenshot from 2019-10-01 17-13-01](https://user-images.githubusercontent.com/29103362/65970267-dd30a900-e46e-11e9-8ee2-c7dba9bfed02.png)

![Screenshot from 2019-10-01 17-14-50](https://user-images.githubusercontent.com/29103362/65970367-149f5580-e46f-11e9-9717-bb46320dac23.png)


## Installation
Create a virtual environment
```Bash
virtualenv blackboard_env
```
Clone this repo inside the virtualenv
```Bash
git clone https://github.com/namu254/assignment_sys.git
```
Install the requirements
```Bash
pip install -r requirements.txt
```
then run the system
```Python
py manage.py runserver
```
Open this link on your browser http://127.0.0.1:8000/

[jqueryui](https://jqueryui.com)

[jquery](https://jquery.com)

[crispy-forms](https://django-crispy-forms.readthedocs.io/en/latest/)

[zurb foundation 6](https://foundation.zurb.com/sites/docs/)
