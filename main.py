# IMPORT E CONFIGURAZIONE

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "matteo_esame_flask"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="libreria_flask_esame"
)
cursor = db.cursor(dictionary=True)


# CATALOGO PUBBLICO

# Elenco libri visibile a tutti
@app.route('/')
def catalogo():
    cursor.execute("""
        SELECT libri.titolo, libri.autore, libri.prezzo, magazzino.quantita
        FROM libri
        LEFT JOIN magazzino ON magazzino.libro_id = libri.id
    """)
    libri = cursor.fetchall()
    return render_template('catalogo.html', libri=libri)


# LOGIN, LOGOUT, DASHBOARD

# Login operatore
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM operatori WHERE username = %s AND password_hash = %s", (username, password))
        operatore = cursor.fetchone()

        if operatore:
            session['operatore_id'] = operatore['id']
            session['operatore_nome'] = operatore['nome']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', errore="Username o password errati")

    return render_template('login.html')


# Dashboard riservata
@app.route('/dashboard')
def dashboard():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# GESTIONE LIBRI

# Elenco libri (area riservata)
@app.route('/libri')
def gestione_libri():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("""
        SELECT libri.id, libri.titolo, libri.autore, libri.isbn, libri.prezzo,
               categorie.nome AS categoria, magazzino.quantita
        FROM libri
        LEFT JOIN categorie ON categorie.id = libri.categoria_id
        LEFT JOIN magazzino ON magazzino.libro_id = libri.id
    """)
    libri = cursor.fetchall()
    return render_template('gestione_libri.html', libri=libri)


# Aggiungi libro
@app.route('/libri/aggiungi', methods=['GET', 'POST'])
def aggiungi_libro():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        titolo = request.form['titolo']
        autore = request.form['autore']
        isbn = request.form['isbn']
        editore = request.form['editore']
        prezzo = request.form['prezzo']
        categoria_id = request.form['categoria_id']
        quantita = request.form['quantita']

        cursor.execute(
            "INSERT INTO libri (titolo, autore, isbn, editore, prezzo, categoria_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (titolo, autore, isbn, editore, prezzo, categoria_id)
        )
        db.commit()

        nuovo_libro_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO magazzino (libro_id, quantita) VALUES (%s, %s)",
            (nuovo_libro_id, quantita)
        )
        db.commit()

        return redirect(url_for('gestione_libri'))

    cursor.execute("SELECT * FROM categorie")
    categorie = cursor.fetchall()
    return render_template('aggiungi_libro.html', categorie=categorie)


# Modifica libro
@app.route('/libri/modifica/<int:id>', methods=['GET', 'POST'])
def modifica_libro(id):
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        titolo = request.form['titolo']
        autore = request.form['autore']
        isbn = request.form['isbn']
        editore = request.form['editore']
        prezzo = request.form['prezzo']
        categoria_id = request.form['categoria_id']
        quantita = request.form['quantita']

        cursor.execute(
            "UPDATE libri SET titolo=%s, autore=%s, isbn=%s, editore=%s, prezzo=%s, categoria_id=%s WHERE id=%s",
            (titolo, autore, isbn, editore, prezzo, categoria_id, id)
        )
        db.commit()

        cursor.execute(
            "UPDATE magazzino SET quantita=%s WHERE libro_id=%s",
            (quantita, id)
        )
        db.commit()

        return redirect(url_for('gestione_libri'))

    cursor.execute("""
        SELECT libri.*, magazzino.quantita
        FROM libri
        LEFT JOIN magazzino ON magazzino.libro_id = libri.id
        WHERE libri.id = %s
    """, (id,))
    libro = cursor.fetchone()

    cursor.execute("SELECT * FROM categorie")
    categorie = cursor.fetchall()

    return render_template('modifica_libro.html', libro=libro, categorie=categorie)


# Elimina libro
@app.route('/libri/elimina/<int:id>')
def elimina_libro(id):
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("DELETE FROM libri WHERE id = %s", (id,))
    db.commit()

    return redirect(url_for('gestione_libri'))


# GESTIONE CONTATTI

