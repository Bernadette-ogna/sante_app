import flet as ft
import psycopg2
from psycopg2 import OperationalError
from datetime import datetime

# ================= CONFIG =================
DB_NAME = "sante"
DB_USER = "sante_user"   # ⚠️ recommandé
DB_PASS = "sante123"       # ⚠️ mets TON vrai mot de passe postgres
DB_HOST = "localhost"
DB_PORT = "5432"

ADMIN_USER = 'admin'
ADMIN_PASS = '1234'

BG = 'https://images.unsplash.com/photo-1576091160550-2173dba999ef'


# ================= DB CONNECTION =================
def get_conn():
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
    except OperationalError as e:
        print("❌ Erreur connexion PostgreSQL :", e)
        return None


# ================= INIT DB =================
def init_db():
    conn = get_conn()
    if conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute('''
                CREATE TABLE IF NOT EXISTS recensement(
                    id SERIAL PRIMARY KEY,
                    nom TEXT,
                    prenom TEXT,
                    ville TEXT,
                    alimentation TEXT,
                    sport TEXT,
                    sommeil TEXT,
                    stress TEXT,
                    tabac TEXT,
                    alcool TEXT,
                    eau TEXT,
                    created_at TEXT
                )
                ''')
        conn.close()


# ================= APP =================
def main(page: ft.Page):

    init_db()

    page.title = 'Santé Premium'
    page.window_width = 1400
    page.window_height = 900
    page.padding = 0
    page.scroll = 'auto'

    # ================= HOME =================
    def home():
        page.controls.clear()

        box = ft.Container(
            width=1100,
            bgcolor='#00000099',
            padding=25,
            border_radius=20,
            content=ft.Column([
                ft.Text('🏥 BIENVENUE  SUR HEALTH FACTS', size=38, weight='bold', color='white'),
                ft.Text('Collecte intelligente des facteurs de santé.', size=18, color='white70'),
                ft.Row([
                    ft.ElevatedButton('COMMENCER', on_click=lambda e: form()),
                    ft.OutlinedButton('ADMIN', on_click=lambda e: login())
                ], alignment='center')
            ], horizontal_alignment='center')
        )

        page.add(ft.Stack([
            ft.Image(src=BG, fit='cover', expand=True),
            ft.Column([box], alignment='center', horizontal_alignment='center', expand=True)
        ], expand=True))

        page.update()

    # ================= FORM =================
    def form():
        page.controls.clear()

        nom = ft.TextField(label='Nom')
        prenom = ft.TextField(label='Prénom')
        ville = ft.TextField(label='Ville')

        alimentation = ft.Dropdown(label='Alimentation',
            options=[ft.dropdown.Option(x) for x in ['Mauvaise','Moyenne','Bonne']])

        sport = ft.Dropdown(label='Sport',
            options=[ft.dropdown.Option(x) for x in ['Jamais','Parfois','Régulière']])

        sommeil = ft.Dropdown(label='Sommeil',
            options=[ft.dropdown.Option(x) for x in ['Mauvais','Moyen','Bon']])

        stress = ft.Dropdown(label='Stress',
            options=[ft.dropdown.Option(x) for x in ['Faible','Moyen','Élevé']])

        tabac = ft.Dropdown(label='Tabac',
            options=[ft.dropdown.Option('Oui'), ft.dropdown.Option('Non')])

        alcool = ft.Dropdown(label='Alcool',
            options=[ft.dropdown.Option('Oui'), ft.dropdown.Option('Non')])

        eau = ft.Dropdown(label='Hydratation',
            options=[ft.dropdown.Option('Faible'), ft.dropdown.Option('Correcte')])

        msg = ft.Text()

        def save(e):
            conn = get_conn()
            if not conn:
                msg.value = "❌ Erreur connexion base"
                msg.color = "red"
                page.update()
                return

            try:
                with conn:
                    with conn.cursor() as cur:
                        cur.execute('''
                        INSERT INTO recensement(
                            nom,prenom,ville,alimentation,sport,
                            sommeil,stress,tabac,alcool,eau,created_at
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ''', (
                            nom.value, prenom.value, ville.value,
                            alimentation.value, sport.value,
                            sommeil.value, stress.value,
                            tabac.value, alcool.value,
                            eau.value, datetime.now().isoformat()
                        ))

                msg.value = "Données enregistrées ✅"
                msg.color = "green"

            except Exception as e:
                msg.value = f"Erreur : {e}"
                msg.color = "red"

            finally:
                conn.close()

            page.update()

        card = ft.Container(
            width=700,
            padding=20,
            bgcolor='#ffffffee',
            border_radius=20,
            content=ft.Column([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: home()),
                ft.Text('Formulaire Santé', size=28, weight='bold'),
                nom, prenom, ville,
                alimentation, sport, sommeil, stress,
                tabac, alcool, eau,
                ft.ElevatedButton('Enregistrer', on_click=save),
                msg
            ], scroll='auto')
        )

        page.add(ft.Stack([
            ft.Image(src=BG, fit='cover', expand=True),
            ft.Column([card], alignment='center', horizontal_alignment='center', expand=True)
        ], expand=True))

        page.update()

    # ================= LOGIN =================
    def login():
        page.controls.clear()

        u = ft.TextField(label='Utilisateur')
        p = ft.TextField(label='Mot de passe', password=True)
        m = ft.Text(color='red')

        def go(e):
            if u.value == ADMIN_USER and p.value == ADMIN_PASS:
                dashboard()
            else:
                m.value = 'Accès refusé'
                page.update()

        box = ft.Container(
            width=400,
            padding=20,
            bgcolor='white',
            border_radius=20,
            content=ft.Column([
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: home()),
                ft.Text('Admin', size=28, weight='bold'),
                u, p,
                ft.ElevatedButton('Connexion', on_click=go),
                m
            ])
        )

        page.add(ft.Stack([
            ft.Image(src=BG, fit='cover', expand=True),
            ft.Column([box], alignment='center', horizontal_alignment='center', expand=True)
        ], expand=True))

        page.update()

    # ================= DASHBOARD =================
    def dashboard():
        page.controls.clear()

        conn = get_conn()
        if not conn:
            page.add(ft.Text("❌ Impossible de charger les données"))
            page.update()
            return

        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute('''
                    SELECT nom,prenom,ville,stress,tabac,alcool
                    FROM recensement
                    ORDER BY id DESC
                    ''')
                    data = cur.fetchall()
        except Exception as e:
            page.add(ft.Text(f"Erreur : {e}"))
            page.update()
            return
        finally:
            conn.close()

        rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(str(v))) for v in r]) for r in data]

        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(x)) for x in
                     ['Nom','Prénom','Ville','Stress','Tabac','Alcool']],
            rows=rows
        )

        page.add(ft.Row([
            ft.Container(
                width=240,
                bgcolor='#0f172a',
                padding=20,
                content=ft.Column([
                    ft.Text('ADMIN', size=28, color='white', weight='bold'),
                    ft.ElevatedButton('Déconnexion', on_click=lambda e: home())
                ])
            ),
            ft.Container(
                expand=True,
                bgcolor='#f8fafc',
                padding=20,
                content=ft.Column([
                    ft.Text('Dashboard Santé', size=30, weight='bold'),
                    ft.Text(f'Total participants: {len(data)}'),
                    table
                ], scroll='auto')
            )
        ], expand=True))

        page.update()

    home()


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
