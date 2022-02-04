import mongoengine

alias_core = "core"
db = "snake_bnb"


def global_init():
    mongoengine.register_connection(alias=alias_core, name=db)