# Elenco contatti
@app.route('/contatti')
def gestione_contatti():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("SELECT * FROM utenti ORDER BY cognome, nome")
    utenti = cursor.fetchall()
    return render_template('gestione_contatti.html', utenti=utenti)


# Aggiungi contatto
@app.route('/contatti/aggiungi', methods=['GET', 'POST'])
def aggiungi_contatto():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        email = request.form['email']
        telefono = request.form['telefono']
        indirizzo = request.form['indirizzo']
        citta = request.form['citta']
        cap = request.form['cap']

        cursor.execute(
            "INSERT INTO utenti (nome, cognome, email, telefono, indirizzo, citta, cap) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nome, cognome, email, telefono, indirizzo, citta, cap)
        )
        db.commit()

        return redirect(url_for('gestione_contatti'))

    return render_template('aggiungi_contatto.html')


# Modifica contatto
@app.route('/contatti/modifica/<int:id>', methods=['GET', 'POST'])
def modifica_contatto(id):
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        email = request.form['email']
        telefono = request.form['telefono']
        indirizzo = request.form['indirizzo']
        citta = request.form['citta']
        cap = request.form['cap']

        cursor.execute(
            "UPDATE utenti SET nome=%s, cognome=%s, email=%s, telefono=%s, indirizzo=%s, citta=%s, cap=%s WHERE id=%s",
            (nome, cognome, email, telefono, indirizzo, citta, cap, id)
        )
        db.commit()

        return redirect(url_for('gestione_contatti'))

    cursor.execute("SELECT * FROM utenti WHERE id = %s", (id,))
    utente = cursor.fetchone()
    return render_template('modifica_contatto.html', utente=utente)


# Elimina contatto
@app.route('/contatti/elimina/<int:id>')
def elimina_contatto(id):
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("DELETE FROM utenti WHERE id = %s", (id,))
    db.commit()

    return redirect(url_for('gestione_contatti'))


# GESTIONE MAGAZZINO

# Elenco quantità a magazzino
@app.route('/magazzino')
def gestione_magazzino():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("""
        SELECT libri.id, libri.titolo, libri.autore, magazzino.quantita
        FROM libri
        LEFT JOIN magazzino ON magazzino.libro_id = libri.id
        ORDER BY libri.titolo
    """)
    libri = cursor.fetchall()
    return render_template('gestione_magazzino.html', libri=libri)


# Modifica quantità di un libro
@app.route('/magazzino/modifica/<int:id>', methods=['GET', 'POST'])
def modifica_quantita(id):
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        quantita = request.form['quantita']

        cursor.execute(
            "UPDATE magazzino SET quantita=%s WHERE libro_id=%s",
            (quantita, id)
        )
        db.commit()

        return redirect(url_for('gestione_magazzino'))

    cursor.execute("""
        SELECT libri.id, libri.titolo, magazzino.quantita
        FROM libri
        LEFT JOIN magazzino ON magazzino.libro_id = libri.id
        WHERE libri.id = %s
    """, (id,))
    libro = cursor.fetchone()
    return render_template('modifica_quantita.html', libro=libro)


# NUOVO ACQUISTO

# Registra acquisto (utente esistente + un libro)
@app.route('/acquisti/nuovo', methods=['GET', 'POST'])
def nuovo_acquisto():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        utente_id = request.form['utente_id']
        libro_id = request.form['libro_id']
        quantita_acquistata = int(request.form['quantita'])

        cursor.execute("""
            SELECT libri.prezzo, magazzino.quantita
            FROM libri
            LEFT JOIN magazzino ON magazzino.libro_id = libri.id
            WHERE libri.id = %s
        """, (libro_id,))
        libro = cursor.fetchone()

        if libro['quantita'] < quantita_acquistata:
            return render_template('nuovo_acquisto.html',
                                    utenti=get_utenti(), libri=get_libri(),
                                    errore="Copie disponibili insufficienti")

        totale = float(libro['prezzo']) * quantita_acquistata

        cursor.execute(
            "INSERT INTO vendite (utente_id, totale) VALUES (%s, %s)",
            (utente_id, totale)
        )
        db.commit()

        nuova_vendita_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO vendite_dettagli (vendita_id, libro_id, quantita, prezzo_unitario) VALUES (%s, %s, %s, %s)",
            (nuova_vendita_id, libro_id, quantita_acquistata, libro['prezzo'])
        )
        db.commit()

        cursor.execute(
            "UPDATE magazzino SET quantita = quantita - %s WHERE libro_id = %s",
            (quantita_acquistata, libro_id)
        )
        db.commit()

        return redirect(url_for('gestione_magazzino'))

    return render_template('nuovo_acquisto.html', utenti=get_utenti(), libri=get_libri())


