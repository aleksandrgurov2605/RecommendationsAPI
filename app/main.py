import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from app.db.database import Base, engine
from app.errors.carts_exceptions import CartUnitNotFoundError, NotEnoughItemsError
from app.errors.categories_exceptions import CategoryParentNotFoundError, CategoryNotFoundError, CategoryParentError
from app.errors.purchases_exceptions import PurchaseNotFoundError
from app.errors.users_exceptions import UserNotFoundError, CredentialsError, TokenHasExpiredError, \
    EmailAlreadyTakenError
from app.errors.items_exceptions import ItemNotFoundError, WrongCategoryNotFoundError, ItemHasNoPriceError
from app.routers.categories import router as categories_router
from app.routers.users import router as users_router
from app.routers.items import router as items_router
from app.routers.carts import router as carts_router
from app.routers.purchases import router as purchases_router
from app.models import *  # noqa
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Запрос: {request.method} {request.url.path}")
    response = await call_next(request)
    process_time = round(time.time() - start_time, 4)
    logger.info(f"Ответ: {response.status_code} (время: {process_time} сек.)")
    return response


@app.get('/')
async def root():
    return {'message': 'Hello World'}


app.include_router(categories_router)
app.include_router(users_router)
app.include_router(items_router)
app.include_router(carts_router)
app.include_router(purchases_router)


@app.exception_handler(CategoryNotFoundError)
async def category_not_found_exception_handler(request: Request, exc: CategoryNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(CategoryParentNotFoundError)
async def category_parent_not_found_exception_handler(request: Request, exc: CategoryParentNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )


@app.exception_handler(CategoryParentError)
async def category_parent_exception_handler(request: Request, exc: CategoryParentError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message},
    )


@app.exception_handler(UserNotFoundError)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(ItemNotFoundError)
async def item_not_found_exception_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )


@app.exception_handler(WrongCategoryNotFoundError)
async def wrong_category_id_exception_handler(request: Request, exc: WrongCategoryNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": exc.message},
    )


@app.exception_handler(CredentialsError)
async def credentials_exception_handler(request: Request, exc: CredentialsError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
    )


@app.exception_handler(TokenHasExpiredError)
async def token_has_expired_exception_handler(request: Request, exc: TokenHasExpiredError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message},
    )


@app.exception_handler(CartUnitNotFoundError)
async def cart_unit_not_found_exception_handler(request: Request, exc: CartUnitNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )

@app.exception_handler(EmailAlreadyTakenError)
async def email_already_taken_exception_handler(request: Request, exc: EmailAlreadyTakenError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )

@app.exception_handler(NotEnoughItemsError)
async def not_enough_items_exception_handler(request: Request, exc: NotEnoughItemsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": exc.message},
    )

@app.exception_handler(ItemHasNoPriceError)
async def item_has_no_price_exception_handler(request: Request, exc: ItemHasNoPriceError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={"detail": exc.message},
    )

@app.exception_handler(PurchaseNotFoundError)
async def purchase_not_found_exception_handler(request: Request, exc: PurchaseNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
