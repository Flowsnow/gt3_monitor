#!/usr/bin/env python  
# encoding: utf-8  

"""
Created on 5/25/17 3:09 PM
@author: Flowsnow
@file: handle.py 
@function: core service:handle
"""
import cx_Oracle
import os
import sys
import hashlib
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import configparser
import logging


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s [%(threadName)s] %(message)s',
                    filename='gt3_app.log', filemode='a')


class PasswordCrypto(object):
    def __init__(self, cfg):
        key = 'servyou_password_key'
        self.key = hashlib.md5(key).hexdigest()
        self.mode = AES.MODE_CBC
        self.salt = b'0000000101000000'
        self.cfg = cfg

    def encrypt(self, text):
        cipher = AES.new(self.key, self.mode, self.salt)
        n_text = text + ('\0' * (16-(len(text) % 16)))
        return b2a_hex(cipher.encrypt(n_text))

    def decrypt(self, text):
        cipher = AES.new(self.key, self.mode, self.salt)
        return cipher.decrypt(a2b_hex(text)).rstrip('\0')

    def __call__(self, flag, env, text):
        if flag == '1':
            password = self.decrypt(text)
            return password
        else:
            password_text = self.encrypt(text)
            self.cfg.set(env, 'password', password_text)
            self.cfg.set(env, 'flag', '1')
            self.cfg.write(open('config.ini', 'w'))
            return text


class FilesHandler:
    def __init__(self, e, cfg):
        self.excel = e
        self.cfg = cfg

        self.data_path = self.cfg.get('basic', 'data_path')
        self.file_path = self.data_path + '/file'
        self.bak_path = self.data_path + '/bak'

    def handle_cpu(self, cfg_file, ip):
        logging.info('handle {}.log : acquire cpu info'.format(ip))
        try:
            options = cfg_file.options('cpujc')
            args = [cfg_file.get('cpujc', o) for o in options]
            args.insert(0, ip)
            self.excel.cpu_sheet.insert(*args)
        except Exception:
            print('section cpujc has error')

    def handle_memory(self, cfg_file, ip):
        logging.info('handle {}.log : acquire memory info'.format(ip))
        options = cfg_file.options('freejc')
        args = [cfg_file.get('freejc', o) for o in options]
        args.insert(0, ip)
        self.excel.memory_sheet.insert(*args)

    def handle_file_system(self, cfg_file, ip):
        logging.info('handle {}.log : acquire file system info'.format(ip))
        options = cfg_file.options('dfhpjc')
        file_systems = filter(lambda x: '.' not in x, options)
        for system in file_systems:
            keys = filter(lambda x: '{}.'.format(system) in x, options)
            keys.insert(0, system)
            args = [cfg_file.get('dfhpjc', key) for key in keys]
            args.insert(0, ip)
            self.excel.disk_use_sheet.insert(*args)

    def handle_busy(self, cfg_file, ip):
        logging.info('handle {}.log : acquire disk busy info'.format(ip))
        options = cfg_file.options('sardjc')
        disks = set([option.partition('.')[0] for option in options])
        for disk in disks:
            keys = filter(lambda x: x.partition('.')[0] == disk, options)
            args = [cfg_file.get('sardjc', key) for key in keys]
            args.insert(0, disk)
            args.insert(0, ip)
            self.excel.disk_busy_sheet.insert(*args)

    def handle_alert(self, cfg_file, ip):
        logging.info('handle {}.log : acquire alert log info'.format(ip))
        if cfg_file.has_section('alertjc'):
            options = cfg_file.options('alertjc')
            if options:
                errors = [cfg_file.get('alertjc', o) for o in options]
                error_str = ' , '.join(errors)
                args = [ip, 'Y', error_str]
                self.excel.alert_sheet.insert(*args)
            else:
                args = [ip, 'N', '']
                self.excel.alert_sheet.insert(*args)
        else:
            # is not database server, don't handle
            pass

    def handle_ogg(self, cfg_file, ip):
        logging.info('handle {}.log : acquire ogg info'.format(ip))
        if cfg_file.has_section('oggjc'):
            options = cfg_file.options('oggjc')
            if options:
                processes = filter(lambda x: '.' not in x, options)
                for process in processes:
                    keys = filter(lambda x: '{}.'.format(process) in x, options)
                    keys.insert(0, process)
                    args = [cfg_file.get('oggjc', key) for key in keys]
                    args.insert(0, ip)
                    args.append('')
                    self.excel.ogg_sheet.insert(*args)
            else:
                pass
        else:
            # is not ogg server, don't handle
            pass

    def handle_file(self, f):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        ip = f[:-4]
        logging.info('starting to handle {}.log'.format(ip))
        cfg_file = configparser.ConfigParser()
        cfg_file.read('{}/{}'.format(self.file_path, f))
        self.handle_cpu(cfg_file, ip)
        self.handle_memory(cfg_file, ip)
        self.handle_file_system(cfg_file, ip)
        self.handle_busy(cfg_file, ip)
        self.handle_alert(cfg_file, ip)
        self.handle_ogg(cfg_file, ip)
        logging.info('handle {}.log finished'.format(ip))

    def run(self):
        if not os.path.exists(self.data_path):
            raise IOError('{} not exists'.format(self.data_path))
        for f in os.listdir(self.file_path):
            self.handle_file(f)


