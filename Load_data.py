import json
import pymysql
import pandas as pd

with open('config.json') as config_file:
    config = json.load(config_file)


df = pd.read_csv('real_estate_data.csv')
mysql_config = config['mysql']

connection = pymysql.connect(
    host = mysql_config['host'],
    user = mysql_config['user'],
    password = mysql_config['password'],
    database = mysql_config['database']
)

cursor = connection.cursor()

create_table_query = ''' 
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
    ) '''

cursor.execute(create_table_query)

insert_query = '''
insert into real_estate(
    property_id, list_price, last_sold_price, estimate, list_date, status,
    city, state, postal_code, type, lot_sqft)

values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
    lot_sqft = values(lot_sqft)'''


for _,row in df.iterrows():
    cursor.execute(insert_query, tuple(row))


connection.commit()
cursor.close()
connection.close()