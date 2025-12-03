# This file makes the routers directory a Python package
# Import your API routers here


from app.routers.auth import router as auth_router

__all__ = ["auth_router"]