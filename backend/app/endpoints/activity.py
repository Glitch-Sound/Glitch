import traceback
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

import sys
sys.path.append('~/app')

from database import get_db
from schema import activity as schema_activity
from crud import activity as crud_activity


router = APIRouter()

@router.get('/activity/{rid_items}', response_model=list[schema_activity.Activity])
def get_items(rid_items: int, db: Session = Depends(get_db)):
    try:
        result = crud_activity.getActivities(db, rid_items=rid_items)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f'error: {str(e)}')


@router.post('/activity/', response_model=schema_activity.Activity)
def create_project(target:schema_activity.ActivityCreate, db: Session = Depends(get_db)):
    try:
        result = crud_activity.createActivity(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f'error: {str(e)}')


@router.put('/activity/', response_model=schema_activity.Activity)
def update_project(target:schema_activity.ActivityUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_activity.updateActivity(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.delete('/activity/{target}', response_model=dict)
def delete_project(target: int, db: Session = Depends(get_db)):
    try:
        crud_activity.deleteActivity(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')
