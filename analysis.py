import sqlite3
from contextlib import closing
from pathlib import Path


DB_PATH = Path(__file__).parent / "ymmo.db"


def connect_db():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Base de données introuvable : {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def print_title(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_subtitle(title: str):
    print("\n" + "-" * 70)
    print(title)
    print("-" * 70)


def analyze_properties(conn: sqlite3.Connection):
    print_title("ANALYSE DES BIENS (TABLE properties)")

    with closing(conn.cursor()) as cur:
        # Nombre total de biens
        cur.execute("SELECT COUNT(*) AS n FROM properties;")
        total = cur.fetchone()["n"]
        print(f"Nombre total de biens : {total}")

        # Répartition par statut
        print_subtitle("Répartition par statut")
        cur.execute("""
            SELECT status, COUNT(*) AS n, 
                   ROUND(AVG(price), 0) AS avg_price
            FROM properties
            GROUP BY status
            ORDER BY n DESC;
        """)
        rows = cur.fetchall()
        if not rows:
            print("Aucun bien enregistré.")
        else:
            print(f"{'Statut':12} | {'Nb biens':8} | {'Prix moyen (€)':14}")
            print("-" * 45)
            for r in rows:
                statut = r["status"] or "inconnu"
                print(f"{statut:12} | {r['n']:8} | {int(r['avg_price']) if r['avg_price'] is not None else '-':14}")

        # Prix min / max / moyen global
        print_subtitle("Prix global")
        cur.execute("""
            SELECT 
                ROUND(AVG(price), 0) AS avg_price,
                MIN(price) AS min_price,
                MAX(price) AS max_price
            FROM properties;
        """)
        r = cur.fetchone()
        if r and r["avg_price"] is not None:
            print(f"Prix moyen : {int(r['avg_price'])} €")
            print(f"Prix min   : {int(r['min_price'])} €")
            print(f"Prix max   : {int(r['max_price'])} €")
        else:
            print("Pas assez de données pour calculer les prix.")

        # Prix moyen par ville
        print_subtitle("Prix moyen par ville (top 10)")
        cur.execute("""
            SELECT city,
                   COUNT(*) AS n,
                   ROUND(AVG(price), 0) AS avg_price
            FROM properties
            GROUP BY city
            HAVING city IS NOT NULL AND city <> ''
            ORDER BY avg_price DESC
            LIMIT 10;
        """)
        rows = cur.fetchall()
        if not rows:
            print("Aucune ville renseignée.")
        else:
            print(f"{'Ville':18} | {'Nb biens':8} | {'Prix moyen (€)':14}")
            print("-" * 50)
            for r in rows:
                print(f"{(r['city'] or '—'):18} | {r['n']:8} | {int(r['avg_price']) if r['avg_price'] is not None else '-':14}")

        # Top 5 villes par volume de biens
        print_subtitle("Top 5 villes par nombre de biens")
        cur.execute("""
            SELECT city,
                   COUNT(*) AS n
            FROM properties
            GROUP BY city
            HAVING city IS NOT NULL AND city <> ''
            ORDER BY n DESC
            LIMIT 5;
        """)
        rows = cur.fetchall()
        if not rows:
            print("Aucune ville renseignée.")
        else:
            print(f"{'Ville':18} | {'Nb biens':8}")
            print("-" * 32)
            for r in rows:
                print(f"{(r['city'] or '—'):18} | {r['n']:8}")


def analyze_clients(conn: sqlite3.Connection):
    print_title("ANALYSE DES CLIENTS (TABLE clients)")

    with closing(conn.cursor()) as cur:
        # Nombre total de clients
        cur.execute("SELECT COUNT(*) AS n FROM clients;")
        total = cur.fetchone()["n"]
        print(f"Nombre total de clients : {total}")

        # Répartition par type (acheteur / vendeur)
        print_subtitle("Répartition par type")
        cur.execute("""
            SELECT type, COUNT(*) AS n
            FROM clients
            GROUP BY type
            ORDER BY n DESC;
        """)
        rows = cur.fetchall()
        if not rows:
            print("Aucun client enregistré.")
        else:
            print(f"{'Type':12} | {'Nb clients':10}")
            print("-" * 28)
            for r in rows:
                t = r["type"] or "inconnu"
                print(f"{t:12} | {r['n']:10}")


def analyze_transactions(conn: sqlite3.Connection):
    print_title("ANALYSE DES TRANSACTIONS (TABLE transactions)")

    with closing(conn.cursor()) as cur:
        # Nombre total de transactions
        cur.execute("SELECT COUNT(*) AS n FROM transactions;")
        total = cur.fetchone()["n"]
        print(f"Nombre total de transactions : {total}")

        if total == 0:
            print("Aucune transaction pour le moment.")
            return

        # CA total et moyen
        print_subtitle("Chiffre d'affaires")
        cur.execute("""
            SELECT 
                SUM(price) AS total_revenue,
                ROUND(AVG(price), 0) AS avg_price
            FROM transactions;
        """)
        r = cur.fetchone()
        print(f"CA total : {int(r['total_revenue'])} €")
        print(f"Prix moyen par transaction : {int(r['avg_price'])} €")

        # Transactions par année (si tu mets des dates au format YYYY-MM-DD)
        print_subtitle("Transactions par année (si date au format YYYY-MM-DD)")
        cur.execute("""
            SELECT SUBSTR(date, 1, 4) AS year,
                   COUNT(*) AS n,
                   SUM(price) AS revenue
            FROM transactions
            WHERE date IS NOT NULL AND LENGTH(date) >= 4
            GROUP BY year
            ORDER BY year;
        """)
        rows = cur.fetchall()
        if not rows:
            print("Aucune année exploitable (format attendu : YYYY-MM-DD).")
        else:
            print(f"{'Année':8} | {'Nb transac':10} | {'CA (€)':12}")
            print("-" * 38)
            for r in rows:
                print(f"{(r['year'] or '—'):8} | {r['n']:10} | {int(r['revenue']) if r['revenue'] is not None else '-':12}")


def main():
    print("=== YMmo — Analyse de la base de données ===")
    print(f"Base : {DB_PATH}")

    try:
        conn = connect_db()
    except FileNotFoundError as e:
        print(e)
        return

    with conn:
        analyze_properties(conn)
        analyze_clients(conn)
        analyze_transactions(conn)


if __name__ == "__main__":
    main()