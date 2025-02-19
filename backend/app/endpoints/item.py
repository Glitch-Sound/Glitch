import traceback
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from schema import item as schema_item
from crud import item as crud_item
from crud.item import ItemParam, ExtractType


router = APIRouter()

def scheduled_item(db: Session = Depends(get_db)):
    try:
        crud_item.update_summary(db)

    except Exception as e:
        print(traceback.format_exc())
        raise e


@router.get('/item/incomplete/{id_project}', response_model=list[schema_item.Item])
def get_items_incomplete(id_project: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.INCOMPLETE.value, id_project=id_project)
        result = crud_item.get_items(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get('/item/all/{id_project}', response_model=list[schema_item.Item])
def get_items_all(id_project: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.ALL.value, id_project=id_project)
        result = crud_item.get_items(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get('/item/high-risk/{id_project}', response_model=list[schema_item.Item])
def get_items_high_risk(id_project: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.HIGH_RISK.value, id_project=id_project)
        result = crud_item.get_items(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get('/item/alert/{id_project}', response_model=list[schema_item.Item])
def get_items_alert(id_project: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.ALERT.value, id_project=id_project)
        result = crud_item.get_items(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get('/item/assignment/{id_project}/{target}', response_model=list[schema_item.Item])
def get_items_assignment(id_project: int, target: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.ASSIGNMENT.value, id_project=id_project, rid_users=target)
        result = crud_item.get_items(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get('/item/relation/{id_project}/{target}', response_model=list[schema_item.Item])
def get_items_relation(id_project: int, target: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.RELATION.value, id_project=id_project, rid_items=target)
        result = crud_item.get_items(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get('/item/search/{id_project}/{target}', response_model=list[schema_item.Item])
def get_items_search(id_project: int, target: str, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.SEARCH.value, id_project=id_project, search=target)
        result = crud_item.get_items(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get("/item/notice/{id_project}", response_model=list[schema_item.Item])
def get_items_notice(id_project: int, db: Session = Depends(get_db)):
    try:
        result = crud_item.get_items_notice(db, id_project)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get('/item/range/{id_project}', response_model=list[schema_item.ItemRange])
def get_items_range(id_project: int, db: Session = Depends(get_db)):
    try:
        result = crud_item.get_items_range(db, id_project)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get('/item/summary-user/{id_project}/{target}', response_model=list[schema_item.Item])
def get_items_summary_user(id_project: int, target: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.SUMMARY_USER.value, id_project=id_project, rid_users=target)
        result = crud_item.get_items(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.put('/item/state/', response_model=schema_item.Item)
def update_item_state(target:schema_item.StateUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.update_item_state(db, target.rid, target.state)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get('/projects/', response_model=list[schema_item.Project])
def get_items(db: Session = Depends(get_db)):
    try:
        result = crud_item.get_projects(db)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.post('/project/', response_model=schema_item.Item)
def create_project(target:schema_item.ProjectCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.create_project(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.put('/project/', response_model=schema_item.Item)
def update_project(target:schema_item.ProjectUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.update_project(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.delete('/project/{target}', response_model=dict)
def delete_project(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.delete_project(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.post('/event/', response_model=schema_item.Item)
def create_event(target:schema_item.EventCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.create_event(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.put('/event/', response_model=schema_item.Item)
def update_event(target:schema_item.EventUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.update_event(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.delete('/event/{target}', response_model=dict)
def delete_event(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.delete_event(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.post('/feature/', response_model=schema_item.Item)
def create_feature(target:schema_item.FeatureCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.create_feature(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.put('/feature/', response_model=schema_item.Item)
def update_feature(target:schema_item.FeatureUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.update_feature(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.delete('/feature/{target}', response_model=dict)
def delete_feature(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.delete_feature(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.post('/story/', response_model=schema_item.Item)
def create_story(target:schema_item.StoryCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.create_story(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.put('/story/', response_model=schema_item.Item)
def update_story(target:schema_item.StoryUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.update_story(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.delete('/story/{target}', response_model=dict)
def delete_story(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.delete_story(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.post('/task/', response_model=schema_item.Item)
def create_task(target:schema_item.TaskCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.create_task(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.put('/task/', response_model=schema_item.Item)
def update_task(target:schema_item.TaskUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.update_task(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.delete('/task/{target}', response_model=dict)
def delete_task(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.delete_task(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.put('/task/priority', response_model=schema_item.Item)
def update_task_priority(target:schema_item.TaskPriorityUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.update_task_priority(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.post('/bug/', response_model=schema_item.Item)
def create_bug(target:schema_item.BugCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.create_bug(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.put('/bug/', response_model=schema_item.Item)
def update_bug(target:schema_item.BugUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.update_bug(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.delete('/bug/{target}', response_model=dict)
def delete_bug(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.delete_bug(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.put('/bug/priority', response_model=schema_item.Item)
def update_bug_priority(target:schema_item.BugPriorityUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.update_bug_priority(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e


@router.get("/item/hierarchy/{id_project}", response_model=schema_item.ItemHierarchy)
def get_hierarchy(id_project: int, db: Session = Depends(get_db)):
    try:
        result = crud_item.get_hierarchy(db, id_project)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e

@router.get("/item/relation-rid/{target}", response_model=list[schema_item.RID])
def get_items_relation_rid(target: int, db: Session = Depends(get_db)):
    try:
        result = crud_item.get_items_relation_rid(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}') from e
