from pydantic import create_model, BaseModel


def create_base_schema(*fields):
    dynamic_model = create_model(
        "BaseSchema", **{field: (str, ...) for field in fields}
    )

    class BaseSchema(BaseModel):
        __annotations__ = dynamic_model.__annotations__

    return BaseSchema
