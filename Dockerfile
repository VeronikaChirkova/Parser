FROM python:3.10.12

#docker build --build-arg UID=3000 --build-arg GID=3000...
ARG UNAME=appuser
ARG UID=3000
ARG GID=3000

# create user
RUN groupadd -g ${GID} ${UNAME} &&\
useradd ${UNAME} -u ${UID} -g ${GID} &&\
usermod -L ${UNAME} &&\
usermod -aG ${UNAME} ${UNAME}

RUN apt update && apt -y upgrade && apt -y install nano && apt -y install bash bash-doc bash-completion
RUN apt install -y libglib2.0-0\
    libnss3 \
    libgconf-2-4 \
    libfontconfig1

# install chrome-stable
RUN wget https://dl-ssl.google.com/linux/linux_signing_key.pub -O /tmp/google.pub
RUN gpg --no-default-keyring --keyring /etc/apt/keyrings/google-chrome.gpg --import /tmp/google.pub
RUN echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p /home/appuser/.cache/selenium
RUN chown -R ${UNAME}:${UNAME} /home/appuser/.cache/selenium

COPY . .

# chown all the files to the app user
RUN chown -R ${UNAME}:${UNAME} /app

USER ${UNAME}

CMD [ "python", "parser.py" ]
