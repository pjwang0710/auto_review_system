from app import crud
import os
import json
import requests
import random
import string
import openai


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
        detail = payload.get('pull_request')
        base_branch = detail.get('base', {}).get('ref', '').lower()
        compare_branch = detail.get('head', {}).get('ref', '').lower()
        detail['pr_link'] = payload.get('pull_request', {}).get('html_url')
        student = await crud.students.get_one(db, {'batch': BATCH, 'github_name': detail['user']['login']})
        student_branch = student.get('name', '').lower() + '_develop'
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
            progress = await crud.progresses.get_one(db, {'pr_link': detail.get('pr_link')})
            detail['progress'] = progress

        detail['student'] = student
        detail['assignment'] = assignment
    elif validate_type == VALIDATE_TYPES.COMMENT:
        detail = payload.get('comment')
        detail['pr_link'] = payload.get('issue', {}).get('html_url')

        # 1. find progress
        progress = await crud.progresses.get_one(db, {'pr_link': detail.get('pr_link')})
        if not progress:
            raise ValueError("error: comment on a wrong pull request, note: please contact PJ for this problem")

        student = await crud.students.get_one(db, {'id': progress.get('student_id')})
        assignment = await crud.assignments.get_one(db, {'id': progress.get('assignment_id')})

        detail['student'] = student
        detail['assignment'] = assignment
        detail['progress'] = progress

    return {
        'pr_link': detail.get('pr_link'),
        'merged_at': detail.get('merged_at'),
        'student': detail.get('student'),
        'assignment': detail.get('assignment'),
        'progress': detail.get('progress')
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


def get_commits(pr_number):
    uri = f'https://api.github.com/repos/AppWorks-School-Materials/Campus-Summer-Back-End/pulls/{pr_number}/commits'
    print("get commits to uri:", uri)
    headers = {
        'Accept': 'application/vnd.github.everest-preview+json',
        'Authorization': f"token {os.getenv('GITHUB_TOKEN')}",
    }
    response = requests.get(uri, headers=headers)
    commits = response.json()
    data = []
    for commit in commits:
        sha = commit.get('sha')
        uri = f'https://api.github.com/repos/AppWorks-School-Materials/Campus-Summer-Back-End/commits/{sha}'
        print("get commit", uri)
        headers = {
            'Accept': 'application/vnd.github.everest-preview+json',
            'Authorization': f"token {os.getenv('GITHUB_TOKEN')}",
        }
        response = requests.get(uri, headers=headers)
        files = response.json().get('files')
        file_meta = []
        for file in files:
            file_meta.append({
                'path': file.get('filename'),
                'patch': file.get('patch')
            })
        data.append({
            'commit_id': sha,
            'file_meta': file_meta
        })
    return data


def create_review(pr_number, commit_id, all_suggestion, event, comments):
    uri = f'https://api.github.com/repos/AppWorks-School-Materials/Campus-Summer-Back-End/pulls/{pr_number}/reviews'
    headers = {
        'Accept': 'application/vnd.github.everest-preview+json',
        'Authorization': f"token {os.getenv('GITHUB_TOKEN')}",
    }
    body = {
        'commit_id': commit_id,
        'body': all_suggestion,
        'event': event,
        'comments': comments
    }
    raw_body = json.dumps(body)
    response = requests.post(uri, data=raw_body, headers=headers)
    return response.json()


def code_review(code_change):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    messages = [{
        "role": "user", "content": f"""
            Evaluate the given code change on github
            '''{code_change} '''
            Please provide guidance and suggestions in a constructive manner, without directly giving the code and answers. Also, assess whether the submitted code passes the evaluation.
        """
    }]
    functions = [
        {
            "name": "code_review",
            "description": "Give some suggestion for these code change on github",
            "parameters": {
                "type": "object",
                "properties": {
                    "suggestion": {
                        "type": "string",
                        "description": "Provide suggestions for the code change."
                    },
                    "event": {
                        "type": "string",
                        "enum": ["APPROVE", "REQUEST_CHANGES", "COMMENT"],
                        "description": "Options for whether the current commit can pass"
                    }
                },
                "required": ["suggestion", "event"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    return json.loads(response_message["function_call"]["arguments"])


# def code_review(pr_number):
#     uri = 'https://api.github.com/repos/AppWorks-School-Materials/Campus-Summer-Back-End/dispatches'
#     print("post comment to uri:", uri)
#     headers = {
#         'Accept': 'application/vnd.github.everest-preview+json',
#         'Authorization': f"token {os.getenv('GITHUB_TOKEN')}",
#     }
#     body = json.dumps({'event_type': 'code-review', 'client_payload': {'pull_request_number': pr_number}})
#     response = requests.post(uri, data=body, headers=headers)
#     return response.json()
