![CI](https://github.com/Dabang-Clone-FinalProject/WPS_DabangAPI/workflows/CI/badge.svg?branch=master)

# WPS_DabangAPI

- python 3.7.4

- pyenv virtualenv

Secrets

```python

ROOT_DIR/secrets.json
{

"base":{

}

}

```



# Deploy

### git ignore

git / linux / macos / django / python / window / pycharm+all / jupyternotebooks

/requirements.txt

/secrets.json

### 가상환경 설정

$ pyenv v/irtualenv 3.7.4 wps-dabangapi

$ pyenv local wps-dabangapi



### poetry

$ peotry init (no / no / yes)

$ poetry add 'django>3.0' djangorestframework notebook

$ poetry add gunicorn

$ poetry add supervisor



### django start project

$ django-admin startproject config

$ mv config app



### Deploy

```
15.164.165.28
```

local : ~/projects/wps12/WPS_DabangAPI/app

EC2 : /home/ubuntu/projects/WPS_DabangAPI/app



### Docker

- .dockerignore
- Dockerfile
- deploy-docker.sh



### HTTPS(Let's Encrypt)

