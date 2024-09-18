import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'b1f3d5e9c828d1c05d709b9de1425f3ff2f9e6c516b4a05f1ecbaad7d9058d7e'
    JWT_SECRET_KEY = os.environ.get(
        'JWT_SECRET_KEY') or '9d21e7e7c65d4f1a2bc72a6053c6e5df2f539af47e9dfac17a3b6a5198d34247'
