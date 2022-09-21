import sqlite3
from datetime import datetime
import time

class Account:

    def __init__(self,path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS account(PhoneNumber TEXT,api_id INTEGER,api_hash TEXT,
        report TEXT,DeletedAccount TEXT,JoinTime TEXT,
        LastAdd TEXT, LastActivity TEXT, SuccessfulAdds INTEGER, UnSuccessfulAdds INTEGER , Adds INTEGER)''')
        self.con.commit()

    def insert_data(self,entities):
        self.cur.execute('''INSERT INTO account(PhoneNumber,api_id,api_hash,report,DeletedAccount,
        JoinTime,LastAdd,LastActivity,SuccessfulAdds,UnSuccessfulAdds,Adds) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', entities)
        self.con.commit()

    def update_report(self,update):
        self.cur.execute("UPDATE account SET report = ? WHERE PhoneNumber = ?;", (update[0],update[1]))
        self.con.commit()

    def update_delete(self,update):
        self.cur.execute("UPDATE account SET DeletedAccount= ? WHERE PhoneNumber= ?;", (update[0],update[1]))
        self.con.commit()
    
    def delete_account(self,update):
        self.cur.execute("DELETE FROM account WHERE PhoneNumber = ?;",(update))
        self.con.commit()
        
    def update_Adds_Successful_UnSuccessful(self,update):
        self.cur.execute("UPDATE account SET SuccessfulAdds=? ,UnSuccessfulAdds=? ,Adds=?  WHERE PhoneNumber=?;", (update[0],update[1],update[2],update[3]))
        self.con.commit()

    def update_LastAdd_LastActivity(self,update):
        self.cur.execute("UPDATE account SET LastAdd=?, LastActivity=?  WHERE PhoneNumber= ?;", (update[0],update[1]))
        self.con.commit()
    
    def update_account(self,update):
        self.cur.execute("UPDATE account SET LastAdd=?, LastActivity=?, SuccessfulAdds=?, UnSuccessfulAdds=? ,Adds=?  WHERE PhoneNumber= ?;", (update[0],update[1],update[2],update[3],update[4],update[5]))
        self.con.commit()

    def get_list_phone(self):
        List_chatid = list()
        self.cur.execute('SELECT PhoneNumber FROM account')
        rows = self.cur.fetchall()
        for id in rows:
            List_chatid.append(id[0])
        return List_chatid

    def get_list_phone_Activity(self):
        list_noActivity = list()
        self.cur.execute("SELECT PhoneNumber,LastAdd,LastActivity FROM account WHERE report = 'False' AND DeletedAccount= 'False'")
        rows = self.cur.fetchall()
        for id in rows:
            list_noActivity.append(id)
        return list_noActivity

    def get_list_healthy_account(self):
        list_healthy_account = list()
        self.cur.execute("SELECT report FROM account WHERE report = 'False' AND DeletedAccount= 'False'")
        rows = self.cur.fetchall()
        for id in rows:
            list_healthy_account.append(id[0])
        return list_healthy_account
    
    def get_list_deleted_account(self):
        list_deleted_account = list()
        self.cur.execute("SELECT DeletedAccount FROM account WHERE DeletedAccount = 'True' ")
        rows = self.cur.fetchall()
        for id in rows:
            list_deleted_account.append(id[0])
        return list_deleted_account
    
    def get_list_Temporary_report(self):
        list_Temporary_report = list()
        self.cur.execute("SELECT report FROM account WHERE NOT report= 'False' AND NOT report= 'True' AND DeletedAccount = 'False'")
        rows = self.cur.fetchall()
        for id in rows:
            list_Temporary_report.append(id[0])
        return list_Temporary_report
    
    def get_list_Permanent_report(self):
        list_Permanent_report = list()
        self.cur.execute("SELECT report FROM account WHERE report= 'True' ")
        rows = self.cur.fetchall()
        for id in rows:
            list_Permanent_report.append(id[0])
        return list_Permanent_report

    def get_SuccessfulAdds_UnSuccessfulAdds_Adds(self,update):
        list_SuccessfulAdds_UnSuccessfulAdds_Adds = list()
        self.cur.execute("SELECT SuccessfulAdds , UnSuccessfulAdds , Adds FROM account WHERE PhoneNumber = ?;",(update))
        rows = self.cur.fetchall()
        for id in rows:
            list_SuccessfulAdds_UnSuccessfulAdds_Adds.append(id)
        return list_SuccessfulAdds_UnSuccessfulAdds_Adds


    def close(self):
        self.con.close()


class Username:

    def __init__(self,path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS username(User TEXT,chat_id TEXT)')
        self.con.commit()

    def insert_data(self,entities):
        self.cur.execute('INSERT INTO username(User,chat_id) VALUES (?,?)', entities)
        self.con.commit()
    
    def delete_username(self,update):
        self.cur.execute("DELETE FROM username WHERE User = ?;",(update))
        self.con.commit()
    
    def delete_all_username(self):
        self.cur.execute("DELETE FROM username;")
        self.con.commit()

    def get_list_username(self):
        List_username = list()
        self.cur.execute("SELECT User FROM username;")
        rows = self.cur.fetchall()
        for id in rows:
            List_username.append(id[0])
        return List_username
    
    def get_list_All(self):
        List_username = list()
        self.cur.execute("SELECT *FROM username;")
        rows = self.cur.fetchall()
        for id in rows:
            List_username.append(id[0])
        return List_username 
    
    def get_list_chat_id(self):
        List_chat_id = list()
        self.cur.execute("SELECT chat_id FROM username;")
        rows = self.cur.fetchall()
        for id in rows:
            List_chat_id.append(id[0])
        return List_chat_id

    def close(self):
        self.con.close()


class AdminsBot:

    def __init__(self,path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS admins(name TEXT,chat_id TEXT,username Text)')
        self.con.commit()

    def insert_data(self,entities):
        self.cur.execute("INSERT INTO admins(name,chat_id,username) VALUES (?,?,?)", entities)
        self.con.commit()
    
    def delete_admin(self,update):
        self.cur.execute("DELETE FROM admins WHERE chat_id = ?;",(update))
        self.con.commit()

    def get_list_admins(self):
        List_admins = list()
        self.cur.execute("SELECT *FROM admins;")
        rows = self.cur.fetchall()
        for id in rows:
            List_admins.append(id)
        return List_admins

    def close(self):
        self.con.close()


class Groups:

    def __init__(self,path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS groups(name TEXT,chat_id TEXT,username Text)')
        self.con.commit()

    def insert_data(self,entities):
        self.cur.execute("INSERT INTO groups(name,chat_id,username) VALUES (?,?,?)", entities)
        self.con.commit()
    
    def delete_group(self,update):
        self.cur.execute("DELETE FROM groups WHERE chat_id = ?;",(update))
        self.con.commit()

    def get_list_groups(self):
        List_groups = list()
        self.cur.execute("SELECT *FROM groups;")
        rows = self.cur.fetchall()
        for id in rows:
            List_groups.append(id)
        return List_groups

    def get_list_username_groups(self,update):
        List_groups = list()
        self.cur.execute("SELECT username FROM groups WHERE chat_id= ?;",(update))
        rows = self.cur.fetchall()
        for id in rows:
            List_groups.append(id[0])
        return List_groups
 
    def close(self):
        self.con.close()


class AddStatistics:

    def __init__(self,path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS addstatistics(PercentAddsSuccessful TEXT,LastAdd TEXT,LastActivity TEXT,AddToday TEXT,RequestedAdditions TEXT,Adds TEXT)')
        self.con.commit()

    def insert_data(self,entities):
        self.cur.execute('INSERT INTO addstatistics(PercentAddsSuccessful, LastAdd, LastActivity, AddToday, RequestedAdditions, Adds) VALUES(?, ?, ?, ?, ?, ?)', entities)
        self.con.commit()

    def update_data(self,update):
        self.cur.execute('''UPDATE addstatistics SET PercentAddsSuccessful= ?,  LastAdd= ?,  LastActivity= ?, 
        AddToday= ?,  RequestedAdditions= ?,  Adds=?;''', (update[0],update[1],update[2],update[3],update[4],update[5]))
        self.con.commit()

    def get_list_Statistics(self):
        List_chatid = list()
        self.cur.execute('SELECT *FROM addstatistics')
        rows = self.cur.fetchall()
        for id in rows:
            List_chatid.append(id)
        return List_chatid

    def close(self):
        self.con.close()


class SettingAddmember:

    def __init__(self,path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def create_table(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS settingadd(id INTEGER,ActivityRange TEXT,AddRange TEXT)')
        self.con.commit()

    def insert_data(self,entities):
        self.cur.execute('INSERT INTO settingadd(id,ActivityRange, AddRange) VALUES(?, ?, ?)', entities)
        self.con.commit()

    def update_data(self,update):
        self.cur.execute('''UPDATE settingadd SET ActivityRange= ?, AddRange= ? WHERE id = 1 ;''', (update[0],update[1]))
        self.con.commit()

    def get_list_Setting(self):
        List_SettingAdd = list()
        self.cur.execute('SELECT *FROM settingadd')
        rows = self.cur.fetchall()
        for id in rows:
            List_SettingAdd.append(id)
        return List_SettingAdd

    def close(self):
        self.con.close()


class DateTime:

    def __init__(self):
        current_time = time.localtime()
        self.d = time.strftime("%d-%m-%Y",current_time)
        self.t = time.strftime("%H:%M:%S",current_time)
    
    def time (self):
        return self.t

    def date (self):
        return self.d
   
