"""api_template models."""
from .user import User
import pkgutil
from pathlib import Path
from sqlalchemy.ext.declarative import declarative_base

def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="api_template.db.models.",
    )
    for module in modules:
        __import__(module.name)

