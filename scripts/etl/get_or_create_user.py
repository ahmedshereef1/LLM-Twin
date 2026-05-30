from zenml import get_step_context, step
from loguru import logger
from typing_extensions import Annotated

from services.application import utils
from services.domain.documents import UserDocument


@step
def get_or_create_user(user_name: str) -> Annotated[UserDocument, "user"]:
    logger.info(f"Getting or create user: {user_name}")

    first_name, last_name = utils.split_user_name(user_name)

    user = UserDocument.get_or_create(first_name=first_name, last_name=last_name)

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="user", metadata=_get_metadata(user_name, user)
    )

    return user


def _get_metadata(user_name: str, user: UserDocument) -> dict:
    return {
        "query": {"user_name": user_name},
        "retrieved": {
            "user_id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    }
