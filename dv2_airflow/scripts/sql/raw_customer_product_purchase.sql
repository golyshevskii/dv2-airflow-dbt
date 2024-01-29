select
    purchase_key,
    customer_key,
    product_key,
    amount,
    price,
    purchase_dt
from raw.temp_raw_customer_product_purchase
where purchase_dt >= '%s'::timestamp - 1 and purchase_dt < '%s'::timestamp;