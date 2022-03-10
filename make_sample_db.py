import db
import random

ddl = [
"""drop table if exists account;""",
"""drop table if exists project;""",
"""drop table if exists switch;""",
"""drop index if exists account_by_name;""",
"""
create table account (
    id integer primary key autoincrement,
    admin_email_address text,
    account_name text
);
""",
"""
create table project (
    id integer primary key autoincrement,
    description text,
    account_id integer,
    archived text
);
""",
"""
create table switch (
    id integer primary key autoincrement,
    project_id integer,
    switch_type text,
    description text,
    archived text
);
""",
"""
create index account_by_name on account (
    account_name 
);
"""
]

def insert_account(cursor, acct_id, email, name):
    generic_insert(cursor, 'account', ['id','admin_email_address','account_name'], [acct_id, email, name])

def insert_project(cursor, proj_id, description, acct_id, archived):
    generic_insert(cursor, 'project', ['id','description','account_id','archived'], [proj_id, description, acct_id, archived])

def insert_switch(cursor, switch_id, proj_id, sw_type, description, archived):
    generic_insert(cursor, 'switch', ['id','project_id','switch_type','description','archived'], [switch_id, proj_id, sw_type, description, archived])

def generic_insert(cursor, table, flds, values):
    fld_lst = ','.join(flds)
    placeholders = ','.join(['?']*len(flds))
    sql = 'insert into {table} ({fld_lst}) values({placeholders});'.format(table=table, fld_lst=fld_lst, placeholders=placeholders)
    cursor.execute(sql, values)

words = ['fowl', 'rainstorm', 'pocket', 'coil', 'cub', 'noise', 'floor', 'lock', 'airplane', 'school', 'recess', 'home', 'interest', 'lunch', 'brass', 'crate', 'parcel', 'jewel', 'plantation', 'division', 'note', 'rub', 'book', 'pet', 'start', 'grape', 'degree', 'sink', 'cook', 'toes', 'wound', 'voice', 'use', 'increase', 'sack', 'rings', 'sock', 'treatment', 'plants', 'ink', 'card', 'insect', 'trucks', 'friction', 'silk', 'pigs', 'snail', 'middle', 'crown', 'knot', 'flame', 'oatmeal', 'company', 'things', 'pen', 'position', 'grandmother', 'flock', 'reaction', 'class', 'boy', 'square', 'soup', 'twig', 'rock', 'test', 'blade', 'song', 'rose', 'spade', 'rat', 'knife', 'corn', 'mitten', 'frogs', 'achiever', 'transport', 'bear', 'spot', 'chin', 'health', 'shake', 'force', 'aftermath', 'expansion', 'street', 'truck', 'arithmetic', 'wax', 'structure', 'credit', 'dirt', 'beds', 'day', 'bikes', 'stage', 'underwear', 'playground', 'shoe', 'plough']
types = ['flag', 'flagexp', 'exp', 'octopus']

used = set()

def next_id():
    while True:
        next_id = random.randint(1000000,9000000)
        if next_id in used:
            continue
        else:
            break
    used.add(next_id)
    return next_id

def email_address():
    while True:
        addr = random.choice(words) + "@" + random.choice(words) + '.com'
        if addr in used:
            continue
        else:
            break
    used.add(addr)
    return addr

def text(count):
    while True:
        text = " ".join(random.choice(words) for _ in range(count))
        if text in used:
            continue
        else:
            break
    used.add(text)
    return text
    
    
def make_account(conn):
    cursor = conn.cursor()
    acct_id = next_id()
    email = email_address()
    name = text(random.choice([2,3]))
    proj_count = random.randint(10, 100)
    print("making account ", name, "with ", proj_count, " projects")
    insert_account(cursor, acct_id, email, name)
    for i in range(proj_count):
        proj_id = next_id()
        description = text(random.choice([2,3,4]))
        proj_archived = random.choice(['n','n','n','n','y']) # ~80% active   
        print("\tmaking project", description)
        insert_project(cursor, proj_id, description, acct_id, proj_archived)
        switch_count = random.randint(5,100)
        switch_count += random.choice([0,0,0,0,0,0,0,0,0,500]) # 10% of the time make a lot more
        for j in range(random.randint(5, 100)):
            switch_id = next_id()
            switch_type = random.choice(types)
            sw_description = text(random.choice([3,4,5,6]))
            sw_archived = random.choice(['n','n','y']) # ~66% active   
            print("\t\tmaking switch", sw_description)
            insert_switch(cursor, switch_id, proj_id, switch_type, sw_description, sw_archived)
    conn.commit()


conn = db.get_connection()
cursor = conn.cursor()
for stmt in ddl:
    cursor.execute(stmt, [])
conn.commit()

make_account(conn)