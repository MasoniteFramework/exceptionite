DEFAULT_OPTIONS = {
    "options": {
        "editor": "vscode",
        "search_url": "https://www.google.com/search?q=",
        "links": {
            "doc": "https://docs.masoniteproject.com",
            "repo": "https://github.com/MasoniteFramework/masonite",
        },
        "stack": {"offset": 8, "shorten": True},
        "hide_sensitive_data": True,
    },
    "handlers": {
        "context": True,
        "solutions": {"stackoverflow": False, "possible_solutions": True},
        "recommendations": {"packages_updates": {"list": ["exceptionite"]}},
    },
}