class DatabasesHandler:
    def __init__(self, e, cfg):
        self.cfg = cfg
        self.excel = e

    @staticmethod
    def query(sql, db):
        cur = db.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result

    def handle_tablespace(self, sheet, db):
        sql = """SELECT K.NAME DBNAME,
       UPPER(F.TABLESPACE_NAME),
       to_char(D.TOT_GROOTTE_MB / 1024),
       to_char(D.sjwjdx),
       TO_CHAR((D.TOT_GROOTTE_MB - F.TOTAL_BYTES) / 1024),
       TO_CHAR(ROUND((D.TOT_GROOTTE_MB - F.TOTAL_BYTES) / D.TOT_GROOTTE_MB * 100,
                     2),
               '990.99') as usage,
       to_char(F.TOTAL_BYTES)
  FROM (SELECT TABLESPACE_NAME,
               ROUND(SUM(BYTES) / (1024 * 1024), 2) TOTAL_BYTES,
               ROUND(MAX(BYTES) / (1024 * 1024), 2) MAX_BYTES
          FROM SYS.DBA_FREE_SPACE
         GROUP BY TABLESPACE_NAME) F,
       (SELECT DD.TABLESPACE_NAME,
               ROUND(SUM(DD.BYTES) / (1024 * 1024), 2) TOT_GROOTTE_MB,
               count(1) * 32 as sjwjdx
          FROM SYS.DBA_DATA_FILES DD
         GROUP BY DD.TABLESPACE_NAME) D,
       v$database K
 WHERE D.TABLESPACE_NAME = F.TABLESPACE_NAME
 order by usage desc"""
        result = self.query(sql, db)
        for row in result:
            sheet.insert(*row)

    def handle_archive(self, sheet, db, diskgroup):
        sql = """select d.NAME,
       d.LOG_MODE,
       decode(d.log_mode,
              'ARCHIVELOG',
              (select t.TOTAL_MB from v$asm_diskgroup t where t.NAME = '{0}'),
              'NOARCHIVELOG',
              0),
       decode(d.log_mode,
              'ARCHIVELOG',
              (select t.TOTAL_MB - t.FREE_MB
                 from v$asm_diskgroup t
                where t.NAME = '{0}'),
              'NOARCHIVELOG',
              0),
       decode(d.log_mode,
              'ARCHIVELOG',
              (select t.FREE_MB from v$asm_diskgroup t where t.NAME = '{0}'),
              'NOARCHIVELOG',
              0)
  from v$database d
""".format(diskgroup)
        result = self.query(sql, db)
        for row in result:
            sheet.insert(*row)

    def handle_lock(self, sheet, db):
        sql = """with ltr as
 (select d.NAME DBNAME,
         to_char(sysdate, 'YYYYMMDDHH24MISS') TM,
         s.sid,
         s.sql_id,
         s.sql_child_number,
         s.prev_sql_id,
         xid,
         to_char(t.start_date, 'YYYYMMDDHH24MISS') start_time,
         e.TYPE,
         e.block,
         e.ctime,
         decode(e.CTIME, 0, (sysdate - t.start_date) * 3600 * 24, e.ctime) el_second
    from v$transaction t, v$session s, v$transaction_enqueue e, v$database d
   where t.start_date <= sysdate - interval '1000' second
     and t.addr = s.taddr
     and t.addr = e.addr(+))
select ltr.*,
       (select q1.sql_text
          from v$sql q1
         where ltr.prev_sql_id = q1.sql_id(+)
           and rownum = 1) prev_sql_text,
       (select q1.sql_text
          from v$sql q1
         where ltr.sql_id = q1.sql_id(+)
           and ltr.sql_child_number = q1.CHILD_NUMBER(+)) sql_text
  from ltr ltr
"""
        result = self.query(sql, db)
        for row in result:
            sheet.insert(*row)

    def run(self):
        if not self.cfg.has_option('basic', 'db_env'):
            return
        db_env = self.cfg.get('basic', 'db_env')
        for env in db_env.split(','):
            env = env.strip()
            username = self.cfg.get(env, 'username')
            password = self.cfg.get(env, 'password')
            url = self.cfg.get(env, 'url')
            diskgroup = self.cfg.get(env, 'diskgroup')
            flag = self.cfg.get(env, 'flag')
            pc = PasswordCrypto(self.cfg)
            logging.info('{}@{} : acquire password from config.ini'.format(username, url))
            password = pc(flag, env, password)
            logging.info('{}@{} : connect'.format(username, url))
            db = cx_Oracle.connect(username, password, url)
            logging.info('{}@{} : query tablespace'.format(username, url))
            self.handle_tablespace(self.excel.tablespace_sheet, db)
            logging.info('{}@{} : query database lock'.format(username, url))
            self.handle_lock(self.excel.db_lock_sheet, db)
            logging.info('{}@{} : query archive diskgroup'.format(username, url))
            self.handle_archive(self.excel.archive_sheet, db, diskgroup)
