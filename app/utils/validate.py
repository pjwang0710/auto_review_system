import requests
from app.utils.utils import random_string

SUCCESS_MESSAGE = "Congrats! You just passed the basic validation." 


def check_signin_valid(response, user_body):
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
    return {
        'name': response['data']['user']['name'],
        'user_id': response['data']['user']['id'],
        'token': response['data']['access_token']
    }


def signup(server, body, status_code, err_msg):
    api = f'{server}/api/1.0/users/signup'
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.post(api, json=body, headers=headers)
    if r.status_code == 404:
        raise ValueError(f'POST {api} not found')
    if r.status_code != status_code:
        raise ValueError(err_msg)
    return r.json()


def signin(server, body, status_code, err_msg):
    api = f'{server}/api/1.0/users/signin'
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.post(api, json=body, headers=headers)
    if r.status_code == 404:
        raise ValueError(f'POST {api} not found')
    if r.status_code != status_code:
        raise ValueError(err_msg)
    return r.json()


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
        response = signup(server, user_body, 200, f'SignUp Failed, input: {user_body}')
        check_signin_valid(response, user_body)
        signup(server, user_body, 403, f'After inputting the same data twice, there was no 403 error thrown. The input data was: {user_body}')
        signup(server, wo_password_body, 400, f'Password field was not entered, but no 400 error was thrown. The input data was: {wo_password_body}')
        signup(server, wo_name_body, 400, f'Name field was not entered, but no 400 error was thrown. The input data was: {wo_name_body}')
        signup(server, wo_email_body, 400, f'Email field was not entered, but no 400 error was thrown. The input data was: {wo_email_body}')
        signup(server, empty_password_body, 400, f'Password is empty, but no 400 error was thrown. The input data was: {empty_password_body}')
        signup(server, empty_name_body, 400, f'Name is empty, but no 400 error was thrown. The input data was: {empty_name_body}')
        signup(server, empty_email_body, 400, f'Email is empty, but no 400 error was thrown. The input data was: {empty_email_body}')
        signup(server, invalid_email_body, 400, f'Email is invalid, but no 400 error was thrown. The input data was: {invalid_email_body}')

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
        signup(server, user_body, 200, f'SignUp Failed, input: {user_body}')
        response = signin(server, user_signin_body, 200, f'SignIn Failed, input: {user_signin_body}')
        check_signin_valid(response, user_body)
        signin(server, wrong_provider_body, 403, f'Wrong provider, but did not respond with a 403 error, input: {wrong_provider_body}')
        signin(server, wrong_email_body, 403, f'Wrong email, but did not respond with a 403 error, input: {wrong_email_body}')
        signin(server, wrong_password_body, 403, f'Wrong password, but did not respond with a 403 error, input: {wrong_password_body}')
        signin(server, wo_provider_body, 400, f'No provider provided, but did not respond with a 400 error, input: {wo_provider_body}')
        signin(server, wo_email_body, 400, f'No email provided, but did not respond with a 400 error, input: {wo_email_body}')
        signin(server, wo_password_body, 400, f'No password provided, but did not respond with a 400 error, input: {wo_password_body}')        
    except Exception as e:
        return {
            'status': 2,
            'message': str(e)
        }
    return {
        'status': 1,
        'message': SUCCESS_MESSAGE
    }


