from .user import start, register, role, help,cat_view,volontier,filter,help_money,quiz
from .admin import statistics,ban,news,cats_reg,cat_change,del_cat,applications


def register_handlers(dp):
    start.register_handlers(dp)
    help.register_handlers(dp)
    register.register_handlers(dp)
    role.register_handlers(dp)
    statistics.register_handlers(dp)
    ban.register_handlers(dp)
    news.register_handlers(dp)
    cats_reg.register_handlers(dp)
    cat_change.register_handlers(dp)
    del_cat.register_handlers(dp)
    cat_view.register_handlers(dp)
    applications.register_handlers(dp)
    volontier.register_handlers(dp)
    filter.register_handlers(dp)
    help_money.register_handlers(dp)
    quiz.register_handlers(dp)
