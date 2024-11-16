# deploy-service

Сервис развертывания и удаления контейнеров с лабораторными работами. 

Поднимает API-сервис с ручками на заупск и удаление. 
```api
POST /api/v1/lab/add 
DELETE /api/v1/lab/delete
```
При запросе запускает 
отложенную задачу с помощью `dramatiq` и брокера `Redis`. Развертыват и удаляет 
задачи с помощью плэйбуков `Ansible`. При деплое создается контейнер `Docker` с 
именем `uuid`'а лабораторной. При развертывании и удалении обновляет статусы 
лабораторной в БД бэкенда.


## Переменные окружения
- `LOG_LEVEL`:  уровень логирования; default `INFO`
- `DEPLOY_PORT`: порт API-сервера; default `8001`
- `BACKEND_URL`: URL бэкенда: default `http://sqli-lab:8000`
- `WATCHER_URL`: URL сервиса watcher; default `http://watcher:8002`
- `DEPLOY_SECRET`: секрет для общения с deploy-service
- `REDIS_HOST`: адрес хоста Redis; default `redis`
- `REDIS_PORT`: порт хоста Redis; default `6379`
- `ANSIBLE_TIMEOUT`: таймаут работы Ansible плэйбука
- `ANSIBLE_PLAYBOOKS_DIR`: путь до скриптов Ansible; default `/app/ansible` (в контейнере)
- `POSTGRES_HOST`: хост БД postgres
- `POSTGRES_PORT`: порт БД postgres
- `POSTGRES_DB`: имя БД postgres
- `POSTGRES_USER`: имя пользователя БД postgres
- `POSTGRES_PASS`: пароль пользователя БД postgres

## Запуск Deploy-Service 
0. Задать настройки хоста, где будут разворачиваться лобораторные в `ansible/inventory.yml`
1. Задать переменные окружения (`.env.example`), при локлаьном запуске сделать экспорт
2. Запуск в docker: `docker compose -f docker/docker-compose.yml up --build`
3. Запуск локально: 

```shell
    python3 -m venv venv 
    source venv/bin/activate 
    pip install -r requirements.txt
    docker compose -f docker/docker-compose-dev.yml up --build -d
    python3 main.py
```

## Настройка хоста для деплоя Ansible
1. Установить openssh, sshpass: `sudo apt install -y openssh-server sshpass`
2. Настроить /etc/ssh/sshd_config:
```
    PubkeyAuthentication no
    PasswordAuthentication yes
    ChallengeResponseAuthentication yes
```

---
_Python 3.12.3 + dramatiq; Redis; Ansible_