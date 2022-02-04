import os
import requests

from .Block import Block


class StackOverflow(Block):

    name = "Stack Overflow"
    component = "StackOverflowBlock"
    tags = ["python"]

    def build(self):
        try:
            response = requests.get(
                "https://api.stackexchange.com/2.2/search/advanced?order=asc&sort=relevance&q='{0}'&body='{0}'&accepted=True&tagged={1}&site=stackoverflow".format(
                    self.handler.message(), ";".join(self.tags)
                )
            ).json()
        except requests.exceptions.ConnectionError:
            return

        accepted_answer_ids = []

        if not response.get("items"):
            response = requests.get(
                "https://api.stackexchange.com/2.2/search?order=desc&sort=relevance&intitle={}&site=stackoverflow&filter=!-*jbN-(0_ynL&tagged={}&key=k7C3UwXDt3J0xOpri8RPgA((".format(
                    self.handler.exception(), ";".join(self.tags)
                )
            ).json()

        for question in response.get("items", []):
            if "accepted_answer_id" in question:
                accepted_answer_ids.append(str(question["accepted_answer_id"]))

        self.count = len(response.get("items", []))

        answers = requests.get(
            "https://api.stackexchange.com/2.2/answers/{}?order=desc&sort=activity&site=stackoverflow".format(
                ";".join(accepted_answer_ids)
            )
        ).json()

        return {"questions": response["items"], "answers": answers}

    def has_content(self):
        return len(self.data.get("questions", [])) > 0