# Elenco utenti (supporto form acquisto)
def get_utenti():
    cursor.execute("SELECT * FROM utenti ORDER BY cognome, nome")
    return cursor.fetchall()


# Elenco libri disponibili (supporto form acquisto)
def get_libri():
    cursor.execute("""
        SELECT libri.id, libri.titolo, libri.prezzo, magazzino.quantita
        FROM libri
        LEFT JOIN magazzino ON magazzino.libro_id = libri.id
        WHERE magazzino.quantita > 0
    """)
    return cursor.fetchall()


# STORICO VENDITE

# Elenco vendite con dettaglio libri
@app.route('/vendite')
def storico_vendite():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    cursor.execute("""
        SELECT vendite.id, vendite.data_vendita, vendite.totale,
               utenti.nome, utenti.cognome
        FROM vendite
        JOIN utenti ON utenti.id = vendite.utente_id
        ORDER BY vendite.data_vendita DESC
    """)
    vendite = cursor.fetchall()

    for vendita in vendite:
        cursor.execute("""
            SELECT libri.titolo, vendite_dettagli.quantita, vendite_dettagli.prezzo_unitario
            FROM vendite_dettagli
            JOIN libri ON libri.id = vendite_dettagli.libro_id
            WHERE vendite_dettagli.vendita_id = %s
        """, (vendita['id'],))
        vendita['dettagli'] = cursor.fetchall()

    return render_template('storico_vendite.html', vendite=vendite)


# RICERCA LIBRI

# Cerca libro per titolo o autore
@app.route('/cerca-libro', methods=['GET', 'POST'])
def cerca_libro():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    risultati = []
    termine_cercato = ''

    if request.method == 'POST':
        termine_cercato = request.form['termine']

        cursor.execute("""
            SELECT libri.titolo, libri.autore, libri.prezzo, magazzino.quantita
            FROM libri
            LEFT JOIN magazzino ON magazzino.libro_id = libri.id
            WHERE libri.titolo LIKE %s OR libri.autore LIKE %s
        """, (f"%{termine_cercato}%", f"%{termine_cercato}%"))
        risultati = cursor.fetchall()

    return render_template('cerca_libro.html', risultati=risultati, termine_cercato=termine_cercato)


# RICERCA PERSONE

# Cerca cliente e mostra storico acquisti
@app.route('/cerca-persona', methods=['GET', 'POST'])
def cerca_persona():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    risultati = []
    termine_cercato = ''

    if request.method == 'POST':
        termine_cercato = request.form['termine']

        cursor.execute("""
            SELECT * FROM utenti
            WHERE nome LIKE %s OR cognome LIKE %s
        """, (f"%{termine_cercato}%", f"%{termine_cercato}%"))
        risultati = cursor.fetchall()

        for utente in risultati:
            cursor.execute("""
                SELECT vendite.id, vendite.data_vendita, vendite.totale
                FROM vendite
                WHERE vendite.utente_id = %s
                ORDER BY vendite.data_vendita DESC
            """, (utente['id'],))
            utente['acquisti'] = cursor.fetchall()

    return render_template('cerca_persona.html', risultati=risultati, termine_cercato=termine_cercato)


# NUOVO UTENTE CON ACQUISTO IMMEDIATO

