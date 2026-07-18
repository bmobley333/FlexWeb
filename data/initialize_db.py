# initialize_db.py
# Automated Supabase database tables initializer script.
# Connects to Supabase PostgreSQL database and runs schema.sql.

import os
import sys

def main():
    print("🌌 FlexWeb Supabase PostgreSQL Database Initializer")
    
    # Prompt the user for the connection string
    print("\nYou can retrieve your connection string from the Supabase dashboard:")
    print("Settings (gear icon) ➔ Database ➔ Connection string (choose 'URI' tab).")
    print("Example: postgresql://postgres:[password]@db.xxxxxx.supabase.co:5432/postgres\n")
    
    conn_str = input("Enter your Supabase PostgreSQL Connection URI:\n").strip()
    if not conn_str:
        print("ERROR: Connection string is required.")
        sys.exit(1)
        
    # Ensure psycopg2 is installed
    try:
        import psycopg2
    except ImportError:
        print("psycopg2-binary is not installed. Installing it now...")
        import subprocess
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "psycopg2-binary"], check=True)
            import psycopg2
        except Exception as e:
            print(f"ERROR: Failed to install psycopg2-binary: {e}")
            print("Please run: pip install psycopg2-binary")
            sys.exit(1)

    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    if not os.path.exists(schema_path):
        print(f"ERROR: schema.sql file not found at: {schema_path}")
        sys.exit(1)
        
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()
        
    print("\nConnecting to database...")
    try:
        conn = psycopg2.connect(conn_str)
        conn.autocommit = True
        cursor = conn.cursor()
        print("Running SQL DDL statements...")
        cursor.execute(sql)
        print("✅ Success! Database tables and indexes created successfully.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\nFallback: You can copy the contents of schema.sql and paste them directly into the 'SQL Editor' tab in the Supabase browser dashboard, then click 'Run'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
