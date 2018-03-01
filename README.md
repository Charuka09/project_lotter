# project_lotter

1. install git bash
2. install python 2.7 from https://www.python.org/downloads/release/python-2714/
3. copy all details in the https://bootstrap.pypa.io/get-pip.py to the notepad and save it as the get-pip.py
4. open git bash from the directory which you created get-pip.py
5. in bash run
  winpty python get-pip.py
6. create the directory project_selector in Documents
7. open git bash in that directory
```shell
   mkdir envs
   cd envs 
   pip install virtualenv
   virtualenv project_lotter
   winpty source project_lotter/Scripts/activate
   cd ..
   git clone https://github.com/rexzing/project_lotter.git
   cd project_lotter
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
```
