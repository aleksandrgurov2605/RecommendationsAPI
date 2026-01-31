from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from app.utils.auth import get_current_user
from app.utils.unitofwork import UnitOfWork

if TYPE_CHECKING:
    from app.schemas.users import UserRead
    from app.utils.unitofwork import IUnitOfWork

UOWDep = Annotated["IUnitOfWork", Depends(UnitOfWork)]
UserDep = Annotated["UserRead", Depends(get_current_user)]
