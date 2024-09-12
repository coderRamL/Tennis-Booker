import psycopg2
from flask import Flask, render_template, request
from sqlalchemy import create_engine, select, text, Integer, String, Column, Table, MetaData
app = Flask(__name__)

@app.route('/us_open', methods = ['GET', 'POST'])
def us_open():
    engine = create_engine("postgresql://laxminarayansubramanian:9Krishna@127.0.0.1:5001/postgres")
    metadata = MetaData()
    match = Table('match', metadata, Column('eventid', Integer, primary_key=True), Column('player_1', String), Column('player_2', String), Column('date', String), Column('time', String), Column('time_of_day', String), Column('stadium', String))
    conn = engine.connect()
    query = select(match)
    exe = conn.execute(query)
    res = exe.fetchall()
    length = len(res)
    i  = 0
    return render_template('data.html', data = res, len = length, i = i)

@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    try:
        conn = psycopg2.connect(host="127.0.0.1",
                                dbname="postgres", 
                                user="laxminarayansubramanian", 
                                password="9Krishna",
                                port=5001)
        conn.autocommit = True
        cur = conn.cursor()
        print("Connected Successfully")
        cur.execute("PREPARE orderplan AS SELECT * FROM match ORDER BY eventid")
        cur.execute("EXECUTE orderplan")
        res = cur.fetchall()
        length = len(res)
        num = str(request.args['id'])
        one = str(request.args['one'])
        two = str(request.args['two'])
        date = str(request.args['date'])
        time = str(request.args['time'])
        ttd = str(request.args['ttd'])
        sta = str(request.args['stadium'])
        query = """PREPARE plan AS SELECT * FROM bookings WHERE eventid = $1"""
        cur.execute(query)
        cur.execute("EXECUTE plan (%s)", (num,))
        result = cur.fetchall()
        l = len(result)
        sql = """PREPARE insplan AS INSERT INTO bookings VALUES ($1, $2, $3, $4, $5, $6, $7, $8)"""
        cur.execute(sql)
        cur.execute("EXECUTE insplan (%s, %s, %s, %s, %s, %s, %s, %s)", (num, one, two, date, time, ttd, sta, '1',))
        print("Insert Success")
        cur.execute("PREPARE bookplan AS SELECT * FROM bookings ORDER BY eventid")
        cur.execute("EXECUTE bookplan")
        res = cur.fetchall()
        length = len(res)
        i  = 0 

    except (Exception, psycopg2.Error) as error:
        if conn:
            print("Failed to insert", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
    if l > 0:
        return render_template('added.html')
    else:
        return render_template('cart.html', data = res, len = length, i = i)

@app.route('/carts', methods = ['GET', 'POST'])
def carts():
    try:
        conn = psycopg2.connect(host="127.0.0.1",
                                dbname="postgres", 
                                user="laxminarayansubramanian", 
                                password="9Krishna",
                                port=5001)
        conn.autocommit = True
        cur = conn.cursor()
        print("Connected Successfully")
        num = str(request.args['eid'])
        sql = """PREPARE delplan AS DELETE FROM bookings WHERE eventid = $1"""
        cur.execute(sql)
        cur.execute("EXECUTE delplan (%s)", (num,))
        cur.execute("PREPARE plan AS SELECT * FROM bookings ORDER BY eventid")
        cur.execute("EXECUTE plan")
        res = cur.fetchall()
        length = len(res)
        i  = 0 
    except (Exception, psycopg2.Error) as error:
        if conn:
            print("Failed to insert", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

    if length == 0:
        return render_template('empty.html')
    else:
        return render_template('carts.html', data = res, len = length, i = i)

@app.route('/booked', methods = ['GET', 'POST'])
def booked():
    return render_template('booked.html')

@app.route('/carte', methods = ['GET', 'POST'])
def carte():
    engine = create_engine("postgresql://laxminarayansubramanian:9Krishna@127.0.0.1:5001/postgres")
    metadata = MetaData()
    match = Table('bookings', metadata, Column('eventid', Integer, primary_key=True), Column('player_1', String), Column('player_2', String), Column('date', String), Column('time', String), Column('time_of_day', String), Column('stadium', String), Column('num_tickets', Integer))
    conn = engine.connect()
    query = select(match).order_by(text('eventid'))
    exe = conn.execute(query)
    res = exe.fetchall()
    length = len(res)
    i  = 0
    return render_template('carts.html', data = res, len = length, i = i)

@app.route('/cartes', methods = ['GET', 'POST'])
def cartes():
    engine = create_engine("postgresql://laxminarayansubramanian:9Krishna@127.0.0.1:5001/postgres")
    metadata = MetaData()
    match = Table('bookings', metadata, Column('eventid', Integer, primary_key=True), Column('player_1', String), Column('player_2', String), Column('date', String), Column('time', String), Column('time_of_day', String), Column('stadium', String), Column('num_tickets', Integer))
    conn = engine.connect()
    query = select(match).order_by(text('eventid'))
    exe = conn.execute(query)
    res = exe.fetchall()
    length = len(res)
    i  = 0
    if length == 0:
        return render_template('empty.html')
    else:
        return render_template('carts.html', data = res, len = length, i = i)

@app.route('/date', methods = ['GET', 'POST'])
def date():
    try:
        conn = psycopg2.connect(host="127.0.0.1",
                                dbname="postgres", 
                                user="laxminarayansubramanian", 
                                password="9Krishna",
                                port=5001)
        conn.autocommit = True
        cur = conn.cursor()
        print("Connected Successfully")
        cur.execute("PREPARE plan AS SELECT * FROM match ORDER BY date, time_of_day, string_to_array(time, ':')::int[]")
        cur.execute("EXECUTE plan")
        res = cur.fetchall()
        length = len(res)
        i  = 0
    except (Exception, psycopg2.Error) as error:
        if conn:
            print("Failed to insert", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

    return render_template('data.html', data = res, len = length, i = i)

@app.route('/stadium', methods = ['GET', 'POST'])
def stadium():
    try:
        conn = psycopg2.connect(host="127.0.0.1",
                                dbname="postgres", 
                                user="laxminarayansubramanian", 
                                password="9Krishna",
                                port=5001)
        conn.autocommit = True
        cur = conn.cursor()
        print("Connected Successfully")
        cur.execute("PREPARE plan AS SELECT * FROM match ORDER BY stadium, date, time_of_day, string_to_array(time, ':')::int[]")
        cur.execute("EXECUTE plan")
        res = cur.fetchall()
        length = len(res)
        i  = 0
    except (Exception, psycopg2.Error) as error:
        if conn:
            print("Failed to insert", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

    return render_template('data.html', data = res, len = length, i = i)

@app.route('/player', methods = ['GET','POST'])
def player():
    engine = create_engine("postgresql://laxminarayansubramanian:9Krishna@127.0.0.1:5001/postgres")
    metadata = MetaData()
    match = Table('match', metadata, Column('eventid', Integer, primary_key=True), Column('player_1', String), Column('player_2', String), Column('date', String), Column('time', String), Column('time_of_day', String), Column('stadium', String))
    conn = engine.connect()
    query = select(match).order_by(text('player_1, player_2'))
    exe = conn.execute(query)
    res = exe.fetchall()
    length = len(res)
    i  = 0
    return render_template('data.html', data = res, len = length, i = i)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    try:
        conn = psycopg2.connect(host="127.0.0.1",
                                dbname="postgres", 
                                user="laxminarayansubramanian", 
                                password="9Krishna",
                                port=5001)
        conn.autocommit = True
        cur = conn.cursor()
        print("Connected Successfully")
        search = str(request.form['search'])
        query = """PREPARE searchplan AS SELECT * FROM match WHERE player_1 = $1 or player_2 = $2 or date = $3 or time = $4 or time_of_day = $5 or stadium = $6"""
        cur.execute(query)
        cur.execute("EXECUTE searchplan (%s, %s, %s, %s, %s, %s)", (search, search, search, search, search, search,))
        res = cur.fetchall()
        length = len(res)
        i  = 0
    except (Exception, psycopg2.Error) as error:
        if conn:
            print("Failed to insert", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

    if length == 0:
        return render_template('blank.html')
    
    return render_template('data.html', data = res, len = length, i = i)

@app.route('/update', methods = ['GET', 'POST'])
def update():
    try:
        conn = psycopg2.connect(host="127.0.0.1",
                                dbname="postgres", 
                                user="laxminarayansubramanian", 
                                password="9Krishna",
                                port=5001)
        conn.autocommit = True
        cur = conn.cursor()
        print("Connected Successfully")
        num = str(request.args['num'])
        id = str(request.args['id'])
        query = """PREPARE updplan AS UPDATE bookings SET num_tickets = $1 WHERE eventid = $2"""
        cur.execute(query)
        cur.execute("EXECUTE updplan (%s, %s)", (num, id,))
        cur.execute("PREPARE plan AS SELECT * FROM bookings ORDER BY eventid")
        cur.execute("EXECUTE plan")
        res = cur.fetchall()
        length = len(res)
        i  = 0
    except (Exception, psycopg2.Error) as error:
        if conn:
            print("Failed to insert", error)

    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

    return render_template('cart.html', data = res, len = length, i = i)

app.run()