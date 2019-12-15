import os

import jinja2
import requests
from jinja2 import (ChoiceLoader, DictLoader, Environment, PackageLoader,
                    select_autoescape)


class StackOverflowIntegration:

    name = "StackOverflow"

    def content(self, handler):
        response = requests.get(
            'https://api.stackexchange.com/2.2/search?order=desc&sort=votes&intitle={}&site=stackoverflow&filter=!-*jbN-(0_ynL&tagged=python&key=k7C3UwXDt3J0xOpri8RPgA(('.format(
                handler.message())
        ).json()

        accepted_answer_ids = []

        if not response['items']:
            response = requests.get(
                'https://api.stackexchange.com/2.2/search?order=desc&sort=votes&intitle={}&site=stackoverflow&filter=!-*jbN-(0_ynL&tagged=python&key=k7C3UwXDt3J0xOpri8RPgA(('.format(
                    handler.exception())
            ).json()

        for question in response.get('items', []):
            if 'accepted_answer_id' in question:
                accepted_answer_ids.append(str(question['accepted_answer_id']))

        answers = requests.get(
            'https://api.stackexchange.com/2.2/answers/{}?order=desc&sort=activity&site=stackoverflow'.format(
                ';'.join(accepted_answer_ids))
        ).json()

        current_path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(current_path, 'templates/stackoverflow.html'), 'r') as f:
            overflow_exception = f.read()

        loader = DictLoader({
            'stackoverflow.html': overflow_exception,
        })

        environment = Environment(
            loader=loader,
            autoescape=select_autoescape(['html', 'xml'])
        )

        return environment.get_template('stackoverflow.html').render({
            'questions': response['items'], 'answers': answers})
