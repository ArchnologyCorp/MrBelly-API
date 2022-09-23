import psycopg2

def openConnection():
    conn = psycopg2.connect(
        host="ec2-3-223-242-224.compute-1.amazonaws.com", 
        database="dcusk4ojn43g3h",
        user="txtfgbvmfpcowk",
        password="a1696082d98712652af6daeafb7eae810e09817056ce48f37b5a39687ca6689c")
    return conn