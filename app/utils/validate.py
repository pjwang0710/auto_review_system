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

    def signup(body, status_code, err_msg):
        api = f'{server}/api/1.0/users/signup'
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(api, json=body, headers=headers)
        if r.status_code != status_code:
            raise ValueError(err_msg)
        
    name = random_string(8)
    user_body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    name = random_string(8)
    wo_password_body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com"
    }
    name = random_string(8)
    empty_password_body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com",
        "password": ''
    }
    name = random_string(8)
    wo_name_body = {
        "email": f"user-{name}@test.com",
        "password": 'test'
    }
    name = random_string(8)
    empty_name_body = {
        "name": "",
        "email": f"user-{name}@test.com",
        "password": 'test'
    }
    name = random_string(8)
    wo_email_body = {
        "name": f"user-{name}",
        "password": 'test'
    }
    name = random_string(8)
    empty_email_body = {
        "name": f"user-{name}",
        "email": "",
        "password": 'test'
    }
    invalid_email_body = {
        "name": f"user-{name}",
        "email": "123456798",
        "password": 'test'
    }
    try:
        signup(user_body, 200, f'SignUp Failed, input: {user_body}')
        signup(user_body, 403, f'After inputting the same data twice, there was no 403 error thrown. The input data was: {user_body}')
        signup(wo_password_body, 403, f'Password field was not entered, but no 400 error was thrown. The input data was: {wo_password_body}')
        signup(wo_name_body, 403, f'Name field was not entered, but no 400 error was thrown. The input data was: {wo_name_body}')
        signup(wo_email_body, 403, f'Email field was not entered, but no 400 error was thrown. The input data was: {wo_email_body}')
        signup(empty_password_body, 400, f'Password is empty, but no 400 error was thrown. The input data was: {empty_password_body}')
        signup(empty_name_body, 400, f'Name is empty, but no 400 error was thrown. The input data was: {empty_name_body}')
        signup(empty_email_body, 400, f'Email is empty, but no 400 error was thrown. The input data was: {empty_email_body}')
        signup(invalid_email_body, 400, f'Email is invalid, but no 400 error was thrown. The input data was: {invalid_email_body}')

    except Exception as e:
        return {
            'status': 2,
            'message': str(e)
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