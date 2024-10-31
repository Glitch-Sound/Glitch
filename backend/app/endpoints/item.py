import traceback
from fastapi import Query, Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

import sys
sys.path.append('~/app')

from database import get_db, SessionLocal  
from schema import item as schema_item
from crud import item as crud_item
from crud.item import ItemParam, ExtractType, updateSummary
from crud import item as crud_item


router = APIRouter()

def scheduledItem():
    try:
        pass

    except Exception as e:
        print(traceback.format_exc())


@router.get('/item/incomplete/{id_project}', response_model=list[schema_item.Item])
def get_items_incomplete(id_project: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.INCOMPLETE.value, id_project=id_project)
        result = crud_item.getItems(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/item/all/{id_project}', response_model=list[schema_item.Item])
def get_items_all(id_project: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.ALL.value, id_project=id_project)
        result = crud_item.getItems(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/item/high-risk/{id_project}', response_model=list[schema_item.Item])
def get_items_high_risk(id_project: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.HIGH_RISK.value, id_project=id_project)
        result = crud_item.getItems(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/item/alert/{id_project}', response_model=list[schema_item.Item])
def get_items_alert(id_project: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.ALERT.value, id_project=id_project)
        result = crud_item.getItems(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/item/assignment/{id_project}/{target}', response_model=list[schema_item.Item])
def get_items_assignment(id_project: int, target: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.ASSIGNMENT.value, id_project=id_project, rid_users=target)
        result = crud_item.getItems(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/item/relation/{id_project}/{target}', response_model=list[schema_item.Item])
def get_items_relation(id_project: int, target: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.RELATION.value, id_project=id_project, rid_items=target)
        result = crud_item.getItems(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/item/search/{id_project}/{target}', response_model=list[schema_item.Item])
def get_items_search(id_project: int, target: str, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.SEARCH.value, id_project=id_project, search=target)
        result = crud_item.getItems(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/item/range/{id_project}', response_model=list[schema_item.ItemRange])
def get_items_search(id_project: int, db: Session = Depends(get_db)):
    try:
        result = crud_item.getItemRange(db, id_project)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/item/summary-user/{id_project}/{target}', response_model=list[schema_item.Item])
def get_items_search(id_project: int, target: int, db: Session = Depends(get_db)):
    try:
        params = ItemParam(type_extract=ExtractType.SUMMARY_USER.value, id_project=id_project, rid_users=target)
        result = crud_item.getItems(db, params)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/item/state/', response_model=schema_item.Item)
def update_item_state(target:schema_item.StateUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.updateItemState(db, target.rid, target.state)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get('/projects/', response_model=list[schema_item.Project])
def get_items(db: Session = Depends(get_db)):
    try:
        result = crud_item.getProjects(db)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.post('/project/', response_model=schema_item.Item)
def create_project(target:schema_item.ProjectCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.createProject(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/project/', response_model=schema_item.Item)
def update_project(target:schema_item.ProjectUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.updateProject(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.delete('/project/{target}', response_model=dict)
def delete_project(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.deleteProject(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.post('/event/', response_model=schema_item.Item)
def create_event(target:schema_item.EventCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.createEvent(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/event/', response_model=schema_item.Item)
def update_event(target:schema_item.EventUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.updateEvent(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.delete('/event/{target}', response_model=dict)
def delete_event(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.deleteEvent(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.post('/feature/', response_model=schema_item.Item)
def create_feature(target:schema_item.FeatureCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.createFeature(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/feature/', response_model=schema_item.Item)
def update_feature(target:schema_item.FeatureUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.updateFeature(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.delete('/feature/{target}', response_model=dict)
def delete_feature(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.deleteFeature(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.post('/story/', response_model=schema_item.Item)
def create_story(target:schema_item.StoryCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.createStory(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/story/', response_model=schema_item.Item)
def update_story(target:schema_item.StoryUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.updateStory(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.delete('/story/{target}', response_model=dict)
def delete_story(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.deleteStory(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.post('/task/', response_model=schema_item.Item)
def create_task(target:schema_item.TaskCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.createTask(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/task/', response_model=schema_item.Item)
def update_task(target:schema_item.TaskUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.updateTask(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.delete('/task/{target}', response_model=dict)
def delete_task(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.deleteTask(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/task/priority', response_model=schema_item.Item)
def update_task(target:schema_item.TaskPriorityUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.updateTaskPriority(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.post('/bug/', response_model=schema_item.Item)
def create_bug(target:schema_item.BugCreate, db: Session = Depends(get_db)):
    try:
        result = crud_item.createBug(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/bug/', response_model=schema_item.Item)
def update_bug(target:schema_item.BugUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.updateBug(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.delete('/bug/{target}', response_model=dict)
def delete_bug(target: int, db: Session = Depends(get_db)):
    try:
        crud_item.deleteBug(db, target)
        return {'result': 'success'}

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.put('/bug/priority', response_model=schema_item.Item)
def update_task(target:schema_item.BugPriorityUpdate, db: Session = Depends(get_db)):
    try:
        result = crud_item.updateBugPriority(db, target)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')


@router.get("/item/hierarchy/{id_project}", response_model=schema_item.ItemHierarchy)
def get_hierarchy(id_project: int, db: Session = Depends(get_db)):
    try:
        result = crud_item.getHierarchy(db, id_project)
        return result

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'error: {str(e)}')
