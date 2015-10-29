import sqlite3
from datetime import datetime

class dbMaster:

  def __init__(self):
    print("control start")
    self.con = sqlite3.connect('data.db')

  def create(self, userid, password, email, name, dob):
    try:
      cur = self.con.cursor()
      cur.execute("INSERT INTO USR (userid, password, email, name, dob) VALUES (?, ?, ?, ?, ?)" (userid, password, email, name, dob))
      self.con.commit()

    except sqlite3.IntegrityError:
      print '\tUser already exists'
      return False
    return True

  def login(self, username, password):
    cur = self.con.cursor()    
    cur.execute("SELECT * FROM USR where userId=? and password=?", (username,password))

    row = cur.fetchone()
    
    result = {}
    
    if row != None:
      result['success'] = True
      result['username'] = row[0]
      result['email'] = row[2]
      result['name'] = row[3]
      result['dob'] = row[4]
    else:
      result['success'] = False
      
    return result
    
  def logout(self, username):
    pass
    
  def changePassword(self, username,  oldPassword, newPassword):
    cur = self.con.cursor()
    cur.execute("UPDATE USR set password=? where userId=? and password=?", (newPassword, username, oldPassword))
    self.con.commit()

    if cur.rowcount > 0:
      return True
    else:
      return False
    
  def search(self, name):
    # TODO: add connection status to these results?
    cur = self.con.cursor()    
    cur.execute("""
    SELECT * FROM USR 
    where name LIKE ?
    """, ('%' + name + '%',))
    rows = cur.fetchall()
    
    users = []
    
    for row in rows:
      user = {}
      user['username'] = row[0]
      user['name'] = row[3]

      users.append(user)
    
    return users
    
  def connect(self, username, friendname):
    try:
      cur = self.con.cursor()
      cur.execute("""
      INSERT INTO CONNECTION_USR 
      (userid, connectionId, status)
      VALUES (?, ?, ?)
      """, (username, friendname, "Request"))
      self.con.commit()
    except sqlite3.Integrityerror:
      print '\tFailed to connect'
      return False
    
    return True
    
  def connectionReject(self, username, connectionId):
    print("attempt connect reject " + username + ':' + connectionId)
    
    cur = self.con.cursor()
    cur.execute("""
    UPDATE CONNECTION_USR
    SET status=?
    WHERE userId=? and connectionId=?
    """, ("Reject", username, connectionId))
    self.con.commit()

    if cur.rowcount > 0:
      return True
    else:
      return False
    
  def connectionAccept(self, username, connectionId):
    print("attempt connect accept " + username + ':' + connectionId)

    cur = self.con.cursor()
    cur.execute("""
    UPDATE CONNECTION_USR
    SET status=?
    WHERE userId=? and connectionId=?
    """, ("Accept", username, connectionId))
    self.con.commit()

    if cur.rowcount > 0:
      return True
    else:
      return False
    
  def connectionList(self, username):
    cur = self.con.cursor()    
    cur.execute("""
    SELECT u.userId, u.name, c.status
    FROM CONNECTION_USR as c, USR as u 
    where 
    (c.userId = ? and c.connectionId = u.userId)
    or
    (c.userId = u.userId and c.connectionId = ?)
    """, (username,username))
    rows = cur.fetchall()
    
    users = []
    
    for row in rows:
      user = {}
      user['username'] = row[0]
      user['name'] = row[1]
      user['status'] = row[2]

      users.append(user)
    
    return users
    
  def connectionRequests(self, username):
    cur = self.con.cursor()    
    cur.execute("""
    SELECT u.userId, u.name, c.status
    FROM CONNECTION_USR as c, USR as u 
    where 
    c.userId = ?
    and 
    c.connectionId = u.userId
    and
    c.status = 'Request'
    """, (username,))
    rows = cur.fetchall()
    
    users = []
    
    for row in rows:
      user = {}
      user['username'] = row[0]
      user['name'] = row[1]
      user['status'] = row[2]

      users.append(user)
    
    return users
    
  def messageSend(self, senderId, receiverId, contents):
    ts = datetime.now()
    deleteStatus = 0
    cur = self.con.cursor()
    cur.execute("""
    INSERT INTO MESSAGE (senderId, receiverId, contents, sendTime, deleteStatus, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (senderId, receiverId, contents, ts, deleteStatus, "Sent"))
    self.con.commit()

    if cur.rowcount > 0:
      return True
    else:
      return False
    
  def messageList(self, username):
    cur = self.con.cursor()    
    cur.execute("""
    SELECT * FROM MESSAGE 
    where receiverId=? or senderId=?
    ORDER BY sendTime
    """, (username,username))
    rows = cur.fetchall()
    
    messages = []
    
    for row in rows:
      message = {}
      message['id'] = row[0]
      message['from'] = row[1]
      message['to'] =  row[2]
      message['content'] = row[3]
      message['time'] = row[4]
      message['reply'] = message['from']
      
      if username == message['from']:
        message['reply'] = message['to']
      
      messages.append(message)
    
    return messages
    
  def messageDelete(self, messageId, userId):
    print("Try to delete the message " + str(messageId))
    cur = self.con.cursor()
    cur.execute("""
    SELECT * 
    FROM MESSAGE
    WHERE msgId=?
    """, (messageId))
    
    row = cur.fetchone()
    senderId = row[1]
    receiverId = row[2]
    ds = row[5]
    if senderId == userId:
      if ds == 0:
        ds = 1
      elif ds == 2:
        ds = 3

    elif receiverId == userId:
      if ds == 0:
        ds = 2
      elif ds == 1:
        ds = 3
    
    cur.execute("""
    UPDATE MESSAGE
    SET deleteStatus=?
    WHERE msgId=?
    """, (ds, messageId))
    self.con.commit()

    if cur.rowcount > 0:
      return True
    else:
      return False
   
  def messageView(self, messageId):
    pass
  
  def profileAddWork(self, dict):
    userId = dict["username"]
    company = dict["company"]
    role = dict["role"]
    location = dict["location"]
    startDate = dict["startDate"]
    endDate = dict["endDate"]

    cur = self.con.cursor()
    try:
      cur.execute("""
      INSERT INTO WORK_EXPR (userId, company, role, location, startDate, endDate)
      VALUES (?, ?, ?, ?, ?, ?)
      """, (userId, company, role, location, startDate, endDate))
      self.con.commit()
    except sqlite3.IntegrityError:
      return False

    return True

  def profileAddEdu(self, dict):
    pass

  def profileView(self, username):
    result = {}
    result['work'] = self.profileWorkExperience(username)
    result['edu'] = self.profileEduExperience(username)
    
    #TODO add connection status
    # This is cannot connect, can connect, connected (0, 1, 2)
    
    return result
    
  def profileWorkExperience(self, username):
    cur = self.con.cursor()    
    cur.execute("""
    SELECT * FROM WORK_EXPR 
    where userId=?
    """, (username,))
    rows = cur.fetchall()
    
    experiences = []
    
    for row in rows:
      experience = {}
      experience['company'] = row[1]
      experience['role'] =  row[2]
      experience['location'] = row[3]
      experience['start'] = row[4]
      experience['end'] = row[5]
      
      experiences.append(experience)
    
    return experiences
    
  def profileEduExperience(self, username):
    cur = self.con.cursor()    
    cur.execute("""
    SELECT * FROM EDUCATIONAL_DETAILS 
    where userId=?
    """, (username,))
    rows = cur.fetchall()
    
    experiences = []
    
    for row in rows:
      experience = {}
      experience['institution'] = row[1]
      experience['major'] =  row[2]
      experience['degree'] = row[3]
      experience['start'] = row[4]
      experience['end'] = row[5]
      
      experiences.append(experience)
    
    return experiences
