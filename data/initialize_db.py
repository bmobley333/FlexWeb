# initialize_db.py
# Automated Supabase database tables initializer and data seeder script.
# Connects to Supabase PostgreSQL database, runs schema_v2.sql, and seeds rules data.

import os
import sys
import json
import pandas as pd
import psycopg2

def main():
    print("🌌 FlexWeb Supabase PostgreSQL Database Initializer & Seeder (v2)")
    
    # Prompt the user for the connection string
    print("\nYou can retrieve your connection string from the Supabase dashboard:")
    print("Settings (gear icon) ➔ Database ➔ Connection string (choose 'URI' tab).")
    print("Example: postgresql://postgres:[password]@db.xxxxxx.supabase.co:5432/postgres\n")
    
    conn_str = input("Enter your Supabase PostgreSQL Connection URI:\n").strip()
    if not conn_str:
        print("ERROR: Connection URI is required.")
        sys.exit(1)

    schema_path = os.path.join(os.path.dirname(__file__), "schema_v2.sql")
    if not os.path.exists(schema_path):
        print(f"ERROR: schema_v2.sql file not found at: {schema_path}")
        sys.exit(1)
        
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()
        
    print("\nConnecting to database and running DDL schema...")
    try:
        conn = psycopg2.connect(conn_str)
        conn.autocommit = True
        cursor = conn.cursor()
        print("Running SQL schema_v2.sql statements...")
        cursor.execute(sql)
        print("✅ Database schema initialized successfully.")
    except Exception as e:
        print(f"❌ Connection or execution failed: {e}")
        sys.exit(1)

    # Database connection is active. Now let's seed the tables!
    db_file_path = r"C:\Repos\Projects\FlexWeb\OldFlexMoxieRaw\FlexMoxie - DB.xlsx"
    if not os.path.exists(db_file_path):
        print(f"ERROR: FlexMoxie - DB.xlsx not found at: {db_file_path}")
        cursor.close()
        conn.close()
        sys.exit(1)

    print(f"\nSeeding database rules from local spreadsheet: {db_file_path}")
    
    # 1. Seed Powers
    try:
        print("Reading 'Powers' sheet...")
        df_powers = pd.read_excel(db_file_path, sheet_name="Powers")
        df_powers = df_powers.dropna(subset=['AbilityName'])
        
        # Clear existing powers
        cursor.execute("TRUNCATE TABLE powers RESTART IDENTITY CASCADE;")
        
        print(f"Inserting {len(df_powers)} powers...")
        insert_query = """
            INSERT INTO powers (name, sub, table_name, usage, action, effect, source, dropdown)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        for _, row in df_powers.iterrows():
            name = str(row['AbilityName']).strip()
            sub = str(row['SubType']).strip() if pd.notna(row['SubType']) else None
            table_name = str(row['TableName']).strip() if pd.notna(row['TableName']) else None
            usage = str(row['Usage']).strip() if pd.notna(row['Usage']) else None
            action = str(row['Action']).strip() if pd.notna(row['Action']) else None
            effect = str(row['Effect']).strip() if pd.notna(row['Effect']) else None
            source = str(row['Source']).strip() if pd.notna(row['Source']) else None
            dropdown = str(row['DropDown']).strip() if pd.notna(row['DropDown']) else None
            
            cursor.execute(insert_query, (name, sub, table_name, usage, action, effect, source, dropdown))
        print("✅ Powers seeded successfully!")
    except Exception as e:
        print(f"❌ Failed to seed Powers: {e}")

    # 2. Seed Magic Items
    try:
        print("\nReading 'Magic Items' sheet...")
        df_items = pd.read_excel(db_file_path, sheet_name="Magic Items")
        df_items = df_items.dropna(subset=['AbilityName'])
        
        # Clear existing magic items
        cursor.execute("TRUNCATE TABLE magic_items RESTART IDENTITY CASCADE;")
        
        print(f"Inserting {len(df_items)} magic items...")
        insert_query = """
            INSERT INTO magic_items (name, sub, table_name, usage, action, effect, source, dropdown)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        for _, row in df_items.iterrows():
            name = str(row['AbilityName']).strip()
            sub = str(row['SubType']).strip() if pd.notna(row['SubType']) else None
            table_name = str(row['TableName']).strip() if pd.notna(row['TableName']) else None
            usage = str(row['Usage']).strip() if pd.notna(row['Usage']) else None
            action = str(row['Action']).strip() if pd.notna(row['Action']) else None
            effect = str(row['Effect']).strip() if pd.notna(row['Effect']) else None
            source = str(row['Source']).strip() if pd.notna(row['Source']) else None
            dropdown = str(row['DropDown']).strip() if pd.notna(row['DropDown']) else None
            
            cursor.execute(insert_query, (name, sub, table_name, usage, action, effect, source, dropdown))
        print("✅ Magic Items seeded successfully!")
    except Exception as e:
        print(f"❌ Failed to seed Magic Items: {e}")

    # 3. Seed SkillSets
    try:
        print("\nReading 'SkillSets' sheet...")
        df_sets = pd.read_excel(db_file_path, sheet_name="SkillSets")
        df_sets = df_sets.dropna(subset=['SkillSet'])
        
        # Clear existing skillsets
        cursor.execute("TRUNCATE TABLE skillsets RESTART IDENTITY CASCADE;")
        
        print(f"Inserting {len(df_sets)} skillsets...")
        insert_query = """
            INSERT INTO skillsets (name, skills, source, sub, table_name, dropdown)
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        for _, row in df_sets.iterrows():
            name = str(row['SkillSet']).strip()
            skills_raw = str(row['SkillList']).strip() if pd.notna(row['SkillList']) else ""
            skills = [s.strip() for s in skills_raw.split(",") if s.strip()]
            
            source = str(row['Source']).strip() if pd.notna(row['Source']) else None
            sub = str(row['SubType']).strip() if pd.notna(row['SubType']) else None
            table_name = str(row['TableName']).strip() if pd.notna(row['TableName']) else None
            dropdown = str(row['DropDown']).strip() if pd.notna(row['DropDown']) else None
            
            cursor.execute(insert_query, (name, json.dumps(skills), source, sub, table_name, dropdown))
        print("✅ SkillSets seeded successfully!")
    except Exception as e:
        print(f"❌ Failed to seed SkillSets: {e}")

    cursor.close()
    conn.close()
    print("\n🎉 Database initialization and rule seeding complete!")

if __name__ == "__main__":
    main()
