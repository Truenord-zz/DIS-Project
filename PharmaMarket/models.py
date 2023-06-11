from typing import Dict

from flask_login import UserMixin
from psycopg2 import sql

from PharmaMarket import login_manager, db_cursor, conn, app


@login_manager.user_loader
def load_user(user_id):
    user_sql = sql.SQL("""
    SELECT * FROM Users
    WHERE pk = %s
    """).format(sql.Identifier('pk'))

    db_cursor.execute(user_sql, (int(user_id),))
    return User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None


class ModelUserMixin(dict, UserMixin):
    @property
    def id(self):
        return self.pk


class ModelMixin(dict):
    pass


class User(ModelUserMixin):
    def __init__(self, user_data: Dict):
        super(User, self).__init__(user_data)
        self.pk = user_data.get('pk')
        self.full_name = user_data.get('full_name')
        self.user_name = user_data.get('user_name')
        self.password = user_data.get('password')


class Customer(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


class Pharmacist(User):
    def __init__(self, user_data: Dict):
        super().__init__(user_data)


if __name__ == '__main__':
    user_data = dict(full_name='a', user_name='b', password='c')
    user = Pharmacist(user_data)
    print(user)

class Drug(ModelMixin):
    def __init__(self, drug_data: Dict):
        super(Drug, self).__init__(drug_data)
        self.pk = drug_data.get('pk')
        self.id = drug_data.get('id')
        self.name = drug_data.get('name')
        self.brand = drug_data.get('brand')
        self.price = drug_data.get('price')
        self.city = drug_data.get('city')
        # From JOIN w/ Sell relation
        self.available = drug_data.get('available')
        self.pharmacist_name = drug_data.get('pharmacist_name')
        self.pharmacist_pk = drug_data.get('pharmacist_pk')


class Sell(ModelMixin):
    def __init__(self, sell_data: Dict):
        super(Sell, self).__init__(sell_data)
        self.available = sell_data.get('available')
        self.pharmacist_pk = sell_data.get('pharmacist_pk')
        self.drug_pk = sell_data.get('drug_pk')


class DrugOrder(ModelMixin):
    def __init__(self, drug_order_data: Dict):
        super(DrugOrder, self).__init__(drug_order_data)
        self.pk = drug_order_data.get('pk')
        self.customer_pk = drug_order_data.get('customer_pk')
        self.pharmacist_pk = drug_order_data.get('pharmacist_pk')
        self.drug_pk = drug_order_data.get('drug_pk')
