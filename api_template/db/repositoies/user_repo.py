from typing import List
from .base_repo import BaseRepository
from api_template.db.models.user import User
from api_template.web.api.api_v1.endpoint.users.schema import CreateUserRequestSchema

class UserRepo(BaseRepository[User, CreateUserRequestSchema, CreateUserRequestSchema]):
    def __init__(self ):
        super().__init__(User)
        
