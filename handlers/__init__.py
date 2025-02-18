from .user import start, register, role, help
from .admin import statistics,ban


def register_handlers(dp):
    start.register_handlers(dp)
    help.register_handlers(dp)
    register.register_handlers(dp)
    role.register_handlers(dp)
    statistics.register_handlers(dp)
    ban.register_handlers(dp)