FROM python:3.9-slim

LABEL maintainer="saper663ru@gmail.com"
LABEL author="saper663"

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install --upgrade pip
# RUN pip install -r /app/requirements.txt --no-cache-dir

# COPY ./cars .

# # CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cars.wsgi"]

ENV BUILD_ONLY_PACKAGES='wget' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # dockerize:
  DOCKERIZE_VERSION=v0.6.1 \
  # tini:
  TINI_VERSION=v0.19.0 \
  # poetry:
  POETRY_VERSION=1.1.7 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"


RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    $BUILD_ONLY_PACKAGES \
  && wget "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
  && rm "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" && dockerize --version \
  && wget -O /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini" \
  && chmod +x /usr/local/bin/tini && tini --version \
  && curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
  && poetry --version \
  && apt-get remove -y $BUILD_ONLY_PACKAGES \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./infra/entrypoint.sh /docker-entrypoint.sh

RUN chmod +x '/docker-entrypoint.sh'
  
COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry lock --no-update\
  && poetry install --no-dev --no-interaction --no-ansi \
  && rm -rf $POETRY_CACHE_DIR

ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]

COPY ./cars/ .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cars.wsgi"]
