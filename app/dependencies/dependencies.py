from typing import Annotated

from fastapi import Depends

from app.utils.auth import get_current_user
from app.utils.unitofwork import UnitOfWork

UOWDep = Annotated["IUnitOfWork", Depends(UnitOfWork)]  # noqa: F821
UserDep = Annotated["UserRead", Depends(get_current_user)]  # noqa: F821
