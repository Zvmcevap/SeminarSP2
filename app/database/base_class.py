from typing import Any, Dict

from sqlalchemy.ext.declarative import as_declarative, declared_attr

class_registry: Dict = {}


# Base model to be inherited by all db models, SQLAlch uses em to m in orm
@as_declarative(class_registry=class_registry)
class Base:
    id: Any
    __name__: str

    # Generate tablename automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
