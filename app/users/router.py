from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.schemas import SUserRegister, SUserAuth, SUser, SUserGet
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import User
from app.users.rb import RBUser


router = APIRouter(prefix='/auth', tags=['Auth'])
get_router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/register/")
async def register_user(user_data: SUserRegister) -> dict:
    user = await UserDAO.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: SUserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    # is_admin = 
    return {'access_token': access_token, 'refresh_token': None}

@router.get("/me/")
async def get_me(user_data: User = Depends(get_current_user)) -> SUser:
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@router.get("/all_users/")
async def get_all_users(user_data: User = Depends(get_current_admin_user)) -> list[SUser]:
    return await UserDAO.find_all()


@router.put("/update_profile/")
async def update_user(
    user: SUser
) -> dict:
    try:
        print(user.dict())
        email = user.dict().pop('email')
        check = await UserDAO.update(filter_by={'email': email}, **user.dict())
        if check:
            return {"message": f"Жанр с ID {user.id} успешно обновлена!"}
        else:
            return {"message": "Ошибка обновления катгории или жанр не найден."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}


@get_router.get("/")
async def get_all_users(user_data: User = Depends(get_current_admin_user)) -> list[SUserGet]:
    return await UserDAO.find_all()


@get_router.get("/{user_id}", summary="Получить одного юзера по id")
async def get_user(user_id: int) -> SUser:
    response = await UserDAO.find_one_or_none_by_id(user_id)
    if response:
        return response
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователя с таким id не существует!')



@get_router.delete("/del/{user_id}")
async def dell_user_by_id(user_id: int) -> dict:
    check = await UserDAO.delete(id=user_id)
    if check:
        return {"message": f"Пользователь с ID {user_id} удален!"}
    else:
        return {"message": "Ошибка при удалении пользователя!"}
    

@get_router.post("/add/")
async def add_user(user: SUser) -> dict:
    check = await UserDAO.add(**user.dict())
    if check:
        return {"message": "Пользователь успешно добавлен!", "user": user}
    else:
        return {"message": "Ошибка при добавлении пользователя!"}
    

@get_router.put("/update/")
async def update_user(
    user: SUser
) -> dict:
    try:
        print(user.dict())
        email = user.dict().pop('email')
        check = await UserDAO.update(filter_by={'email': email}, **user.dict())
        if check:
            return {"message": f"Пользователь с ID {user.id} успешно обновлена!"}
        else:
            return {"message": "Ошибка обновления пользователя или пользователь не найден."}
    except Exception as e:
        return {"message": f"Ошибка: {str(e)}"}