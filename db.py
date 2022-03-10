import sqlite3
import os
from sqlite3.dbapi2 import Cursor

def get_connection():
    conn_str = os.getenv('DB_CONN_STR')
    if not conn_str:
        conn_str = os.path.join(os.path.dirname(__file__), "db.sqlite3")
    conn =  sqlite3.connect(conn_str)
    conn.row_factory = sqlite3.Row
    return conn

def get_projects(conn):
    sql = """select p.id, p.description, p.account_id, p.archived
    from project p;"""
    cursor = conn.execute(sql, [])
    rows = cursor.fetchall()
    out = {}
    for row in rows:
        rec = {}
        rec['id'] = int(row['id'])
        rec['description'] = row['description']
        rec['account_id'] = int(row['account_id'])
        rec['archived'] = row['archived']
        rec['url'] = "/project/" + str(row['id'])
        out[rec['id']] = rec
    return out

def get_switches_by_project(conn, project_id):
    sql = """select sw.id, sw.description 
    from switch sw
    where sw.project_id = ?
    and archived = 'n';"""
    cursor = conn.execute(sql, [project_id])
    rows = cursor.fetchall()
    out = {}
    out[project_id] = {}
    for row in rows:
        rec = {}
        rec['id'] = int(row['id'])
        rec['description'] = row['description']
        out[project_id][rec['id']] = rec
    return out

def get_summary_by_project(conn, project_id):
    sql = """select p.id, p.description, p.account_id, p.archived, s.switch_type, count(s.switch_type) as cnt 
from project p
left join switch s on (p.id = s.project_id) 
where s.project_id = ?
group by s.switch_type;"""
    cursor = conn.execute(sql, [project_id])
    rows = cursor.fetchall()
    out = {}
    row = rows[0]
    rec = {}
    rec['id'] = int(row['id'])
    rec['description'] = row['description']
    rec['account_id'] = int(row['account_id'])
    rec['archived'] = row['archived']
    rec['url'] = "/project/" + str(row['id'])
    summary = {}
    rec['summary'] = summary
    for row in rows:
      summary[row['switch_type']] = row['cnt']
 
    out[project_id] = rec
    return out
