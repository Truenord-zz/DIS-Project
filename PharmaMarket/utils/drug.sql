DROP TABLE IF EXISTS Drug CASCADE;

CREATE TABLE IF NOT EXISTS Drug(
    pk serial unique not null PRIMARY KEY,
	id INT,
	name VARCHAR(200),
	brand VARCHAR(200),
	price INT,
	city VARCHAR(200)
);

DELETE FROM Drug;

CREATE INDEX IF NOT EXISTS drug_index
ON Drug (id, name, brand);

DROP TABLE IF EXISTS Sell;

CREATE TABLE IF NOT EXISTS Sell(
    pharmacist_pk int not null REFERENCES Pharmacists(pk) ON DELETE CASCADE,
    drug_pk int not null REFERENCES Drug(pk) ON DELETE CASCADE,
    available boolean default true,
    PRIMARY KEY (pharmacist_pk, drug_pk)
);

CREATE INDEX IF NOT EXISTS sell_index
ON Sell (pharmacist_pk, available);

DELETE FROM Sell;

DROP TABLE IF EXISTS DrugOrder;

CREATE TABLE IF NOT EXISTS DrugOrder(
    pk serial not null PRIMARY KEY,
    customer_pk int not null REFERENCES Customers(pk) ON DELETE CASCADE,
    pharmacist_pk int not null REFERENCES Pharmacists(pk) ON DELETE CASCADE,
    drug_pk int not null REFERENCES Drug(pk) ON DELETE CASCADE,
    created_at timestamp not null default current_timestamp
);

DELETE FROM DrugOrder;

CREATE OR REPLACE VIEW vw_drug
AS
SELECT p.id, p.name, p.brand,
       p.price, p.city, s.available,
       p.pk as drug_pk,
       f.full_name as pharmacist_name,
       f.pk as pharmacist_pk
FROM Drug p
JOIN Sell s ON s.drug_pk = p.pk
JOIN pharmacists f ON s.pharmacist_pk = f.pk
ORDER BY available, p.pk;