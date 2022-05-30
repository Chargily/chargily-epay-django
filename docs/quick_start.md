# Quick start
Make sure you aleardy have an account in [chargily](https://epay.chargily.com.dz/)

if you don't have an account follow this [toturial](https://dev.chargily.com/docs/#/epay-intro) 

## Installing package 
after u create virtual environment, install django and create project then run the following command 
```
pip install chargily-epay-django
```

### Setup chargily app in django project 
go to `settings.py` and add `chargily-epay-django` to `INSTALLED_APPS`
``` 
# settings.py

INSTALLED_APPS = [
    # ....
    'chargily-epay-django',
]
```

now you are ready to use this package for examples see `user guide`