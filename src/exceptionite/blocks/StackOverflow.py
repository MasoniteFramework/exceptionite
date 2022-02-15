import requests
import urllib
from ..Block import Block


class StackOverflow(Block):
    id = "stackoverflow"
    name = "Stack Overflow Answers"
    component = "StackOverflowBlock"
    tags = ["python"]
    api_url = "https://api.stackexchange.com/2.2/"
    empty_msg = "No solution found on Stack Overflow."
    disable_scrubbing = True

    def get_tags(self):
        return ";".join(self.tags)

    def build(self):
        query = urllib.parse.urlencode(
            {
                "order": "asc",
                "sort": "relevance",
                "q": self.handler.message(),
                "body": self.handler.message(),
                "accepted": True,
                "tagged": self.get_tags(),
                "site": "stackoverflow",
            }
        )

        try:
            response = requests.get(f"{self.api_url}search/advanced?{query}").json()
        except requests.exceptions.ConnectionError:
            return {}

        accepted_answer_ids = []

        if not response.get("items"):
            query = urllib.parse.urlencode(
                {
                    "order": "desc",
                    "sort": "relevance",
                    "intitle": self.handler.exception(),
                    "site": "stackoverflow",
                    "filter": "!-*jbN-(0_ynL",
                    "tagged": self.get_tags(),
                    "key": "k7C3UwXDt3J0xOpri8RPgA((",
                }
            )
            response = requests.get(f"{self.api_url}search/advanced?{query}").json()

        for question in response.get("items", []):
            if "accepted_answer_id" in question:
                accepted_answer_ids.append(str(question["accepted_answer_id"]))

        query = urllib.parse.urlencode(
            {"order": "desc", "sort": "activity", "site": "stackoverflow"}
        )
        answers = requests.get(
            f"{self.api_url}answers/{';'.join(accepted_answer_ids)}?{query}"
        ).json()

        return {"questions": response["items"], "answers": answers}

    def has_content(self):
        return len(self.data.get("questions", [])) > 0
