from flask import g

import sqlite3

from idl import app, json
from idl.cache.base import BaseCache

class SQLiteCache(BaseCache):

    def test(self):
        conn = self.get_connection()
        try:
            for row in conn.execute('SELECT * FROM cache LIMIT 1'):
                pass
        except sqlite3.OperationalError:
            sql = 'CREATE TABLE cache (key TEXT PRIMARY KEY, value TEXT)'
            conn.execute(sql)
            for row in conn.execute('SELECT * FROM cache LIMIT 1'):
                pass

    def get_connection(self):
        if not self.disabled:
            return sqlite3.connect(app.config['SQLITE_DB_FILE'])

    def get(self, key):
        if not self.disabled:
            sql = 'SELECT value FROM cache WHERE key=? LIMIT 1'
            result = g.cache_connection.execute(sql, (key,)).fetchone()
            if result:
                return json.loads(result[0])

    def set(self, key, value):
        if not self.disabled:
            sql = 'REPLACE INTO cache VALUES (?, ?)'
            g.cache_connection.execute(sql, (key, json.dumps(value)))
            g.cache_connection.commit()

    def delete(self, key):
        if not self.disabled:
            sql = 'DELETE FROM cache WHERE key = ?'
            g.cache_connection.execute(sql, (key,))
            g.cache_connection.commit()

