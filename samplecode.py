import pandas as pd
import numpy as np
import psycopg2

def read_file():
    file = open('sample_file.txt', 'r')

    data = file.readlines()
    road_id = []
    direction = []
    lines = []
    modified_data = []

    for line in data:
        modified_data.append(line.strip())

    new = []
    for entry in modified_data:
        new.append(entry.split(' '))

    for i in new:
        road_id.append(i[0])
        if len(i)==1:
            direction.append('')
            lines.append('')
        if len(i) >= 2:
            direction.append(i[1])
        if len(i)>=3:
            lines.append(i[2:])

    for j in lines:
        if type(j) == list:
            for k in range(len(j)):
                j[k] = j[k].strip(',')

    Polyline = []
    for values in lines:
        polyline = [tuple(map(float, pair.split(':'))) for pair in values]
        Polyline.append(polyline)

    return road_id, direction, Polyline

def db_connection(host, user, password, database):
    db_params= {'host':host,
                'user':user,
                'password':password,
                'database':database}
    try:
        conn = psycopg2.connect(**db_params)
    except psycopg2.Error as e:
            print("Error connecting to PostgreSQL:", e)

    else:
        print('Database Connected!!')
        cursor = conn.cursor()
        cursor.execute(""" DROP TABLE IF EXISTS road_links; """)
        cursor.execute(""" CREATE TABLE IF NOT EXISTS road_links(
                    Road_ID BIGINT,
                    Direction FLOAT,
                    Polyline VARCHAR);
        """)

        df = pd.DataFrame()
        road_id, direction, Polyline = read_file()
        df['Road_ID'] = road_id
        df['Direction'] = direction
        df['Polyline'] = Polyline

        df.replace('', np.nan, inplace=True)
        df['Road_ID'].astype('int')
        df['Direction'].astype('float')

        for i, row in df.iterrows():
            a = (row['Road_ID'], row['Direction'], row['Polyline'])
            a = tuple(a)
            cursor.execute('INSERT INTO road_links (Road_ID, Direction, Polyline) VALUES (%s, %s, %s)', a)

        conn.commit()
        cursor.execute('select * from road_links where direction = 2')
        result = cursor.fetchall()
        for res in result:
            print(res)
        return result

db_connection(host = 'localhost',
              user = 'postgres',
              password = 'postgres',
              database = 'lokeshrakurthi')