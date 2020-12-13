import sqlite3

create_novel = """
create table novel(
    title   char(100)   not null,
    content text        not null,
    primary key(title)
);
"""

create_user = """
create table user(
    user_id     char(50)    not null,
    password    char(50)    not null,
    primary key(user_id)
);
"""

create_upload = """
create table upload(
    user_id char(50)    not null,
    title   char(50)    not null,
    path    char(50)    not null,
    primary key(user_id, title)
);
"""

create_bookmark = """
create table bookmark(
    user_id char(50)    not null,
    local   char(1)     not null,
    title   char(50)    not null,
    page    char(50)    not null,
    primary key(user_id, local, title)
);
"""

conn = sqlite3.connect('Data/data/book_data.db')
cursor = conn.cursor()

cursor.execute(create_novel)
cursor.execute(create_user)
cursor.execute(create_bookmark)
cursor.execute(create_upload)

f = open('Data/book/斗破苍穹.txt', 'r', encoding='utf8')
content = f.read()
title = "斗破苍穹"

cursor.execute("insert into novel(title, content) \
    values('%s', '%s')"%(title, content))

f.close()
f = open('Data/book/龙族.txt', 'r', encoding='utf8')
content = f.read()
title = "龙族"

cursor.execute("insert into novel(title, content) \
    values('%s', '%s')"%(title, content))

conn.commit()
conn.close()