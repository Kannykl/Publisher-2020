import base64


def check_user(request):
    jwt = request.COOKIES['user_jwt']
    info_part = jwt.split('.')[1].encode('ascii')
    decoded_jwt = eval(base64.b64decode(info_part).decode('ascii'))
    username = decoded_jwt['username']
    group = decoded_jwt['group']
    return [username, group]
