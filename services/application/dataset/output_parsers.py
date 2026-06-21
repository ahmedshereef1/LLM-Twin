from langchain_core.output_parsers import PydanticOutputParser
from loguru import logger


class ListPydanticOutputParser(PydanticOutputParser):
    def _parse_obj(self, obj: dict | list):
        logger.info(f"Parser received type: {type(obj)}")
        if isinstance(obj, list):
            return [
                super(ListPydanticOutputParser, self)._parse_obj(obj_) for obj_ in obj
            ]
        else:
            return super(ListPydanticOutputParser, self)._parse_obj(obj)
