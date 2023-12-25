from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    available_permissions = {
        'all': True,
    }


class User(AbstractUserRole):
    available_permissions = {
        'change_userprofiles': True,
        'delete_userprofiles': True,
        'view_userprofiles': True,
        'add_address': True,
        'change_address': True,
        'delete_address': True,
        'view_address': True,
        'add_payment': True,
        'change_payment': True,
        'delete_payment': True,
        'view_payment': True,
    }
