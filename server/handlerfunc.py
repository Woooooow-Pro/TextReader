import socket
import sqlite3
import os


database_path = 'Data/data/book_data.db'
WordPerPage = 2000

def register(data):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        table = cursor.execute('select user_id from user')

        user_id = data[1]
        password = data[2]
        flag = True

        for i in table:
            if user_id == i[0]:
                flag = False
                break
            else:
                continue
    
        if flag:
            cursor.execute("insert into user(user_id, password)\
                values('%s', '%s')"%(user_id, password))
        
    return 'Register ' + str(flag) + '\n'


def login(data):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        table = cursor.execute('select user_id, password from user')

        user_id = data[1]
        password = data[2]
        flag = False

        for i in table:
            if user_id == i[0] and password == i[1]:
                flag = True
                break
            else:
                continue

    return 'Login ' + str(flag) + '\n'


def get_title(data):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        title  = data[1]

        if title == '*':
            table = cursor.execute("select title from novel")
        else:
            table = cursor.execute("select title \
                from novel where title like '%%%s%%'"%title)
 
        x = []
        for i in table:
            x.append(i)

        if len(x) <= 0:
            return 'GetTitle ' + str(False) + '\n'
        else:
            ret = 'GetTitle ' + str(True) + '\n'

        for i in x:
            ret = ret + str(i) + '\n'

    return ret


def get_content(data):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        title = data[1]
        page = int(data[2])

        table = cursor.execute("select content \
            from novel where title = '%s'"%title)
        
        x = []
        for i in table:
            x.append(i)
        if len(x) <= 0:
            return 'GetContent ' + str(False) + '\n'
        else:
            ret = 'GetContent ' + str(True) + '\n'
        
        length = len(x[0][0])
        last_page = ((length - 1) // WordPerPage) + 1

        if page <= 1:
            page = 1
        elif page >= last_page:
            page = last_page
        
        ret = ret + str(page) + '\n'
        while len(ret) < 40:
            ret += ' '
        ret = ret + '\n'
        ret = ret + x[0][0][(page - 1) * WordPerPage : page * WordPerPage]
    
    return ret


def get_path(data):
    with sqlite3.connect(database_path) as conn:
        cursor  = conn.cursor()
        user_id = data[1]
        table   = cursor.execute("select title, path \
            from upload where user_id = '%s'"%user_id)

        x = []
        for i in table:
            x.append(i)
        if len(x) <= 0:
            return 'GetPath ' + str(False) + '\n'
        else:
            ret = 'GetPath ' + str(True) + '\n'

        for i in x:
            # 所以不要作死往 title 里面加空格, 空格用 ^ 表示
            ret = ret + str(x[0]) + ' ' + str(x[1]) + '\n'
    return ret


def add_path(data):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        user_id = data[1]
        title   = data[2]
        path    = data[3]

        print('path: ' + path)
        print('user_id: ' + user_id)

        table = cursor.execute("select user_id \
            from user where user_id = '%s'" %user_id)
        x = []
        for i in table:
            x.append(i)
        if len(x) > 0:
            return 'AddPath ' + str(False) + '\n'

        table = cursor.execute("select user_id, title from user")
        for i in table:
            if user_id == i[0] and title == i[1]:
                return 'AddPath ' + str(False) + '\n'

        cursor.execute("insert into upload(user_id, title, path) \
                        values('%s', '%s', '%s')"%(user_id, title, path))

    return 'AddPath ' + str(True) + '\n'
        

def get_record(data):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        user_id = data[1]
        local = data[2]
        title = data[3]

        table = cursor.execute("select page from bookmark \
            where user_id = '%s' \
                and local = '%s' \
                and title = '%s'"
            %(user_id,local,title))

        x = []
        for i in table:
            x.append(i)
        if len(x) <= 0:
            return 'GetRecord ' + str(False) + '\n'
        else:
            ret = 'GetRecord ' + str(True) + '\n'

        for i in x:
            ret = ret + str(i[0]) + '\n'
    return ret


def add_record(data):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        user_id = data[1]
        local   = data[2]
        title   = data[3]
        page    = data[4]
        cursor.execute("delete from bookmark \
            where user_id = '%s' \
                and local = '%s' \
                and title='%s'"%(user_id, local, title))
        conn.commit()
        cursor.execute("insert into bookmark(user_id, local, title, page) \
            values('%s', '%s', '%s', '%s')"%(user_id, local, title, page))
    return 'AddRecord ' + str(True) + '\n'


def get_last_page(data):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        title = data[1]
        table = cursor.execute("select content \
            from novel where title = '%s'"%title)
        
        x = []
        for i in table:
            x.append(i)
        if len(x) <= 0:
            return 'GetLastPage ' + str(False) + '\n'
        else:
            ret = 'GetLastPage ' + str(True) + '\n'
        
        length = len(x[0][0])
        last_page = ((length - 1) // WordPerPage) + 1
        ret = ret + str(last_page) + '\n'

    return ret


def delete_path(data):
    with sqlite3.connect(database_path) as conn:
        cursor = conn.cursor()
        user_id = data[1]
        title   = data[2]
        cursor.execute("delete from upload \
            where user_id = '%s' and title = '%s'"%(user_id, title))
        cursor.execute("delete from bookmark \
            where user_id = '%s' and local = '0' \
                and title = '%s'"%(user_id, title))
    return 'DeletePath ' + str(True) + '\n'
