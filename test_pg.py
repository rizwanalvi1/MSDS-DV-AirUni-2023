import psycopg2
import main_configurations as conf

conn = psycopg2.connect(
    dbname=conf.dbname,
    user=conf.user,
    password=conf.password,
    host=conf.host,
    port=conf.port
)


cur = conn.cursor()

cur.execute("SELECT * FROM {}".format(conf.table_name))

rows = cur.fetchall()

for row in rows:
    print(row)
# ssh ip172-18-0-19-cg097q2e69v000de86tg@direct.labs.play-with-docker.com