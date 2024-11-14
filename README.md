# deploy-service

Сервис развертывания контейнеров с лабораторными работами.

## Запуск
1. `docker-compose -f docker/docker-compose-dev.yml up --build`

## Настройка хоста для деплоя ansible
1. sudo apt install -y openssh-server sshpass
2. Настроить /etc/ssh/sshd_config


    PubkeyAuthentication no
    PasswordAuthentication yes
    ChallengeResponseAuthentication yes