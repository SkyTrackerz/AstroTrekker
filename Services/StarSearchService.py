from skyfield.api import load
import pandas as pd
import sqlite3
from typing import List


class StarSearchService:
    def __init__(self, hipparcos_file: str, ephemeris_file: str):
        # Load the ephemeris file
        self.eph = load(ephemeris_file)

        # Load Hipparcos data into DataFrame
        self.hip_df = pd.read_csv(hipparcos_file)

        # Initialize SQLite database
        self.init_database()

    def init_database(self):
        """Initialize SQLite database with star data"""
        conn = sqlite3.connect('stars.db')

        # Create tables
        conn.execute('''
        CREATE TABLE IF NOT EXISTS stars (
            hip_id INTEGER PRIMARY KEY,
            proper_name TEXT,
            magnitude REAL
        )
        ''')

        # Index for faster prefix searches
        conn.execute('CREATE INDEX IF NOT EXISTS idx_proper_name ON stars(proper_name)')

        # Insert data from DataFrame
        self.hip_df.to_sql('stars', conn, if_exists='replace', index=False)
        conn.close()

    def search_stars(self, prefix: str, limit: int = 10) -> List[dict]:
        """Search for stars by name prefix"""
        conn = sqlite3.connect('stars.db')
        cursor = conn.cursor()

        # Search for stars matching prefix
        query = """
        SELECT hip_id, proper_name, magnitude 
        FROM stars 
        WHERE proper_name LIKE ? || '%'
        ORDER BY magnitude ASC
        LIMIT ?
        """

        results = cursor.execute(query, (prefix.upper(), limit)).fetchall()
        conn.close()

        return [
            {
                'id': row[0],
                'name': row[1],
                'magnitude': row[2]
            }
            for row in results
        ]

    def search_solar_system(self, prefix: str) -> List[str]:
        """Search for solar system bodies by prefix"""
        # Get list of available bodies from ephemeris
        bodies = [name for name in self.eph.names()
                  if name.lower().startswith(prefix.lower())]
        return bodies