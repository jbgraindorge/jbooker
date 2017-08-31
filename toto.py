#!/usr/local/bin/python3-jb
from flask import Flask, render_template, request, url_for
from flask_cassandra import CassandraCluster

app = Flask(__name__)
cassandra = CassandraCluster()

app.config['CASSANDRA_NODES'] = ['127.0.0.1']  # can be a string or list of nodes

@app.route("/")
def cassandra_test():
    session = cassandra.connect()
    session.set_keyspace("keyspace1")
    cql = "SELECT * FROM books"
    r = session.execute(cql)
    print(r)
    retour = []
    for row in r:
       retour.append(str(row.id))
       print(row.id,row.title)
    ###
    print(retour)
    print(type(retour))
    #toto="tata"
    #return(str(retour))
    return render_template("rez2.html", retour=retour)

if __name__ == '__main__':
    app.run()
