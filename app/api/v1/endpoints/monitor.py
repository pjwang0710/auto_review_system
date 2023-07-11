from app import crud
from app.db import get_database
from app.utils.exception import CustomizeException, CustomizeReturn
from app.utils.utils import VALIDATE_TYPES, parse_github_payload, post_comment, code_review, get_commits
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
    pr_number = None
    print('action:', payload.get('action'))
    if payload.get('action') == 'closed' and not payload.get('pull_request', {}).get('merged_at'):
        validate_type = VALIDATE_TYPES.CLOSED
    elif payload.get('pull_request'):
        if payload.get('pull_request', {}).get('merged_at'):
            validate_type = VALIDATE_TYPES.MERGE
        elif payload.get('action') == 'reopened' or payload.get('action') == 'opened' or payload.get('action') == 'synchronize':
            pr_number = payload.get('pull_request', {}).get('number')
            validate_type = VALIDATE_TYPES.PULL_REQUEST
        uri = payload.get('pull_request', {}).get('issue_url') + '/comments'
    elif payload.get('comment') and payload.get('comment', {}).get('body', '').lower().strip() == 'fixed':
        uri = payload.get('comment', {}).get('issue_url', '') + '/comments'
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
        if uri is not None:
            post_comment(uri, str(e))
        print('parse payload failed:', str(e))
        print('payload:', payload)
        return {
            'msg': str(e)
        }

    # 2. validate
    valid_result = None
    try:
        if validate_type == VALIDATE_TYPES.PULL_REQUEST or validate_type == VALIDATE_TYPES.COMMENT:
            valid_result = await validate(data['assignment']['part'], data['student']['server'])
            print("validResult:", valid_result)
    except Exception as e:
        print('validate failed,:', str(e))
        return {
            'msg': 'validate failed'
        }

    # 3. save change to DB
    print(validate_type)
    if validate_type == VALIDATE_TYPES.PULL_REQUEST:
        progress = {
            'student_id': data.get('student', {}).get('_id'),
            'assignment_id': data.get('assignment', {}).get('_id'),
            'pr_link': data.get('pr_link'),
            'status_id': valid_result.get('status'),
        }
        conditions = {
            'student_id': progress.get('student_id'),
            'assignment_id': progress.get('assignment_id'),
        }
        student_progress = await crud.progresses.get_one(db, conditions)
        if student_progress is None:
            _ = await crud.progresses.insert_one(db, progress)
        else:
            _ = await crud.progresses.update_one(db, conditions, progress)
    elif validate_type == VALIDATE_TYPES.COMMENT:
        _ = await crud.progresses.update_one(db, {
            'id': data.get('progress', {}).get('_id')
        }, {
            'status_id': valid_result.get('status')
        })
    elif validate_type == VALIDATE_TYPES.MERGE:
        _ = await crud.progresses.update_one(db, {
            'id':  data.get('progress', {}).get('_id')
        }, {
            'status_id': 3,
            'finished_at': datetime.datetime.strptime(data.get('merged_at'), '%Y-%m-%dT%H:%M:%SZ')
        })
    elif validate_type == VALIDATE_TYPES.CLOSED:
        _ = await crud.progresses.update_one(db, {
            'id': data.get('progress', {}).get('_id')
        }, {
            'status_id': 4,
        })

    # 4. post result
    if validate_type == VALIDATE_TYPES.PULL_REQUEST or validate_type == VALIDATE_TYPES.COMMENT:
        post_comment(uri, valid_result.get('message'))
        if (valid_result.get('message') == 'Congrats! You just passed the basic validation.'):
            commits = get_commits(pr_number)
            suggestions = []
            seen = {}
            for commit in commits[::-1]:
                for file in commit.get('file_meta'):
                    if not file.get('path').endswith(".js") and not file.get('path').endswith(".ts"):
                        continue
                    if seen.get(file.get('path')):
                        continue
                    patch = file.get('patch')
                    reviews = code_review(patch)
                    suggestions.append(f"filename: {file.get('path')} <br />suggestion: <br /> {reviews.get('suggestion')} <br />event: {reviews.get('event')}")
                    seen[file.get('path')] = True
            if suggestions == []:
                post_comment(uri, "[ChatGPT]<br /> .js file was not detected.")
            else:    
                post_comment(uri, "[ChatGPT]<br />" + "<br /><br />".join(suggestions).replace('\n', '<br />'))
