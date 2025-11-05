"""API routes"""

from .auth import router as auth_router
from .clients import router as clients_router
from .modules import router as modules_router
from .configurations import router as configurations_router
from .github import router as github_router
from .environments import router as environments_router

__all__ = [
    "auth_router",
    "clients_router",
    "modules_router",
    "configurations_router",
    "github_router",
    "environments_router",
]
