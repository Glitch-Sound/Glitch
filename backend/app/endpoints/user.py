import traceback
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

import sys
sys.path.append('~/app')

from database import get_db
from schema import user as schema_user
from crud import user as crud_user


router = APIRouter()

@router.get('/user/', response_model=list[schema_user.User])
def get_users(db: Session = Depends(get_db)):
    try:
        result = crud_user.getUsers(db)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/user/project/{id_project}', response_model=list[schema_user.User])
def get_users(id_project: int, db: Session = Depends(get_db)):
    try:
        result = crud_user.getUsersProject(db, id_project)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')



@router.get('/user/{rid_users}', response_model=schema_user.User)
def get_user(rid_users: int, db: Session = Depends(get_db)):
    try:
        result = crud_user.getUser(db, rid_users)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.post('/user/', response_model=schema_user.User)
def create_user(target: schema_user.UserCreate, db: Session = Depends(get_db)):
    try:
        result = crud_user.createUser(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/user/', response_model=schema_user.User)
def update_user(target: schema_user.UserUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_user.updateUser(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.delete('/user/{target}', response_model=dict)
def delete_user(target: int, db: Session = Depends(get_db)):
    try:
        crud_user.deleteUser(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/login/', response_model=schema_user.User)
def login(target: schema_user.Login, db: Session = Depends(get_db)):
    try:
        result = crud_user.login(db, target)
        if result is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')
