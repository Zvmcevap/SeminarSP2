import datetime
import logging

from sqlalchemy.orm import Session

from app.crud import crud_user
from app.schemas import schemas
from app.core.config import settings
from app.models import models
from app.database.session import engine

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    models.Base.metadata.create_all(bind=engine)
    user = crud_user.crud_user.get_by_username(db, username=settings.FIRST_SUPERUSER_NAME)
    if not user:
        user_in = schemas.UserSuperCreate(
            username=settings.FIRST_SUPERUSER_NAME,
            plain_password=settings.FIRST_SUPERUSER_PASSWORD,
            email=settings.FIRST_SUPERUSER_EMAIL,
            is_superuser=True,
        )

        crud_user.crud_user.create(db, obj_in=user_in)
    else:
        logger.warning(f"Skipping creating admin. Admin: {settings.FIRST_SUPERUSER_NAME} already exists.")