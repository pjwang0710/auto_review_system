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
        return r.json()
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
        response = signup(user_body, 200, f'SignUp Failed, input: {user_body}')

        if 'data' in response.keys():
            if 'access_token' not in response['data'].keys():
                raise ValueError(f"Incorrect response, the returned value does not include an access_token. response: {response['data']}")
            if 'user' not in response['data'].keys():
                raise ValueError(f"Incorrect response, the returned value does not include an user. response: {response['data']}")
            else:
                keys = ['id', 'provider', 'name', 'email', 'picture']
                for key in keys:
                    if key not in response['data']['user'].keys():
                        raise ValueError(f"Incorrect response, the returned value does not include an user.{key}. response: {response['data']}")
                if response['data']['user']['provider'] != 'native':
                    raise ValueError(f"Incorrect response, user.provider != native. response: {response['data']}")
                if response['data']['user']['name'] != user_body.get('name'):
                    raise ValueError(f"Incorrect response, user.name != {user_body.get('name')}. response: {response['data']}")
                if response['data']['user']['email'] != user_body.get('email'):
                    raise ValueError(f"Incorrect response, user.email != {user_body.get('email')}. response: {response['data']}")

        signup(user_body, 403, f'After inputting the same data twice, there was no 403 error thrown. The input data was: {user_body}')
        signup(wo_password_body, 400, f'Password field was not entered, but no 400 error was thrown. The input data was: {wo_password_body}')
        signup(wo_name_body, 400, f'Name field was not entered, but no 400 error was thrown. The input data was: {wo_name_body}')
        signup(wo_email_body, 400, f'Email field was not entered, but no 400 error was thrown. The input data was: {wo_email_body}')
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


async def validatePart4(server):

    def signup(body, status_code, err_msg):
        api = f'{server}/api/1.0/users/signup'
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(api, json=body, headers=headers)
        if r.status_code != status_code:
            raise ValueError(err_msg)
        return r.json()

    def signin(body, status_code, err_msg):
        api = f'{server}/api/1.0/users/signin'
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(api, json=body, headers=headers)
        if r.status_code != status_code:
            raise ValueError(err_msg)
        return r.json()

    name = random_string(8)
    user_body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    user_signin_body = {
        "provider": "native",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    wrong_provider_body = {
        "provider": "google",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    wrong_email_body = {
        "provider": "native",
        "email": f"user-{name}-fake@test.com",
        "password": "test"
    }
    wrong_password_body = {
        "provider": "native",
        "email": f"user-{name}@test.com",
        "password": "test123456"
    }
    wo_provider_body = {
        "email": f"user-{name}@test.com",
        "password": "test123456"
    }
    wo_email_body = {
        "provider": "native",
        "password": "test123456"
    }
    wo_password_body = {
        "provider": "native",
        "email": f"user-{name}@test.com"
    }
    try:
        signup(user_body, 200, f'SignUp Failed, input: {user_body}')
        response = signin(user_signin_body, 200, f'SignIn Failed, input: {user_signin_body}')
        if 'data' in response.keys():
            if 'access_token' not in response['data'].keys():
                raise ValueError(f"Incorrect response, the returned value does not include an access_token. response: {response['data']}")
            if 'user' not in response['data'].keys():
                raise ValueError(f"Incorrect response, the returned value does not include an user. response: {response['data']}")
            else:
                keys = ['id', 'provider', 'name', 'email', 'picture']
                for key in keys:
                    if key not in response['data']['user'].keys():
                        raise ValueError(f"Incorrect response, the returned value does not include an user.{key}. response: {response['data']}")
                if response['data']['user']['provider'] != 'native':
                    raise ValueError(f"Incorrect response, user.provider != native. response: {response['data']}")
                if response['data']['user']['name'] != user_signin_body.get('name'):
                    raise ValueError(f"Incorrect response, user.name != {user_signin_body.get('name')}. response: {response['data']}")
                if response['data']['user']['email'] != user_signin_body.get('email'):
                    raise ValueError(f"Incorrect response, user.email != {user_signin_body.get('email')}. response: {response['data']}")

        signin(wrong_provider_body, 403, f'Wrong provider, but did not respond with a 403 error, input: {wrong_provider_body}')
        signin(wrong_email_body, 403, f'Wrong email, but did not respond with a 403 error, input: {wrong_email_body}')
        signin(wrong_password_body, 403, f'Wrong password, but did not respond with a 403 error, input: {wrong_password_body}')
        signin(wo_provider_body, 403, f'No provider provided, but did not respond with a 403 error, input: {wo_provider_body}')
        signin(wo_email_body, 403, f'No email provided, but did not respond with a 403 error, input: {wo_email_body}')
        signin(wo_password_body, 403, f'No password provided, but did not respond with a 403 error, input: {wo_password_body}')        
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
    validatePart3,
    validatePart4
]