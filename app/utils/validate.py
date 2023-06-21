import requests
from app.utils.utils import random_string

SUCCESS_MESSAGE = "Congrats! You just passed the basic validation." 


async def validate(part, server):
    print(f"validate part: {part} server: {server}")
    validator = validators[part-1]
    result = await validator(server)
    return result


async def validatePart1(server):
    return {
        'status': 1,
        'message': SUCCESS_MESSAGE
    }


async def validatePart2(server):
    return {
        'status': 1,
        'message': SUCCESS_MESSAGE
    }


async def validatePart3(server):
    api = f'{server}/api/1.0/users/signup'
    name = random_string(8)
    body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.post(api, body=body, headers=headers)
    if r.status_code != 200:
        return {
            'status': 2,
            'message': 'SignUp Failed'
        }
    r = requests.post(api, body=body, headers=headers)
    if r.status_code != 403:
        return {
            'status': 2,
            'message': 'Email Already Exists'
        }
    body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com"
    }
    r = requests.post(api, body=body, headers=headers)
    if r.status_code != 400:
        return {
            'status': 2,
            'message': 'Password Required'
        }
    body = {
        "name": f"user-{name}",
        "password": "test"
    }
    r = requests.post(api, body=body, headers=headers)
    if r.status_code != 400:
        return {
            'status': 2,
            'message': 'Email Required'
        }
    body = {
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    r = requests.post(api, body=body, headers=headers)
    if r.status_code != 400:
        return {
            'status': 2,
            'message': 'Name Required'
        }
    return {
        'status': 1,
        'message': SUCCESS_MESSAGE
    }


validators = [
    validatePart1,
    validatePart2,
    validatePart3
]