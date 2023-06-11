from PharmaMarket import db_cursor, conn
from PharmaMarket.models import User, Pharmacist, Customer, Drug, Sell, DrugOrder


# INSERT QUERIES
def insert_user(user: User):
    sql = """
    INSERT INTO Users(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (user.user_name, user.full_name, user.password))
    conn.commit()


def insert_pharmacist(pharmacist: Pharmacist):
    sql = """
    INSERT INTO Pharmacists(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (pharmacist.user_name, pharmacist.full_name, pharmacist.password))
    conn.commit()


def insert_customer(customer: Customer):
    sql = """
    INSERT INTO Customers(user_name, full_name, password)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (customer.user_name, customer.full_name, customer.password))
    conn.commit()


def insert_drug(drug: Drug):
    sql = """
    INSERT INTO Drug (id,name,brand,price,city)
    VALUES (%s, %s, %s, %s, %s) RETURNING pk
    """
    db_cursor.execute(sql, (
        drug.id,
        drug.name,
        drug.brand,
        drug.price,
        drug.city
    ))
    conn.commit()
    return db_cursor.fetchone().get('pk') if db_cursor.rowcount > 0 else None


def insert_sell(sell: Sell):
    sql = """
    INSERT INTO Sell(pharmacist_pk, drug_pk)
    VALUES (%s, %s)
    """
    db_cursor.execute(sql, (sell.pharmacist_pk, sell.drug_pk,))
    conn.commit()


def insert_drug_order(order: DrugOrder):
    sql = """
    INSERT INTO DrugOrder(drug_pk, pharmacist_pk, customer_pk)
    VALUES (%s, %s, %s)
    """
    db_cursor.execute(sql, (
        order.drug_pk,
        order.pharmacist_pk,
        order.customer_pk,
    ))
    conn.commit()


# SELECT QUERIES
def get_user_by_pk(pk):
    sql = """
    SELECT * FROM Users
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user


def get_pharmacist_by_pk(pk):
    sql = """
    SELECT * FROM Pharmacists
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    pharmacist = Pharmacist(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return pharmacist


def get_drug_by_filters(name=None, brand=None, city=None,
                           pharmacist_pk=None, pharmacist_name=None, price=None):
    sql = """
    SELECT * FROM vw_drug
    WHERE
    """
    conditionals = []
    if name:
        conditionals.append(f"name='{name}'")
    if brand:
        conditionals.append(f"brand='{brand}'")
    if city:
        conditionals.append(f"city = '{city}'")
    if pharmacist_pk:
        conditionals.append(f"pharmacist_pk = '{pharmacist_pk}'")
    if pharmacist_name:
        conditionals.append(f"pharmacist_name LIKE '%{pharmacist_name}%'")
    if price:
        conditionals.append(f"price <= {price}")

    args_str = ' AND '.join(conditionals)
    order = " ORDER BY price "
    db_cursor.execute(sql + args_str + order)
    drug = [Drug(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return drug


def get_customer_by_pk(pk):
    sql = """
    SELECT * FROM Customers
    WHERE pk = %s
    """
    db_cursor.execute(sql, (pk,))
    customer = Customer(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return customer


def get_drug_by_pk(pk):
    sql = """
    SELECT drug_pk as pk, * FROM vw_drug
    WHERE drug_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    drug = Drug(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return drug


def get_all_drug_by_pharmacist(pk):
    sql = """
    SELECT * FROM vw_drug
    WHERE pharmacist_pk = %s
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql, (pk,))
    drug = [Drug(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return drug


def get_user_by_user_name(user_name):
    sql = """
    SELECT * FROM Users
    WHERE user_name = %s
    """
    db_cursor.execute(sql, (user_name,))
    user = User(db_cursor.fetchone()) if db_cursor.rowcount > 0 else None
    return user

def get_all_drug():
    sql = """
    SELECT drug_pk as pk, id,name,brand,price,city, pharmacist_name, available, pharmacist_pk
    FROM vw_drug
    ORDER BY available DESC, price
    """
    db_cursor.execute(sql)
    drug = [Drug(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return drug


def get_available_drug():
    sql = """
    SELECT * FROM vw_drug
    WHERE available = true
    ORDER BY price  
    """
    db_cursor.execute(sql)
    drug = [Drug(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return drug


def get_orders_by_customer_pk(pk):
    sql = """
    SELECT * FROM DrugOrder po
    JOIN Drug p ON p.pk = po.drug_pk
    WHERE customer_pk = %s
    """
    db_cursor.execute(sql, (pk,))
    orders = [DrugOrder(res) for res in db_cursor.fetchall()] if db_cursor.rowcount > 0 else []
    return orders


# UPDATE QUERIES
def update_sell(available, drug_pk, pharmacist_pk):
    sql = """
    UPDATE Sell
    SET available = %s
    WHERE drug_pk = %s
    AND pharmacist_pk = %s
    """
    db_cursor.execute(sql, (available, drug_pk, pharmacist_pk))
    conn.commit()
