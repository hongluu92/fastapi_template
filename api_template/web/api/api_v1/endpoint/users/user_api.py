from typing import List

from api_template.errors.http_res_err import HttpResException
from .schema import *
from fastapi import APIRouter, Depends, Query
from api_template.db.repositoies.user_repo import UserRepo

router = APIRouter()


@router.get("",response_model=List[GetUserListResponseSchema],)
async def get_user_list(limit: int = 100,offset: int = 0,):
    return await UserRepo().get_multi(offset = offset, limit=limit)

@router.get("/{id}", response_model=GetUserListResponseSchema,)
async def get_user_by_id(id: int):
    return await UserRepo().get_by_id(id)

@router.post("",response_model=GetUserListResponseSchema,)
async def create_user(request: CreateUserRequestSchema):
    return await UserRepo().create(request)

@router.put("/{id}",response_model=GetUserListResponseSchema,)
async def create_user(id: int, request: CreateUserRequestSchema):
    user = await UserRepo().get_by_id(id)
    if not user:
        raise HttpResException(code= "100", message="User not exits")
    return await UserRepo().update(obj_current=user, obj_new= request)
