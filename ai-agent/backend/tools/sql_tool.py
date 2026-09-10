import os
import struct
import pyodbc
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    server = os.getenv("FABRIC_SQL_SERVER")
    database = os.getenv("FABRIC_SQL_DATABASE")

    # Authentification Azure AD (ton identité Microsoft)
    credential = DefaultAzureCredential()
    token = credential.get_token("https://database.windows.net/.default")
    token_bytes = token.token.encode("utf-16-le")
    token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)

    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Encrypt=yes;TrustServerCertificate=no;"
    )
    # 1256 = attribut spécial pour passer le token Azure AD
    return pyodbc.connect(conn_str, attrs_before={1256: token_struct})


def get_kpi_snapshot(month: str) -> list[dict]:
    """Récupère les KPI d'un mois donné (ex: '2024-03')."""
    query = """
        SELECT Month, Region, Category, Revenue, RevenueTarget,
               RevenueGapPct, RevenueStatus
        FROM dbo.vw_ai_kpi_snapshot
        WHERE Month = ?
        ORDER BY RevenueGapPct ASC
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, month)
    columns = [c[0] for c in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conn.close()
    return rows


# Test rapide
if __name__ == "__main__":
    results = get_kpi_snapshot("2024-03")
    print(f"{len(results)} lignes trouvées pour 2024-03\n")
    for r in results[:5]:
        print(f"{r['Region']:15} {r['Category']:25} "
              f"gap={r['RevenueGapPct']*100:.1f}% [{r['RevenueStatus']}]")