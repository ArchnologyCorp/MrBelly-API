import psycopg2

def openConnection():
    conn = psycopg2.connect(
        host="bbio43cxsc7culcqqqnp-postgresql.services.clever-cloud.com", 
        database="bbio43cxsc7culcqqqnp",
        user="ugfhyj2ph23mx4h4rohn",
        password="J7685ISIeik3iWJTkEJOxqK1wqVdqK")
    return conn