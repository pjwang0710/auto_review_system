from app import crud
import os
import json
import requests
import random
import string


class VALIDATE_TYPES:
    PULL_REQUEST = 'pull_request'
    COMMENT = 'comment'
    MERGE = 'merge'
    CLOSED = 'closed'


def random_string(length):
    letters = string.ascii_letters + string.digits  # includes both uppercase and lowercase letters, and digits
    result = ''.join(random.choice(letters) for _ in range(length))
    return result


async def parse_github_payload(db, payload, validate_type):
    BATCH = 3.5
    detail = None
    if validate_type == VALIDATE_TYPES.PULL_REQUEST or validate_type == VALIDATE_TYPES.MERGE or validate_type == VALIDATE_TYPES.CLOSED:
        detail = payload['pull_request']
        base_branch = detail['base']['ref'].lower()
        compare_branch = detail['head']['ref'].lower()
        detail['pr_link'] = payload['pull_request']['html_url']
        print({'batch': BATCH, 'github_name': detail['user']['login']})
        student = await crud.students.get_one(db, {'batch': BATCH, 'github_name': detail['user']['login']})
        print(student)
        student_branch = student['name'].lower() + '_develop'
        # 1. check base branch (should be <student_name>_develop)
        if base_branch != student_branch:
            print(f"base branch should be: {student_branch}")
            raise ValueError(f"error: base branch should be **{student_branch}**, note: please **Close** this pull request and create a new one")

        # 2. check compare branch (should be week_x_part_y and can be found in DB in this batch)
        assignment = await crud.assignments.get_one(db, {'batch': BATCH, 'name': compare_branch})
        if not assignment:
            raise ValueError("error: compare branch name should be **week_n_part_m**, note: please **Close** this pull request and create a new one")

        # 3. get progress when the type is merge
        if validate_type == VALIDATE_TYPES.MERGE or validate_type == VALIDATE_TYPES.CLOSED:
            progress = await crud.progresses.get_one(db, {'pr_link': detail['pr_link']})
            detail['progress'] = progress

        detail['student'] = student
        detail['assignment'] = assignment
    elif validate_type == VALIDATE_TYPES.COMMENT:
        detail = payload['comment']
        detail['pr_link'] = payload['issue']['html_url']

        # 1. find progress
        progress = await crud.progresses.get_one(db, {'pr_link': detail['pr_link']})
        if not progress:
            raise ValueError("error: comment on a wrong pull request, note: please contact PJ for this problem")

        student = await crud.students.get_one(db, {'id': progress['student_id']})
        assignment = await crud.assignments.get_one(db, {'id': progress['assignment_id']})

        detail['student'] = student
        detail['assignment'] = assignment
        detail['progress'] = progress

    return {
        'pr_link': detail['pr_link'],
        'merged_at': detail['merged_at'],
        'student': detail['student'],
        'assignment': detail['assignment'],
        'progress': detail['progress'],
    }


def post_comment(uri, content):
    print("post comment to uri:", uri)
    headers = {
        'User-Agent': 'request',
        'Authorization': f"token {os.getenv('GITHUB_TOKEN')}"
    }
    body = json.dumps({"body": json.dumps(content)})
    response = requests.post(uri, data=body, headers=headers)
    return response