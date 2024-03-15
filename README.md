# Парсинг сайтов
1. Скачайте проект:<br>
```bash
git clone https://github.com/VeronikaChirkova/Parser.git
```
2. Создайте вртуальное окружение:<br>
```bash
python -m venv venv
```
3. Активируйте виртуальное окружение:<br>
```bash
. ./venv/bin/activate
```
4. Установите зависимости:<br>
```bash
pip install -r requirements.txt
```
5. Данный парсер собирает информацию (картинки и текст описания к ним )с сайтов:<br>
```text
    https://www.wildberries.ru - аксессуары для ванной
    https://ru.freepik.com - картинки котов
    https://www.cian.ru - квартиры
    https://tourist.tez-tour.com - отели в Турции
    https://avidreaders.ru - книги фантастика
    https://www.tvigle.ru - популярные фильмы
    https://skazkaflora.ru - букеты из роз
    https://ghtoys.ru - настольные игры
    https://nsk.winestyle.ru - вина
    https://sensorikagame.ru - развивающие игры для детей
```

## Запуск в докере
1. Создайте нового пользователя `appuser` без домашней директории и добавьте его в группу `appuser` на локальном ПК.<br>

```bash
useradd -M appuser -u 3000 -g 3000 && sudo usermod -L appuser &&sudo usermod -aG appuser appuser
```
Это необходимо для обеспечения безопасности, чтобы запуск процессов внутри контейнера осуществлялся от пользователя, который не имеет никаких прав на хостовой машине.<br>

UID (GID) пользователя в контейнере и пользователя за пределами контейнера, у которого есть соответствующие права на доступ к файлу, должны соответствовать.<br>

2. В Dockerfile необходимо прописать: UID (GID), создание пользователя и передачу ему прав, смену пользователя.<br>
```text
ARG UNAME=appuser
ARG UID
ARG GID

# create user
RUN groupadd -g ${GID} ${UNAME} &&\
useradd ${UNAME} -u ${UID} -g ${GID} &&\
usermod -L ${UNAME} &&\
usermod -aG ${UNAME} ${UNAME}

# chown all the files to the app user
RUN chown -R ${UNAME}:${UNAME} /app

USER ${UNAME}
```
3. Команда для создания образа (обязательно указать UID (GID)):<br>

```bash
docker build . --build-arg UID=3000 --build-arg GID=3000 -f Dockerfile -t parser
```
4. Создайте и запустите контейнер:<br>
```bash
docker run --rm --name -v /opt/docker_containers/parser/result/:/app/result/ parser parser
```
<br>
