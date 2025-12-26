Инструкция по запуску: 
1. git clone https://github.com/Yarnyan/webapi
2. cd webapi
3. Открываете терминал пишите: docker compose up --build или docker-compose up --build в зависисти от вашей версии(подразумевается что у вас уже открыт локально докер)
4. что бы проверить nuts, открываем два терминала и пишем в одном: 
docker run --rm -it --network test_default natsio/nats-box \
    nats sub weather.updates -s nats://nats:4222
   а в другом: docker run --rm --network test_default natsio/nats-box \
    nats pub weather.updates -s nats://nats:4222 '{"temp":99.9,"humidity":50}'
5. поздравляю проект полностью рабочий
