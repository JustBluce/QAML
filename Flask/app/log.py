#Cai
import sys
sys.path.append("..")
sys.path.insert(0, './app')
from app import import_libraries, util
from import_libraries import *
log = Blueprint('log', __name__)


@log.route('/in', methods=['POST'])
def log_in():
    if request.method == 'POST':
        User = request.form.get('User')
        Password = request.form.get('Password')
        sql = '''SELECT
user_inf.`User`,
user_inf.`Password`
FROM
user_inf
WHERE
user_inf.`User` = \''''+User+"'"
        result_sql = db.session.execute(sql)
        result_sql = result_sql.fetchall()
        # print(result_sql)
        # print(User)
        # print(Password)
        if result_sql == []:
            return 'User does not exist'
        else:
            if result_sql[0][1] != Password:
                return 'Incorrect password'
            else:
                return 'Correct password'


@log.route('/add', methods=['POST'])
def log_add():
    if request.method == 'POST':
        User = request.form.get('User')
        Password = request.form.get('Password')
        # 先要判断
        sql = '''SELECT
        user_inf.`User`,
        user_inf.`Password`
        FROM
        user_inf
        WHERE
        user_inf.`User` = \'''' + User + "'"
        result_sql = db.session.execute(sql)
        result_sql = result_sql.fetchall()
        if result_sql == []:
            sql = 'INSERT INTO `user_inf` (`User`, `Password`) VALUES (\'' + \
                User + '\',\'' + Password + '\')'
            db.session.execute(sql)
            return 'Successfully add new user'
        else:
            return 'The user already exists'


@log.route('/change', methods=['POST'])
def log_change():
    if request.method == 'POST':
        User = request.form.get('User')
        Password_old = request.form.get('Password_old')
        Password_new = request.form.get('Password_new')
        # Judge
        sql = '''SELECT
        user_inf.`User`,
        user_inf.`Password`
        FROM
        user_inf
        WHERE
        user_inf.`User` = \'''' + User + "'"
        result_sql = db.session.execute(sql)
        result_sql = result_sql.fetchall()
        if result_sql == []:
            return 'User does not exist'
        else:
            if result_sql[0][1] != Password_old:
                return 'Password input error, change failed'
            else:
                sql = "UPDATE `user_inf` SET `Password`=\'" + \
                    Password_new + '\' WHERE (`User`=\''+User+'\')'
                db.session.execute(sql)
                db.session.commit()
                return 'Successfully changed'