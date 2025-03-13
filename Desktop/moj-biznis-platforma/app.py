import sqlite3
import qrcode
from flask import Flask, request, jsonify

app = Flask(__name__)

# Konfigurácia databázy
DATABASE = 'databaza.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def generuj_qr_kod(data, subor):
    """Vygeneruje QR kód a uloží ho do súboru."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(subor)

# --- Dotazník ---
@app.route('/dotaznik', methods=['GET', 'POST'])
def dotaznik():
    if request.method == 'GET':
        return jsonify({'message': 'Dotazník zatiaľ nie je implementovaný'})
    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({'message': 'Odpovede boli úspešne spracované!'}), 200
    else:
        return "Metóda nie je povolená", 405

# --- Marketingový Asistent ---
@app.route('/kampane', methods=['GET', 'POST'])
def sprava_kampani():
    conn = get_db_connection()
    if request.method == 'GET':
        kampane = conn.execute('SELECT id, nazov, cielova_skupina, sprava FROM kampane').fetchall()
        conn.close()
        return jsonify([dict(row) for row in kampane])
    elif request.method == 'POST':
        data = request.get_json()
        nazov = data['nazov']
        cielova_skupina = data['cielova_skupina']
        sprava = data['sprava']
        conn.execute('INSERT INTO kampane (nazov, cielova_skupina, sprava) VALUES (?, ?, ?)', (nazov, cielova_skupina, sprava))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Kampan bola úspešne vytvorená!'}), 201
    else:
        return "Metóda nie je povolená", 405

# --- Platba cez QR kód ---
@app.route('/platba', methods=['GET'])
def platba():
    cislo_uctu = "SK12345678901234567890"
    suma = 9.99
    variabilny_symbol = "1234567890"
    popis = "Platba za prémiové funkcie"

    platobne_udaje = f"iban={cislo_uctu}&amount={suma}&vs={variabilny_symbol}¤cy=EUR&message={popis}"

    subor = "qr_kod.png"
    generuj_qr_kod(platobne_udaje, subor)

    return jsonify({'message': 'QR kód bol vygenerovaný'})

# --- Objednávkový Asistent --- (Zatiaľ prázdne)
@app.route('/produkty', methods=['GET', 'POST'])
def sprava_produktov():
    return jsonify({'message': 'Objednávkový asistent zatiaľ nie je implementovaný'})

if __name__ == '__main__':
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS kampane (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazov TEXT NOT NULL,
        cielova_skupina TEXT,
        sprava TEXT
    )
    """)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS produkty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazov TEXT NOT NULL,
        popis TEXT,
        cena REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()
    app.run(debug=True)