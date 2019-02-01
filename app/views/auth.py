# -*- coding: utf-8 -*-

from sanic import Blueprint

from sanic.response import json, text
from app.ext import auth
from app.models.user import validate_login
from sanic.request import Request
from sanic.exceptions import abort, InvalidUsage

bp = Blueprint('auth', url_prefix='auth')


@bp.route('/login', methods=['POST'])  # login = decorator(login)
async def login(request):
    data = request.data
    name = data.get('username')
    password = data.get('password')
    is_validate, user = await validate_login(name, password)
    if not is_validate:
        return json({'code': 0, 'msg': '登录失败'})

    auth.login_user(request, user)
    return json({'code': 1, 'msg': '登录成功'})


@bp.route('/logout')
@auth.login_required
async def logout(request):
    auth.logout_user(request)
    return json({'code': 1, 'msg': '注销成功'})


@bp.route('/index')
@auth.login_required
async def index(request):
    print(request.headers)
    print(request['session'])

    return json({'code': 1, 'msg': 'index成功'})
