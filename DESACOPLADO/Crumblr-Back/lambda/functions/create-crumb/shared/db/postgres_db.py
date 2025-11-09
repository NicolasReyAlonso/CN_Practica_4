import psycopg2
import psycopg2.extras
import json
from typing import List, Optional
from shared.db.db import Database
from shared.models.crumb import Crumb
import os

class PostgresDatabase(Database):
    
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        self.connection.autocommit = True
        self.initialize()
    
    def initialize(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS crumbs (
                    crumb_id VARCHAR(36) PRIMARY KEY,
                    content TEXT NOT NULL,
                    image_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def create_crumb(self, crumb: Crumb) -> Crumb:
        with self.connection.cursor() as cursor:
            sql = """
                INSERT INTO crumbs (crumb_id, content, image_url, created_at)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (crumb.crumb_id, crumb.content, crumb.image_url, crumb.created_at))
        return crumb


    def get_crumb(self, crumb_id: str) -> Optional[Crumb]:
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            sql = "SELECT * FROM crumbs WHERE crumb_id = %s"
            cursor.execute(sql, (crumb_id,))
            result = cursor.fetchone()
            if result:
                result = dict(result)
                result['created_at'] = (
                    result['created_at'].isoformat() if result['created_at'] else None
                )
                return Crumb(**result)
        return None

    
    def get_all_crumbs(self):
        with self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            sql = "SELECT * FROM crumbs ORDER BY created_at DESC"
            cursor.execute(sql)
            results = cursor.fetchall()
            return [Crumb(**row) for row in results]

    
    def update_crumb(self, crumb_id: str, crumb: Crumb) -> Optional[Crumb]:
        with self.connection.cursor() as cursor:
            sql = """
                UPDATE crumbs
                SET content = %s,
                    image_url = %s,
                    created_at = created_at
                WHERE crumb_id = %s
            """
            cursor.execute(sql, (crumb.content, crumb.image_url, crumb_id))
            if cursor.rowcount > 0:
                return self.get_crumb(crumb_id)
        return None

    def delete_crumb(self, crumb_id: str) -> bool:
        with self.connection.cursor() as cursor:
            sql = "DELETE FROM crumbs WHERE crumb_id = %s"
            cursor.execute(sql, (crumb_id,))
            return cursor.rowcount > 0