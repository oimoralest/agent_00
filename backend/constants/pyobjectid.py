"""
Defines pydantic model for ObjectId
"""

from typing import Any

from bson.objectid import ObjectId
from pydantic_core import CoreSchema
from pydantic_core.core_schema import (
    chain_schema,
    is_instance_schema,
    json_or_python_schema,
    no_info_plain_validator_function,
    plain_serializer_function_ser_schema,
    str_schema,
    union_schema,
)


class PyObjectId(str):
    """
    Represents a Pydantic ObjectId
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, _source_type: Any, _handler: Any
    ) -> CoreSchema:
        """
        Get Pydantic Core Schema

        Args:
            _source_type: Source type
            _handler: Handler
        """
        return json_or_python_schema(
            json_schema=str_schema(),
            python_schema=union_schema(
                [
                    is_instance_schema(ObjectId),
                    chain_schema(
                        [str_schema(), no_info_plain_validator_function(cls.validate)]
                    ),
                ]
            ),
            serialization=plain_serializer_function_ser_schema(lambda x: str(x)),
        )

    @classmethod
    def validate(cls, value: Any) -> ObjectId:
        """
        Validate ObjectId

        Args:
            value: Value to validate
        """
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)
