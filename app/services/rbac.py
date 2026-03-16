def is_admin(user):
    return user.role_id == 1


def is_manager(user):
    return user.role_id == 2


def is_member(user):
    return user.role_id == 3