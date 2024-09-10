use real_estate;

create table if not exists real_estate(
    property_id varchar(225) primary key,
    list_price decimal(15,2),
    last_sold_price decimal(15,2),
    estimate decimal(15,2),
    list_date date,
    status varchar(225),
    city varchar(225),
    state varchar(225),
    postal_code varchar(225),
    type varchar(225),
    lot_sqft int
    );
    

insert into real_estate(
    property_id, list_price, last_sold_price, estimate, list_date, status,
    city, state, postal_code, type, lot_sqft)

values(property_id, list_price, last_sold_price, estimate, list_date, status,
    city, state, postal_code, type, lot_sqft)
on duplicate key update
    list_price = values(list_price),
    last_sold_price = values(last_sold_price),
    estimate = values(estimate),
    list_date = values(list_date),
    status = values(status),
    city = values(city),
    state = values(state),
    postal_code = values(postal_code),
    type = values(type),
    lot_sqft = values(lot_sqft);

select * from real_estate;