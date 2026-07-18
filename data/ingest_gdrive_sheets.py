# ingest_gdrive_sheets.py
# Scrapes Powers, Magic Items, and SkillSets from Google Sheet and populates Supabase database.

import sys
import os
import json
import psycopg2

# Add gdrive-helper path to system path
sys.path.append(r"C:\Repos\Jodar\services\gdrive-helper")
import drive_helper
from googleapiclient.discovery import build

SPREADSHEET_ID = "1v3ixyJa8EoxLRTYpxVtqPm6AmWLFALHZSdEufjNxS8s"
DB_URI = "postgresql://postgres.yqwrvtgkrwbakehbckrn:I3iJp%25%40TmGp95LvF@aws-0-ca-central-1.pooler.supabase.com:5432/postgres"

def clean_row(row, min_cols=10):
    # Pad row with empty strings if it has fewer columns
    if len(row) < min_cols:
        row += [""] * (min_cols - len(row))
    return [c.strip() if c else "" for c in row]

def ingest_powers(sheets_service, db_conn):
    print("\n⚡ Ingesting Powers...")
    res = sheets_service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Powers!A5:L1000"
    ).execute()
    rows = res.get("values", [])
    if not rows:
        print("No powers data found.")
        return

    # Check headers
    headers = [h.lower() for h in clean_row(rows[0])]
    print(f"Headers: {headers}")

    # Extract indexes
    idx_name = headers.index("power")
    idx_usage = headers.index("usage")
    idx_action = headers.index("action")
    idx_effect = headers.index("effect")
    idx_source = headers.index("source")

    cursor = db_conn.cursor()
    # Clear existing powers
    cursor.execute("TRUNCATE TABLE powers RESTART IDENTITY;")
    
    count = 0
    for r in rows[1:]:
        cleaned = clean_row(r, len(headers))
        if not cleaned[idx_name]:
            continue # skip empty rows
        
        name = cleaned[idx_name]
        usage = cleaned[idx_usage]
        action = cleaned[idx_action]
        effect = cleaned[idx_effect]
        source = cleaned[idx_source]

        cursor.execute(
            """
            INSERT INTO powers (name, usage, action, effect, source)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET
                usage = EXCLUDED.usage,
                action = EXCLUDED.action,
                effect = EXCLUDED.effect,
                source = EXCLUDED.source;
            """,
            (name, usage, action, effect, source)
        )
        count += 1

    db_conn.commit()
    cursor.close()
    print(f"✅ Successfully ingested {count} powers.")

def ingest_magic_items(sheets_service, db_conn):
    print("\n✨ Ingesting Magic Items...")
    res = sheets_service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Magic Items!A5:L1000"
    ).execute()
    rows = res.get("values", [])
    if not rows:
        print("No magic items data found.")
        return

    headers = [h.lower() for h in clean_row(rows[0])]
    print(f"Headers: {headers}")

    idx_name = headers.index("name")
    idx_usage = headers.index("usage")
    idx_action = headers.index("action")
    idx_effect = headers.index("effect")
    idx_source = headers.index("source")

    cursor = db_conn.cursor()
    # Clear existing magic items
    cursor.execute("TRUNCATE TABLE magic_items RESTART IDENTITY;")

    count = 0
    for r in rows[1:]:
        cleaned = clean_row(r, len(headers))
        if not cleaned[idx_name]:
            continue
        
        name = cleaned[idx_name]
        usage = cleaned[idx_usage]
        action = cleaned[idx_action]
        effect = cleaned[idx_effect]
        source = cleaned[idx_source]

        cursor.execute(
            """
            INSERT INTO magic_items (name, usage, action, effect, source)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET
                usage = EXCLUDED.usage,
                action = EXCLUDED.action,
                effect = EXCLUDED.effect,
                source = EXCLUDED.source;
            """,
            (name, usage, action, effect, source)
        )
        count += 1

    db_conn.commit()
    cursor.close()
    print(f"✅ Successfully ingested {count} magic items.")

def ingest_skillsets(sheets_service, db_conn):
    print("\n🎓 Ingesting SkillSets...")
    res = sheets_service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="SkillSets!A5:L1000"
    ).execute()
    rows = res.get("values", [])
    if not rows:
        print("No skillsets data found.")
        return

    headers = [h.lower() for h in clean_row(rows[0])]
    print(f"Headers: {headers}")

    idx_name = headers.index("name")
    idx_skills = headers.index("skills")
    idx_source = headers.index("source")

    cursor = db_conn.cursor()
    # Clear existing skillsets
    cursor.execute("TRUNCATE TABLE skillsets RESTART IDENTITY;")

    count = 0
    for r in rows[1:]:
        cleaned = clean_row(r, len(headers))
        if not cleaned[idx_name]:
            continue

        name = cleaned[idx_name]
        skills_str = cleaned[idx_skills]
        source = cleaned[idx_source]

        # Parse skills to JSON list
        skills_list = [s.strip() for s in skills_str.split(",") if s.strip()]

        cursor.execute(
            """
            INSERT INTO skillsets (name, skills, source)
            VALUES (%s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET
                skills = EXCLUDED.skills,
                source = EXCLUDED.source;
            """,
            (name, json.dumps(skills_list), source)
        )
        count += 1

    db_conn.commit()
    cursor.close()
    print(f"✅ Successfully ingested {count} skillsets.")

def main():
    print("🌌 FlexWeb Google Sheet Rules Ingestor Starting...")
    try:
        creds = drive_helper.get_credentials("metascapegame")
        sheets_service = build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"ERROR: Google API initialization failed: {e}")
        sys.exit(1)

    try:
        db_conn = psycopg2.connect(DB_URI)
        print("Connected to Supabase PostgreSQL database successfully.")
    except Exception as e:
        print(f"ERROR: Database connection failed: {e}")
        sys.exit(1)

    try:
        ingest_powers(sheets_service, db_conn)
        ingest_magic_items(sheets_service, db_conn)
        ingest_skillsets(sheets_service, db_conn)
        print("\n🎉 Database Ingestion Complete!")
    except Exception as e:
        print(f"\n❌ Ingestion failed: {e}")
    finally:
        db_conn.close()

if __name__ == "__main__":
    main()