async def validatePart5(server):
    def get_profile(user_id, token, status_code, err_msg):
        api = f'{server}/api/1.0/users/{user_id}/profile'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        r = requests.get(api, headers=headers)
        if r.status_code == 404:
            raise ValueError(f'GET {api} not found')
        if r.status_code != status_code:
            raise ValueError(err_msg)
        return r.json()

    def update_profile(body, token, status_code, err_msg):
        api = f'{server}/api/1.0/users/profile'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        r = requests.put(api, json=body, headers=headers)
        if r.status_code == 404:
            raise ValueError(f'PUT {api} not found')
        if r.status_code != status_code:
            raise ValueError(err_msg)
        return r.json()

    def update_picture(token, status_code, err_msg):
        api = f'{server}/api/1.0/users/picture'
        files = [
            ('picture', ('profile.png', open('app/utils/profile.png', 'rb'), 'image/png'))
        ]
        headers = {
            'Authorization': f'Bearer {token}'
        }
        r = requests.put(api, files=files, headers=headers)
        print(r.status_code, r.content)
        if r.status_code == 404:
            raise ValueError(f'PUT {api} not found')
        if r.status_code != status_code:
            raise ValueError(err_msg)
        return r.json()

    def get_profile_wo_headers(user_id, status_code, err_msg):
        api = f'{server}/api/1.0/users/{user_id}/profile'
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.get(api, headers=headers)
        if r.status_code == 404:
            raise ValueError(f'GET {api} not found')
        if r.status_code != status_code:
            raise ValueError(err_msg)
        return r.json()

    def update_profile_wo_token(body, status_code, err_msg):
        api = f'{server}/api/1.0/users/profile'
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.put(api, json=body, headers=headers)
        if r.status_code == 404:
            raise ValueError(f'PUT {api} not found')
        if r.status_code != status_code:
            raise ValueError(err_msg)
        return r.json()

    name = random_string(8)
    user1_body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    user1_signin_body = {
        "provider": "native",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    name = random_string(8)
    user2_body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com",
        "password": "test"
    }

    try:
        signup(server, user1_body, 200, f'SignUp Failed, input: {user1_body}')
        signup(server, user2_body, 200, f'SignUp Failed, input: {user2_body}')
        response = signin(server, user1_signin_body, 200, f'SignIn Failed, input: {user1_signin_body}')
        data1 = check_signin_valid(response, user1_body)
        data2 = check_signin_valid(response, user2_body)
        res = get_profile(data1.get('user_id'), data1.get('token'), 200, f"Get profile error, user_id: {data1.get('user_id')}, jwt: {data1.get('token')}")
        if res['data']['user']['id'] != data1.get('user_id'):
            raise ValueError(f"{res['data']['user']['id']} != {data1.get('user_id')}, input: {data1.get('user_id')}")
        if res['data']['user']['name'] != data1.get('name'):
            raise ValueError(f"{res['data']['user']['name']} != {data1.get('name')}, input: {data1.get('user_id')}")
        res = get_profile(data2.get('user_id'), data1.get('token'), 200, f"Get profile error, user_id: {data2.get('user_id')}, jwt: {data1.get('token')}")
        if res['data']['user']['id'] != data2.get('user_id'):
            raise ValueError(f"{res['data']['user']['id']} != {data2.get('user_id')}, input: {data2.get('user_id')}")
        if res['data']['user']['name'] != data2.get('name'):
            raise ValueError(f"{res['data']['user']['name']} != {data2.get('name')}, input: {data2.get('user_id')}")
        get_profile_wo_headers(data2.get('user_id'), 401, "No token provided, but did not respond with a 401 error.")
        get_profile(data2.get('user_id'), '123', 403, "Wrong token provided, but did not respond with a 403 error.")

        body = {
            "name": f'user-{random_string(8)}',
            "introduction": random_string(64),
            "tags": f'{random_string(6)},{random_string(6)},{random_string(6)}'
        }
        res = update_profile(body, data1.get('token'), 200, f"Update profile failed, input: {body}, jwt: {data1.get('token')}")
        if (res.get('data', {}).get('user', {}).get('id') != data1.get('user_id')):
            raise ValueError(f"Update Profile Response is wrong, {res.get('data', {}).get('user', {}).get('id')} != {data1.get('user_id')}, input: jwt: {data1.get('token')}")
        profile = get_profile(data1.get('user_id'), data1.get('token'), 200, f"Get profile error, user_id: {data1.get('user_id')}, jwt: {data1.get('token')}")
        if profile.get('data', {}).get('user', {}).get('name') != body.get('name'):
            raise ValueError(f"Update Profile failed, {profile.get('data', {}).get('user', {}).get('name') } != {body.get('name')}, input: jwt: {data1.get('token')}")
        if profile.get('data', {}).get('user', {}).get('introduction') != body.get('introduction'):
            raise ValueError(f"Update Profile failed, {profile.get('data', {}).get('user', {}).get('introduction') } != {body.get('introduction')}, input: jwt: {data1.get('token')}")
        if profile.get('data', {}).get('user', {}).get('tags') != body.get('tags'):
            raise ValueError(f"Update Profile failed, {profile.get('data', {}).get('user', {}).get('tags') } != {body.get('tags')}, input: jwt: {data1.get('token')}")
        update_profile_wo_token(body, 401, "No token provided, but did not respond with a 401 error.")
        update_profile(body, '123', 403, "Wrong token provided, but did not respond with a 403 error.")
        update_picture(data1.get('token'), 200, 'Picture upload failed, image here: https://www.flaticon.com/free-icon/profile_3135715?term=user&page=1&position=7&origin=search&related_id=3135715')
        profile = get_profile(data1.get('user_id'), data1.get('token'), 200, f"Get profile error, user_id: {data1.get('user_id')}, jwt: {data1.get('token')}")
        if profile.get('data', {}).get('user', {}).get('picture') == '':
            raise ValueError("Update Picture failed")

    except Exception as e:
        return {
            'status': 2,
            'message': str(e)
        }
    return {
        'status': 1,
        'message': SUCCESS_MESSAGE
    }


async def validatePart6(server):
    def send_friend_request(user_id, token, status_code, err_msg):
        api = f'{server}/api/1.0/friends/{user_id}/request'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        r = requests.post(api, headers=headers)
        if r.status_code == 404:
            raise ValueError(f'POST {api} not found')
        if r.status_code != status_code:
            raise ValueError(err_msg)
        return r.json()        
    
    def send_friend_request_agree(friendship_id, token, status_code, err_msg):
        api = f'{server}/api/1.0/friends/{friendship_id}/agree'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        r = requests.post(api, headers=headers)
        if r.status_code == 404:
            raise ValueError(f'POST {api} not found')
        if r.status_code != status_code:
            raise ValueError(err_msg)
        return r.json()        

    name = random_string(8)
    user1_body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    user1_signin_body = {
        "provider": "native",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    name = random_string(8)
    user2_body = {
        "name": f"user-{name}",
        "email": f"user-{name}@test.com",
        "password": "test"
    }
    try:
        signup(server, user1_body, 200, f'SignUp Failed, input: {user1_body}')
        signup(server, user2_body, 200, f'SignUp Failed, input: {user2_body}')
        response = signin(server, user1_signin_body, 200, f'SignIn Failed, input: {user1_signin_body}')
        data1 = check_signin_valid(response, user1_body)
        data2 = check_signin_valid(response, user2_body)
        response = send_friend_request(data2.get('user_id'), data1.get('token'), 200, f"Send Friend Request Error, user_id: {data2.get('user_id')}, jwt: {data1.get('token')}")
        friendship_id = response.get('data', {}).get('friendship', {}).get('id')
        send_friend_request_agree(friendship_id, data1.get('user_id'), 400, f"user_id: {data1.get('user_id')} cannot agree this friend request")
        send_friend_request_agree(friendship_id, data2.get('user_id'), 200, f"user_id: {data2.get('user_id')} cannot agree this friend request")
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
    validatePart4,
    validatePart5,
    validatePart6
]
