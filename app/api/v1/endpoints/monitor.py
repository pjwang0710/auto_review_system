from app import crud
from app.db import get_database
from app.utils.exception import CustomizeException, CustomizeReturn
from app.utils.utils import VALIDATE_TYPES, parse_github_payload, post_comment
from app.utils.validate import validate

import datetime
from typing import Any
from fastapi import APIRouter, Depends, Request


router = APIRouter()


@router.post("/progresses")
async def add_progresses(request: Request, db=Depends(get_database)) -> Any:
    payload = await request.json()

    uri = None
    validate_type = None
    if payload['action'] == 'closed' and not payload['pull_request']['merged_at']:
        validate_type = VALIDATE_TYPES.CLOSED
    elif payload['pull_request']:
        if payload['pull_request']['merged_at']:
            validate_type = VALIDATE_TYPES.MERGE
        elif payload['action'] == 'opened':
            validate_type = VALIDATE_TYPES.PULL_REQUEST
        uri = payload['pull_request']['issue_url'] + '/comments'
    elif payload['comment'] and payload['comment']['body'].lower().strip() == 'fixed':
        uri = payload['comment']['issue_url'] + '/comments'
        validate_type = VALIDATE_TYPES.COMMENT

    if not validate_type:
        print("payload without valid type")
        return

    print("validateType:", validate_type)

    # 1. parse payload
    data = None
    try:
        data = await parse_github_payload(db, payload, validate_type)
        print('payload data:', data)
    except Exception as e:
        post_comment(uri, e.message)
        print('parse payload failed:', e.message)
        print('payload:', payload)
        return {
            'msg': e.message
        }

    # 2. validate
    valid_result = None
    try:
        if validate_type == VALIDATE_TYPES.PULL_REQUEST or validate_type == VALIDATE_TYPES.COMMENT:
            valid_result = await validate(data['assignment']['part'], data['student']['server'])
            print("validResult:", valid_result)
    except Exception as e:
        print('validate failed,:', e.message)
        return {
            'msg': 'validate failed'
        }

    # 3. save change to DB
    print(validate_type)
    if validate_type == VALIDATE_TYPES.PULL_REQUEST:
        progress = {
            'student_id': data['student']['_id'],
            'assignment_id': data['assignment']['_id'],
            'pr_link': data['pr_link'],
            'status_id': valid_result['status'],
        }
        conditions = {
            'student_id': progress['student_id'],
            'assignment_id': progress['assignment_id'],
        }
        student_progress = await crud.progresses.get_one(db, conditions)
        if student_progress is None:
            _ = await crud.progresses.insert_one(db, progress)
        else:
            _ = await crud.progresses.update_one(db, conditions, progress)
    elif validate_type == VALIDATE_TYPES.COMMENT:
        _ = await crud.progresses.update_one(db, {
            'id': data['progress']['_id']
        }, {
            'status_id': valid_result['status']
        })
    elif validate_type == VALIDATE_TYPES.MERGE:
        _ = await crud.progresses.update_one(db, {
            'id': data['progress']['_id']
        }, {
            'status_id': 3,
            'finished_at': datetime.datetime(data['merged_at'])
        })
    elif validate_type == VALIDATE_TYPES.CLOSED:
        _ = await crud.progresses.update_one(db, {
            'id': data['progress']['_id']
        }, {
            'status_id': 4,
        })

    # 4. post result
    if validate_type == VALIDATE_TYPES.PULL_REQUEST or validate_type == VALIDATE_TYPES.COMMENT:
        post_comment(uri, valid_result['message'])
