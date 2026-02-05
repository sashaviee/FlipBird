# database.py
import sqlite3
import datetime
import json
from pathlib import Path


class GameDatabase:
    def __init__(self, db_path="game_data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Таблица рекордов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT,
                score INTEGER,
                level INTEGER,
                date TIMESTAMP
            )
        ''')

        # Таблица настроек
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        # Таблица статистики
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                games_played INTEGER DEFAULT 0,
                total_score INTEGER DEFAULT 0,
                best_score INTEGER DEFAULT 0,
                last_played TIMESTAMP
            )
        ''')

        conn.commit()
        conn.close()

    def save_score(self, player_name, score, level):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO scores (player_name, score, level, date)
            VALUES (?, ?, ?, ?)
        ''', (player_name, score, level, datetime.datetime.now()))

        # Обновляем статистику
        cursor.execute('''
            INSERT OR REPLACE INTO statistics (id, games_played, total_score, best_score, last_played)
            VALUES (
                1,
                COALESCE((SELECT games_played FROM statistics WHERE id=1), 0) + 1,
                COALESCE((SELECT total_score FROM statistics WHERE id=1), 0) + score,
                MAX(COALESCE((SELECT best_score FROM statistics WHERE id=1), 0), ?),
                ?
            )
        ''', (score, datetime.datetime.now()))

        conn.commit()
        conn.close()

    def get_high_scores(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT player_name, score, level, date
            FROM scores
            ORDER BY score DESC, date DESC
            LIMIT ?
        ''', (limit,))

        scores = cursor.fetchall()
        conn.close()
        return scores

    def get_statistics(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM statistics WHERE id=1')
        stats = cursor.fetchone()
        conn.close()

        if stats:
            return {
                'games_played': stats[1],
                'total_score': stats[2],
                'best_score': stats[3],
                'last_played': stats[4]
            }
        return None

    def save_setting(self, key, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value)
            VALUES (?, ?)
        ''', (key, json.dumps(value)))

        conn.commit()
        conn.close()

    def load_setting(self, key, default=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT value FROM settings WHERE key=?', (key,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return json.loads(result[0])
        return default

    def export_to_csv(self, filename="game_data.csv"):
        import csv

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Экспорт рекордов
        cursor.execute('SELECT * FROM scores')
        scores = cursor.fetchall()

        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Player', 'Score', 'Level', 'Date'])
            writer.writerows(scores)

        conn.close()
        return len(scores)