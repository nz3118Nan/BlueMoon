#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: security.py
Author: Zhan Nan
Date: 2025-03-03
Description: Security module for the application
"""
################################################################################
# system settings
import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
os.chdir(root_dir)
sys.path.append(root_dir)

# built-in modules
from datetime import datetime, timedelta, timezone
from typing import Union, Optional, Dict
from jose import JWTError, jwt
from passlib.context import CryptContext

# developed modules
from app.core.config import Config
from app.core.logging_setting import logger

################################################################################
# Authentication service
class AuthService:
    '''
    Authentication service for the application
    '''
    def __init__(self, secret_key: str = Config['user_management_security']['SECRET_KEY'], 
                 algorithm: str = Config['user_management_security']['ALGORITHM'], 
                 access_token_expire_minutes: int = Config['user_management_security']['ACCESS_TOKEN_EXPIRE_MINUTES']):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
        # TODO: replace with database connection 
        self.fake_users_db = {
            "johndoe": {
                "id": 89134519234,
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password_hash": self.get_password_hash("1123123"),
                "is_active": True,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            }
        }

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        if not self.pwd_context.verify(plain_password, hashed_password):
            return False
        elif self.pwd_context.verify(plain_password, hashed_password):
            return True

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def get_user(self, username: str) -> Optional[User]:
        # TODO: replace with database connection 
        user_dict = self.fake_users_db.get(username)
        if user_dict:
            return User(**user_dict)
        return None

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.get_user(username)
        if not user or not self.verify_password(password, user.password_hash):
            return None
        return user

    def create_access_token(self, data: Dict[str, str], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

################################################################################
# main
if __name__ == "__main__":
    auth_service = AuthService()

    # TRUE CASE
    # Authenticate user
    user = auth_service.authenticate_user("johndoe", "1123123")
    if user:
        print(f"User {user.username} authenticated successfully.")
        # Create access token
        access_token = auth_service.create_access_token(data={"uid": user.id,
                                                              "email": user.email,
                                                              "is_active": user.is_active,
                                                              })
        print(f"Access token: {access_token}")
    else:
        print("Invalid username or password.")
        
    # Decode access token
    decoded_token = auth_service.decode_access_token(access_token)
    print(f"Decoded token: {decoded_token}")

    # FALSE CASE
    # Authenticate user
    user = auth_service.authenticate_user("johndoe", "asdf")
    if user:
        print(f"User {user.username} authenticated successfully.")
    else:
        print("Invalid username or password.")
    