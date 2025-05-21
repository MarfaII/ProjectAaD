CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    doc_id TEXT NOT NULL,
    item TEXT NOT NULL,
    category TEXT NOT NULL,
    amount INTEGER NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    discount NUMERIC(10, 2) NOT NULL,
    shop_num INTEGER NOT NULL,
    cash_num INTEGER NOT NULL,
    load_date DATE NOT NULL
);