# Crea cliente e registra subito un acquisto
@app.route('/acquisti/nuovo-utente', methods=['GET', 'POST'])
def nuovo_utente_e_acquisto():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        cognome = request.form['cognome']
        email = request.form['email']
        telefono = request.form['telefono']
        indirizzo = request.form['indirizzo']
        citta = request.form['citta']
        cap = request.form['cap']

        libro_id = request.form['libro_id']
        quantita_acquistata = int(request.form['quantita'])

        cursor.execute("""
            SELECT libri.prezzo, magazzino.quantita
            FROM libri
            LEFT JOIN magazzino ON magazzino.libro_id = libri.id
            WHERE libri.id = %s
        """, (libro_id,))
        libro = cursor.fetchone()

        if libro['quantita'] < quantita_acquistata:
            return render_template('nuovo_utente_acquisto.html', libri=get_libri(),
                                    errore="Copie disponibili insufficienti")

        cursor.execute(
            "INSERT INTO utenti (nome, cognome, email, telefono, indirizzo, citta, cap) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (nome, cognome, email, telefono, indirizzo, citta, cap)
        )
        db.commit()

        nuovo_utente_id = cursor.lastrowid

        totale = float(libro['prezzo']) * quantita_acquistata

        cursor.execute(
            "INSERT INTO vendite (utente_id, totale) VALUES (%s, %s)",
            (nuovo_utente_id, totale)
        )
        db.commit()

        nuova_vendita_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO vendite_dettagli (vendita_id, libro_id, quantita, prezzo_unitario) VALUES (%s, %s, %s, %s)",
            (nuova_vendita_id, libro_id, quantita_acquistata, libro['prezzo'])
        )
        db.commit()

        cursor.execute(
            "UPDATE magazzino SET quantita = quantita - %s WHERE libro_id = %s",
            (quantita_acquistata, libro_id)
        )
        db.commit()

        return redirect(url_for('gestione_magazzino'))

    return render_template('nuovo_utente_acquisto.html', libri=get_libri())


# STATISTICHE VENDITE

# Statistiche vendite con filtro mese/anno
@app.route('/statistiche')
def statistiche_vendite():
    if 'operatore_id' not in session:
        return redirect(url_for('login'))

    periodo_scelto = request.args.get('periodo', '')

    cursor.execute("""
        SELECT DISTINCT DATE_FORMAT(data_vendita, '%Y-%m') AS periodo
        FROM vendite
        ORDER BY periodo DESC
    """)
    periodi_disponibili = cursor.fetchall()

    if periodo_scelto:
        filtro_data = "AND DATE_FORMAT(vendite.data_vendita, '%Y-%m') = %s"
        parametro = (periodo_scelto,)
    else:
        filtro_data = ""
        parametro = ()

    cursor.execute(f"""
        SELECT libri.titolo, SUM(vendite_dettagli.quantita) AS totale_venduto
        FROM vendite_dettagli
        JOIN libri ON libri.id = vendite_dettagli.libro_id
        JOIN vendite ON vendite.id = vendite_dettagli.vendita_id
        WHERE 1=1 {filtro_data}
        GROUP BY libri.id, libri.titolo
        ORDER BY totale_venduto DESC
    """, parametro)
    libri_piu_venduti = cursor.fetchall()

    cursor.execute(f"""
        SELECT SUM(totale) AS incasso_totale
        FROM vendite
        WHERE 1=1 {filtro_data}
    """, parametro)
    incasso = cursor.fetchone()

    cursor.execute(f"""
        SELECT utenti.nome, utenti.cognome, SUM(vendite.totale) AS totale_speso
        FROM vendite
        JOIN utenti ON utenti.id = vendite.utente_id
        WHERE 1=1 {filtro_data}
        GROUP BY utenti.id, utenti.nome, utenti.cognome
        ORDER BY totale_speso DESC
    """, parametro)
    classifica_clienti = cursor.fetchall()

    return render_template('statistiche.html',
                            libri_piu_venduti=libri_piu_venduti,
                            incasso=incasso,
                            classifica_clienti=classifica_clienti,
                            periodi_disponibili=periodi_disponibili,
                            periodo_scelto=periodo_scelto)


# AVVIO APPLICAZIONE

if __name__ == '__main__':
    app.run(debug=True)