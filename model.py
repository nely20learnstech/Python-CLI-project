import datetime

class Expirable_grocery:
    def __init__(self, name, category, quantity, product_creation_date, expiration_date,
                 created_at=None, updated_at = None, id=None):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.product_creation_date = product_creation_date
        self.expiration_date = expiration_date
        self.created_at = created_at if created_at is not None else datetime.datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.datetime.now()
        self.id = id if id is not None else None


class Unexpirable_grocery:
    def __init__(self, name, category, quantity, 
                 created_at=None, updated_at=None, id=None
                ):
        self.name = name
        self.category = category
        self.created_at = created_at if created_at is not None else datetime.datetime.now()
        # self.updated_at = datetime.datetime.now() if updated_at is not None else datetime.datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.datetime.now()
        self.quantity = quantity
        self.id = id if id is not None else None


class Minimal_information:
    def __init__(self, id, name, category, quantity=None):
        self.id = id
        self.name = name
        self.category = category
        self.quantity = quantity if quantity is not None else None