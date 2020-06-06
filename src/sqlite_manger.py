# -*- coding: utf-8 -*-

import sqlite3


class SQLManage:
    def __init__(self, basedate):
        self.db = sqlite3.connect(basedate, check_same_thread=False)
        self.cursor = self.db.cursor()

    def user_exists(self, user_id):
        cursor = self.db.cursor()
        with self.db:
            res = self.cursor.execute(f"SELECT status FROM bot WHERE user_id = {user_id}").fetchall()
            return bool(len(res))

    def add_user(self, user_id, status='False'):
        cursor = self.db.cursor()
        with self.db:
            return cursor.execute('INSERT INTO `bot` (`user_id`, `status`) VALUES (?, ?)', (user_id, status)).fetchall()

    def check_status(self, user_id):
        cursor = self.db.cursor()
        with self.db:
            return cursor.execute(f"SELECT status FROM bot WHERE user_id = {user_id}").fetchall()

    def status_on(self, user_id):
        cursor = self.db.cursor()
        with self.db:
            command = f"""
            UPDATE bot
            SET status = 'True'
            WHERE user_id = {user_id}
            """
            return cursor.execute(command).fetchall()

    def status_off(self, user_id):
        cursor = self.db.cursor()
        with self.db:
            command = f"""
            UPDATE bot
            SET status = 'False'
            WHERE user_id = {user_id}
            """
            return cursor.execute(command).fetchall()

    def get_all_id(self):
        cursor = self.db.cursor()
        with self.db:
            return cursor.execute('SELECT user_id FROM bot').fetchall()

    def close(self):
        self.db.close()