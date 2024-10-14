import traceback
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

import sys
sys.path.append('~/app')

from database import get_db
from schema import summary as schema_summary
from crud import summary as crud_summary


router = APIRouter()

@router.get('/summary/project/{id_project}', response_model=list[schema_summary.SummaryItem])
def get_summary_project(id_project: int, db: Session = Depends(get_db)):
    try:
        result = crud_summary.getSummariesProject(db, id_project)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/summary/item/{rid_items}', response_model=list[schema_summary.SummaryItem])
def get_summary_item(rid_items: int, db: Session = Depends(get_db)):
    try:
        result = crud_summary.getSummariesItem(db, rid_items)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/summary/user/{id_project}/{rid_users}', response_model=list[schema_summary.SummaryUser])
def get_summary_item(id_project: int, rid_users: int, db: Session = Depends(get_db)):
    try:
        result = crud_summary.getSummariesUser(db, id_project, rid_users)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


