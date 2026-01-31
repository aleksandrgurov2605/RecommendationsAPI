from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from app.utils.auth import get_current_user
from app.utils.unitofwork import UnitOfWork

if TYPE_CHECKING:
    from app.utils.unitofwork import IUnitOfWork
    from app.schemas.users import UserRead

UOWDep = Annotated["IUnitOfWork", Depends(UnitOfWork)]
UserDep = Annotated["UserRead", Depends(get_current_user)]
