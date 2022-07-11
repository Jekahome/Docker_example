
## Dockerfile

```
FROM python:3.7.2-alpine3.8

LABEL maintainer="yaroshjeka@gmail.com"

# Устанавливаем зависимости
RUN apk add --update git

# Задаём текущую рабочую директорию
WORKDIR script

# Копируем код из локального контекста в рабочую директорию образа /script
COPY my_script.py .

# Задаём значение по умолчанию для переменной
ARG buildtime_variable=default_value

# переопределить default_value для «buildtime_variable» при сборке
ENV ENV_VAR_NAME=$buildtime_variable 

# Настраиваем команду, которая должна быть запущена в контейнере во время его выполнения
ENTRYPOINT python /script/my_script.py --my_var ${ENV_VAR_NAME}
# CMD python ./my_script.py --my_var ${ENV_VAR_NAME}  # можно переопределить при run

# Открываем порты
EXPOSE 8000

# Создаём том для хранения данных
VOLUME /container_data

``` 



## 1. Явно создать том и подключить его
```
$ docker volume create \
    --name host_data_with_name \
    --opt type=bind \
    --opt device=/home/jeka/Projects/Docker_example/ex1/host_data \
    --opt o=bind
```

### Список примонтированных томов
```
$ docker volume ls
```

### Удалить примонтированный том
```
$ docker volume rm my_volume
```

### Удалить не связанные тома
```
$ docker volume ls -f dangling=true
```

### Инспектировать том
```
$ docker inspect host_data_with_name

 [
     {
         "CreatedAt": "2022-07-11T18:36:33+02:00",
         "Driver": "local",
         "Labels": {},
         "Mountpoint": "/var/lib/docker/volumes/host_data_with_name/_data",
         "Name": "host_data_with_name",
         "Options": {
            "device": "/home/jeka/Projects/Docker_example/ex1/host_data",
            "o": "bind",
            "type": "bind"
        },
        "Scope": "local"
    }
]
```

## 2. Создать Image docker_ex/v1 и передать ARG для инициализации ENV
```
$ cd <folder Dockerfile>
$ docker build -t docker_ex/v1 \
    --build-arg buildtime_variable=hello \
    --file Dockerfile .
```

## 3. Запуск контейнера на основе Image docker_ex/v1 с примонтированной папкой
 
### Монтирование папки хоста host_data на папку контейнера container_data:
``` --mount source=host_data_with_name,destination=/container_data  ```
 
### Для выполнения скрипта из CMD Dockerfile
```
$ docker run -p 8000:8000 \
    --name name_container_docker_ex_v1 \
    --mount source=host_data_with_name,destination=/container_data \
    -it docker_ex/v1 
 
OUTPUT: ENV_VAR_NAME= hello
OUTPUT: my_var= hello
```
  
### Для выполнения своего скрипта.

Переопределение CMD скрипта на свой ```-c "python my_script.py --my_var hi && ls -l /container_data"```
```
$ docker run -p 8000:8000 \
    --name name_container_docker_ex_v1 \
    --mount source=host_data_with_name,destination=/container_data \
    -it docker_ex/v1 /bin/sh -c "python my_script.py \
    --my_var hi && ls -l /container_data"

OUTPUT: ENV_VAR_NAME= hello
OUTPUT: my_var= hi
drwxrwxr-x    2 1000     1000          4096 Jul 11 16:44 container_data
drwxr-xr-x    1 root     root          4096 Jul 11 16:42 script
...
```

## Доступ через порт

Если контейнер не завершает работу сразу,а запускает демона

1. Сможем выполнять произвольный скрипт используя `docker exec -it <CONTAINER NAME> <BASH COMMAND>` или выполнить через терминал `docker exec -it <CONTAINER NAME> /bin/sh`

2. Сможем получить к содержимому контейнера через порт, если пробросить порт ```<HOST PORT>:<CONTAINER PORT>``` сможем открыть браузер `http://127.0.0.1:8080/` или `curl 127.0.0.1:8080`

```
$ docker run --rm -p 8080:8000 \
    --mount source=host_data_with_name,destination=/container_data \
    --name name_container_docker_ex_v1 \
    -it docker_ex/v1 /bin/sh 
    
$ docker exec -it name_container_docker_ex_v1 python my_script.py --my_var hi

$ docker exec -it name_container_docker_ex_v1 /bin/sh (далее вввод команды в консоле)

$ docker container stop name_container_docker_ex_v1
```

