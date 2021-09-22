FROM python:3.8.3

RUN pip install -U pip \
    && pip install "poetry==1.1.8" \
    && poetry config virtualenvs.create false

# Install dependencies
COPY pyproject.toml /tmp
COPY poetry.lock /tmp

WORKDIR /tmp
RUN poetry install --no-interaction --no-ansi

COPY docker/django/.bashrc /root/