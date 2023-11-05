import logging
import os
import random

import sentry_sdk
from flask import Flask, request
from sentry_sdk.integrations.flask import FlaskIntegration

SENTRY_DSN = os.environ.get("SENTRY_DSN")


sentry_sdk.init(
    dsn=SENTRY_DSN,
    enable_tracing=True,
    integrations=[
        FlaskIntegration(
            transaction_style="url",
        ),
    ],
)

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is requred')


@app.route('/sentry-test')
def sentry_test():
    raise Exception("This is a test exception for Sentry!")


@app.route('/')
def index():
    result = random.randint(1, 50)
    app.logger.info(f'Пользователю досталось число {result}')
    return f"Ваше число {result}! {SENTRY_DSN}"
