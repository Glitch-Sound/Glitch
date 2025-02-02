import traceback
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schema import activity as schema_activity
from crud import activity as crud_activity


router = APIRouter()

@router.get('/activity/{rid_items}', response_model=list[schema_activity.Activity])
def get_items(rid_items: int, db: Session = Depends(get_db)):
    try:
        result = crud_activity.get_activities(db, rid_items=rid_items)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f'error: {str(e)}') from e


@router.post('/activity/', response_model=schema_activity.Activity)
def create_project(target:schema_activity.ActivityCreate, db: Session = Depends(get_db)):
    try:
        result = crud_activity.create_activity(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f'error: {str(e)}') from e


@router.put('/activity/', response_model=schema_activity.Activity)
def update_project(target:schema_activity.ActivityUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_activity.update_activity(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.delete('/activity/{target}', response_model=dict)
def delete_project(target: int, db: Session = Depends(get_db)):
    try:
        crud_activity.delete_activity(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e
