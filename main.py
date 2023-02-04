from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from hashlib import sha256


from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'app'
app.config['MYSQL_PASSWORD'] ='1234'
app.config['MYSQL_DB'] = "primjer"
mysql = MySQL(app)



app.secret_key = '_5#y2L"F4Q8z\n\xec]/'


@app.route('/', methods=['GET'])
def pocetna():

    #print (session['id_uloge'])
    if 'ime' in session:
        if session['id_uloge']==0:
            query = f"SELECT  id,ime, prezime FROM veslaci WHERE id_uloge=1"
            cursor = mysql.connection.cursor()
            cursor.execute(query)
            korisnici = cursor.fetchall()






            return render_template('index.html',korisnici=korisnici)
        elif session['id_uloge']==1:
            return redirect(url_for('rezultati'))
    return redirect(url_for('login')),303



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = sha256(request.form.get('password').encode()).hexdigest()

        query =f"SELECT ime, id_uloge,id,prezime FROM veslaci WHERE HEX(password)='{password}' AND email='{email}'"
        cursor= mysql.connection.cursor()
        cursor.execute(query)
        korisnik=cursor.fetchall()

        if korisnik:
            session['ime'] = korisnik[0][0]
            session['id_uloge'] = korisnik[0][1]
            session['id'] = korisnik[0][2]
            session['prezime']=korisnik[0][3]
            return redirect(url_for('pocetna')), 303

        else:
            return render_template('login.html', error='Uneseni su krivi korisnički podaci')



@app.route('/index_veslac', methods=['GET'], )
def rezultati():

        id = session['id']
        ime = session['ime']
        prezime = session['prezime']
        if  session['id_uloge']==0:
            id= request.args.get('id')
            ime = session['ime']
            prezime = session['prezime']





        print(session['id'])
        query = f"SELECT datum_vrijeme_upisa, vrijednost FROM sile WHERE veslac={id} ORDER BY datum_vrijeme_upisa  DESC"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        sile = cursor.fetchall()

        query = f"SELECT ime,prezime FROM veslaci WHERE id={id}"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        veslaci = cursor.fetchall()
        podaci=[
            {
                'ime':veslaci[0][0],
                'prezime':veslaci[0][1]
            }
        ]

        data_zadnji = [

            {
                'vrijeme': f'{sile[0][0]}',
                'vrijednost': f'{sile[0][1]}'
            },
            {
                'vrijeme': f'{sile[1][0]}',
                'vrijednost': f'{sile[1][1]}',
            },
            {
                'vrijeme': f'{sile[2][0]}',
                'vrijednost': f'{sile[2][1]}',
            },
            {
                'vrijeme': f'{sile[3][0]}',
                'vrijednost': f'{sile[3][1]}',
            },
            {
                'vrijeme': f'{sile[4][0]}',
                'vrijednost': f'{sile[4][1]}',
            },
            {
                'vrijeme': f'{sile[5][0]}',
                'vrijednost': f'{sile[5][1]}',
            },
            {
                'vrijeme': f'{sile[6][0]}',
                'vrijednost': f'{sile[6][1]}',
            },
            {
                'vrijeme': f'{sile[7][0]}',
                'vrijednost': f'{sile[7][1]}',
            },
            {
                'vrijeme': f'{sile[8][0]}',
                'vrijednost': f'{sile[8][1]}',
            },
            {
                'vrijeme': f'{sile[9][0]}',
                'vrijednost': f'{sile[9][1]}',
            }
        ]
        query = f"SELECT datum_vrijeme_upisa, vrijednost FROM sile WHERE veslac=1 ORDER BY vrijednost  DESC"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        sile = cursor.fetchall()
        data_top = [
            {
                'vrijeme': f'{sile[0][0]}',
                'vrijednost': f'{sile[0][1]}',
            },
            {
                'vrijeme': f'{sile[1][0]}',
                'vrijednost': f'{sile[1][1]}',
            },
            {
                'vrijeme': f'{sile[2][0]}',
                'vrijednost': f'{sile[2][1]}',
            },
            {
                'vrijeme': f'{sile[3][0]}',
                'vrijednost': f'{sile[3][1]}',
            },
            {
                'vrijeme': f'{sile[4][0]}',
                'vrijednost': f'{sile[4][1]}',
            },
            {
                'vrijeme': f'{sile[5][0]}',
                'vrijednost': f'{sile[5][1]}',
            },
            {
                'vrijeme': f'{sile[6][0]}',
                'vrijednost': f'{sile[6][1]}',
            },
            {
                'vrijeme': f'{sile[7][0]}',
                'vrijednost': f'{sile[7][1]}',
            },
            {
                'vrijeme': f'{sile[8][0]}',
                'vrijednost': f'{sile[8][1]}',
            },
            {
                'vrijeme': f'{sile[9][0]}',
                'vrijednost': f'{sile[9][1]}',
            }
        ]
        return render_template('index_veslac.html', data_zadnji=data_zadnji, data_top=data_top,podaci=podaci), 303

@app.route('/sila', methods=[ 'POST'])
def sila():

        json=request.get_json()
        sila=(json['sila'])
        id=(json['id'])

        query= f"INSERT INTO sile(datum_vrijeme_upisa,vrijednost,veslac) VALUES(NOW(),{sila},{id})"
        cursor= mysql.connection.cursor()
        cursor.execute(query)

        mysql.connection.commit()
        #print (sila)
        return "ke"




@app.route('/nazad', methods=['GET'])
def nazad():
     return redirect(url_for('pocetna')), 303






if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)


