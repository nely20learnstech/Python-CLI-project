import datetime

class Grocery:
    def __init__(self, name, category, quantity, created_at=None, updated_at=None, id=None):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.created_at = created_at if created_at is not None else datetime.datetime.now()
        self.updated_at = updated_at if updated_at is not None else datetime.datetime.now()
        self.id = id if id is not None else None


class Expirable_grocery(Grocery):
    def __init__(self, name, category, quantity, product_creation_date, expiration_date,
                 created_at=None, updated_at=None, id=None):
        super().__init__(name, category, quantity, created_at, updated_at, id)
        self.product_creation_date = product_creation_date
        self.expiration_date = expiration_date


class Unexpirable_grocery(Grocery):
    def __init__(self, name, category, quantity, created_at=None, updated_at=None, id=None):
        super().__init__(name, category, quantity, created_at, updated_at, id)


class Minimal_information:
    def __init__(self, id, name, category, quantity=None):
        self.id = id
        self.name = name
        self.category = category
        self.quantity = quantity if quantity is not None else None
