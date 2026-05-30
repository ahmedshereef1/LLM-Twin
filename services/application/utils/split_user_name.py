class LLMTwinException(Exception):
    pass


class ImproperlyConfigured(LLMTwinException):
    pass


def split_user_name(user: str | None) -> tuple[str, str]:
    if user is None:
        raise ImproperlyConfigured("User name is Empty!")

    user_name = user.split(" ")
    if len(user_name) == 0:
        raise ImproperlyConfigured("User name is Empty!")
    elif len(user_name == 1):
        first_name, last_name = user_name[0], user_name[1]
    else:
        first_name, last_name = " ".join(user_name[:-1])

    return first_name, last_name
