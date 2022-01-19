FROM python:3.8-slim

WORKDIR /opt
COPY app/ app
RUN python3.8 -m venv .env
RUN .env/bin/pip install -r app/requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y gnupg2 curl
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
&& echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
&& apt-get update \
&& apt-get install -y yarn 
 
WORKDIR /opt/app/web
RUN yarn && yarn build
RUN rm -rf node_modules
ENV VUE_APP_SERVER_URL="${VUE_APP_SERVER_URL}"


WORKDIR /opt
ENV SERVER_URL="${SERVER_URL}"
ENV PG_USER="${PG_USER}"
ENV PG_PASSWORD="${PG_PASSWORD}"
ENV PG_HOST="${PG_HOST}"
ENV PG_PORT="${PG_PORT}"
ENV PG_DBNAME="${PG_DBNAME}"

CMD [".env/bin/python", "-m", "app.main"]




