import decimal
from flask import Flask, request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
import pymysql
from collections import OrderedDict
import json
from sqlalchemy import func
import os
import time
from flask import Blueprint, render_template, request, jsonify
from collections import OrderedDict
from app import db
import json

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
        print(result_sql)
        print(User)
        print(Password)
        if result_sql == []:
            return '用户名不存在'
        else:
            if result_sql[0][1] != Password:
                return '密码错误'
            else:
                return '密码正确'


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
            return '增加成功'
        else:
            return '存在该用户，增加失败'


@log.route('/change', methods=['POST'])
def log_change():
    if request.method == 'POST':
        User = request.form.get('User')
        Password_old = request.form.get('Password_old')
        Password_new = request.form.get('Password_new')
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
            return '用戶名不存在'
        else:
            if result_sql[0][1] != Password_old:
                return '密码输入错误，修改失败'
            else:
                sql = "UPDATE `user_inf` SET `Password`=\'" + \
                    Password_new + '\' WHERE (`User`=\''+User+'\')'
                db.session.execute(sql)
                db.session.commit()
                return '修改成功'
