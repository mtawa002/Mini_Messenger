import pygtk
pygtk.require('2.0')
import gtk
import gobject
import threading
from Queue import Queue

class clientUI:

  def __init__(self, dm):
    gobject.threads_init()
    
    self.dm = dm
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.show()
    self.window.connect("destroy", self.destroy)
    self.window.set_title("Database Client")
    self.window.set_size_request(800, 400)
    
    self.user = {}
    
    self.loginPage = self.buildLoginPage() 
    
    self.window.add(self.loginPage)
    
    self.pages = [
    'user',
    'people',
    'profile',
    'request',
    'message',
    'compose'
    ]
    
    self.login("Giovani", "Terry")
    
  def main(self):
    try:
      gtk.main()
    except KeyboardInterrupt:
      print("Goodbye...")
      exit(0)
      
  def destroy(self, widget, data=None):
    gtk.main_quit()
    
  def switchTo(self, new):
    widgets = self.window.get_children()
    
    for widget in widgets:
      self.window.remove(widget)
   
    self.window.add(new)
    
  def buildLoginPage(self):
    hbox = gtk.HBox(True, 10)
    hbox.show()
    
    create_side = gtk.VBox()
    create_side.show()
    
    form_box = gtk.VBox()
    form_box.show()
    
    # Username
    
    username_box = gtk.HBox()
    username_box.show()
    
    label = gtk.Label("Username")
    label.show()
    username_box.pack_start(label, expand = True, fill = True)
    
    self.username = gtk.Entry()
    self.username.show()
    username_box.pack_start(self.username, expand = False, fill = False)
    form_box.pack_start(username_box, expand = False, fill = False)
    
    # Password
    
    password_box = gtk.HBox()
    password_box.show()
    
    label = gtk.Label("Password")
    label.show()
    password_box.pack_start(label, expand = True, fill = True)
    
    self.password = gtk.Entry()
    self.password.show()
    password_box.pack_start(self.password, expand = False, fill = False)
    form_box.pack_start(password_box, expand = False, fill = False)
    
    
    create_side.pack_start(form_box, expand = True, fill = False)
    
    # Create
    
    create_box = gtk.HBox(False, 10)
    create_box.show()
    
    self.create_button = gtk.Button("Create User")
    self.create_button.connect_after("clicked", self.create)
    self.create_button.show()
    
    create_box.pack_start(self.create_button, expand = False, fill = False)
    
    self.login_button = gtk.Button("Login")
    self.login_button.connect_after("clicked", self.callback_login)
    self.login_button.show()
    
    create_box.pack_start(self.login_button, expand = False, fill = False)

    
    create_side.pack_start(create_box, expand = True, fill = False)
    
    status_image = gtk.Image()
    status_image.set_from_stock(gtk.STOCK_DIALOG_INFO, gtk.ICON_SIZE_DIALOG)
    status_image.show()
    
    hbox.add(create_side)
    hbox.pack_start(status_image, expand = False, fill = False)
    return hbox
    
  def buildMainPage(self):
    notebook = gtk.Notebook()
    notebook.set_tab_pos(gtk.POS_LEFT)
    notebook.connect_after("switch-page", self.switch)
    notebook.show()
    
    #Notebook tabs
    label = gtk.Label("User")
    userPage = self.buildUserPage()
    notebook.append_page(userPage, label)
    notebook.child_set_property(userPage, 'tab-expand', True)
    
    label = gtk.Label("People")
    peoplePage = self.buildPeoplePage()
    notebook.append_page(peoplePage, label)
    notebook.child_set_property(peoplePage, 'tab-expand', True)
    
    self.profileContainer = gtk.VBox()
    self.profileContainer.show()
    
    label = gtk.Label("Profile")
    notebook.append_page(self.profileContainer, label)
    notebook.child_set_property(self.profileContainer, 'tab-expand', True)
    
    label = gtk.Label("Requests")
    requestPage = self.buildRequestPage()
    notebook.append_page(requestPage, label)
    notebook.child_set_property(requestPage, 'tab-expand', True)
    
    label = gtk.Label("Messages")
    messagePage = self.buildMessagePage()
    notebook.append_page(messagePage, label)
    notebook.child_set_property(messagePage, 'tab-expand', True)
    
    label = gtk.Label("Compose")
    composePage = self.buildComposePage()
    notebook.append_page(composePage, label)
    notebook.child_set_property(composePage, 'tab-expand', True)
    
    self.notebook = notebook
    
    return notebook
    
  def buildUserPage(self):
    vbox = gtk.VBox(False, 10)
    vbox.show()

    button = gtk.Button("My Profile")
    button.connect_after("clicked", self.show_profile)
    button.show()
    vbox.pack_start(button, False, False)
    
    button = gtk.Button("Logout")
    button.connect_after('clicked', self.callback_logout)
    button.show()
    vbox.pack_start(button, False, False)
    
    hbox = gtk.HBox(False, 10)
    hbox.show()
    
    label = gtk.Label("Old")
    label.show()
    hbox.pack_start(label, False, False)
    
    oldPassword = gtk.Entry()
    oldPassword.show()
    hbox.pack_start(oldPassword)
    
    label = gtk.Label("New")
    label.show()
    hbox.pack_start(label, False, False)
    
    newPassword = gtk.Entry()
    newPassword.show()
    hbox.pack_start(newPassword, False, False)
    
    button = gtk.Button("Change Password")
    button.show()
    hbox.pack_start(button, False, False)
    
    vbox.pack_start(hbox, False, False)
    
    return vbox
    
  def buildPeoplePage(self):
    vbox = gtk.VBox(False, 10)
    vbox.show()
    
    text = gtk.Entry()
    text.show()
    vbox.pack_start(text, False, False)
    
    self.model_search = gtk.ListStore(str, str, str)
    tree_view = gtk.TreeView(self.model_search)
    
    def callback_search(widget, text):
      name = text.get_text()
      users = self.dm.search(name)
      
      self.model_search.clear()
      
      for user in users:
        self.model_search.append([
        user['username'],
        user['name'],
        ''
        ])
    
    button = gtk.Button("Search")
    button.show()
    button.connect_after('clicked', callback_search, text)
    vbox.pack_start(button, False, False)
    
    def callback_all(widget):
      users = self.dm.connectionList(self.user['username'])
      
      self.model_search.clear()
      
      for user in users:
        self.model_search.append([
        user['username'],
        user['name'],
        user['status']
        ])
    
    button = gtk.Button("All Connections")
    button.show()
    button.connect_after('clicked', callback_all)
    vbox.pack_start(button, False, False)
    
    frame = gtk.Frame()
    frame.show()
    
    listWindow = gtk.ScrolledWindow()
    listWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    listWindow.show()
    frame.add(listWindow)
    vbox.pack_start(frame, True, True)
    
    listWindow.add_with_viewport(tree_view)
    tree_view.show()
    
    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn("Username", cell, text=0)
    tree_view.append_column(column)
    
    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn("Name", cell, text=1)
    tree_view.append_column(column)
    
    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn("Status", cell, text=2)
    tree_view.append_column(column)
    
    hbox = gtk.HBox()
    hbox.show()
    
    button = gtk.Button("Connect")
    button.show()
    hbox.pack_start(button, False, False)
    
    button = gtk.Button("Disconnect")
    button.show()
    hbox.pack_start(button, False, False)
    
    button = gtk.Button("View Profile")
    button.show()
    hbox.pack_start(button, False, False)
    
    button = gtk.Button("Message")
    button.show()
    hbox.pack_start(button, False, False)
    
    vbox.pack_start(hbox, False, False)
    
    return vbox
    
    
  def buildProfilePage(self, username):
    profile = self.dm.profileView(username)
  
    vbox = gtk.VBox(False, 10)
    vbox.show()
    
    label = gtk.Label("Username: " + username)
    label.show()
    vbox.pack_start(label, False, False)
    
    hbox = gtk.HBox()
    hbox.show()
    vbox.pack_start(hbox, False, False)
    
    button = gtk.Button("Connect")
    button.show()
    hbox.pack_start(button, False, False)
    
    button = gtk.Button("Disconnect")
    button.show()
    hbox.pack_start(button, False, False)
    
    button = gtk.Button("Message")
    button.show()
    hbox.pack_start(button, False, False)
    
    profileWindow = gtk.ScrolledWindow()
    profileWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    profileWindow.show()
    vbox.pack_start(profileWindow)

    profileBox = gtk.VBox(False, 10)
    profileBox.show()
    profileWindow.add_with_viewport(profileBox)

    frame = gtk.Frame("Connections")
    frame.show()
    profileBox.add(frame)
    
    users = ['John Hinkel', 'marlin brando', 'asshole']
    users = self.dm.connectionList(username)

    table = gtk.Table(len(users), 3)
    
    for index, user in enumerate(users):
      label = gtk.Label(user['username'])
      label.show()
      table.attach(label, 0, 1, index, index+1)
      
      label = gtk.Label(user['name'])
      label.show()
      table.attach(label, 1, 2, index, index+1)
      
      button = gtk.Button("View Profile")
      button.connect_after('clicked', self.show_profile, user['username'])
      button.show()
      table.attach(button, 2, 3, index, index+1)
    
    table.show()
    frame.add(table)

    experience = profile['work']

    cols = 6
    
    if len(experience) > 0:
      frame = gtk.Frame("Work Experience")
      frame.show()
      profileBox.add(frame)
      table = gtk.Table(len(experience)*cols, 3)
      frame.add(table)
    
    for index, exp in enumerate(experience):
    
      count = 0
      label = gtk.Label("Experience " + str(index + 1))
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      button = gtk.Button("Delete")
      button.show()
      table.attach(button, 1, 2, cols*index + count, cols*index + count +1)

      count = count  + 1
      label = gtk.Label("Company")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      label = gtk.Label(exp['company'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)

      count = count  + 1
      label = gtk.Label("Role")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
            
      label = gtk.Label(exp['role'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)
      
      count = count  + 1
      label = gtk.Label("Location")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      label = gtk.Label(exp['location'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)
      
      count = count  + 1
      label = gtk.Label("Start")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      label = gtk.Label(exp['start'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)
      
      count = count  + 1
      label = gtk.Label("End")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      label = gtk.Label(exp['end'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)
    
    table.show()
    
    experience = profile['edu']
    
    if len(experience) > 0:
      frame = gtk.Frame("Work Experience")
      frame.show()
      profileBox.add(frame)
      table = gtk.Table(len(experience)*cols, 3)
      frame.add(table)
      
    cols = 6
    
    for index, exp in enumerate(experience):
    
      count = 0
      label = gtk.Label("Experience " + str(index + 1))
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      button = gtk.Button("Delete")
      button.show()
      table.attach(button, 1, 2, cols*index + count, cols*index + count +1)

      count = count  + 1
      label = gtk.Label("Institution")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      label = gtk.Label(exp['institution'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)

      count = count  + 1
      label = gtk.Label("Major")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
            
      label = gtk.Label(exp['major'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)
      
      count = count  + 1
      label = gtk.Label("Degree")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      label = gtk.Label(exp['degree'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)
      
      count = count  + 1
      label = gtk.Label("Start")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      label = gtk.Label(exp['start'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)
      
      count = count  + 1
      label = gtk.Label("End")
      label.show()
      table.attach(label, 0, 1, cols*index + count, cols*index + count +1)
      
      label = gtk.Label(exp['end'])
      label.show()
      table.attach(label, 1, 2, cols*index + count, cols*index + count +1)
    
    table.show()
    
    return vbox
    
  def buildRequestPage(self):
    vbox = gtk.VBox(False, 10)
    vbox.show()
    frame = gtk.Frame("Requests")
    frame.show()
    
    listWindow = gtk.ScrolledWindow()
    listWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    listWindow.show()
    
    frame.add(listWindow)
    vbox.pack_start(frame, True, True)
    
    self.model_request = gtk.ListStore(str, str)
    tree_view = gtk.TreeView(self.model_request)
    listWindow.add_with_viewport(tree_view)
    tree_view.show()
    
    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn("Username", cell, text=0)
    tree_view.append_column(column)
    
    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn("Name", cell, text=1)
    tree_view.append_column(column)
    
    hbox = gtk.HBox()
    hbox.show()
    vbox.pack_start(hbox, False, False)
    
    def callback_connect(widget, selection, action):
      t_model, t_iter = selection.get_selected()
      
      if t_iter != None:
        s_new = t_model.iter_next(t_iter)
        if s_new == None:
          s_new = t_model.get_iter_first()
          
        if s_new != None:
          selection.select_iter(s_new)
        
        user = t_model.get_value(t_iter, 0)
        t_model.remove(t_iter)
        
        if action == 'accept':
          self.dm.connectionAccept(self.user['username'], user)
        elif action == 'reject':
          self.dm.connectionReject(self.user['username'], user)
    
    button = gtk.Button("Accept")
    button.connect_after('clicked', callback_connect, tree_view.get_selection(), 'accept')
    button.show()
    hbox.pack_start(button, False, False)
    
    button = gtk.Button("Reject")
    button.connect_after('clicked', callback_connect, tree_view.get_selection(), 'reject')
    button.show()
    hbox.pack_start(button, False, False)
    
    return vbox
    
  def buildMessagePage(self):
    hbox = gtk.HBox(True, 10)
    hbox.show()
    
    vbox = gtk.VBox(False, 10)
    vbox.show()
    hbox.pack_start(vbox)
    
    frame = gtk.Frame("Messages")
    frame.show()
    vbox.pack_start(frame, True, True)
    
    listWindow = gtk.ScrolledWindow()
    listWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    listWindow.show()
    frame.add(listWindow)
    
    self.model_messages = gtk.ListStore(int, str, str, str, str)
    tree_view = gtk.TreeView(self.model_messages)
    
    listWindow.add_with_viewport(tree_view)
    tree_view.show()
    
    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn("From", cell, text=1)
    tree_view.append_column(column)
    
    cell = gtk.CellRendererText()
    column = gtk.TreeViewColumn("To", cell, text=2)
    tree_view.append_column(column)
    
    actions = gtk.HBox()
    actions.show()
    vbox.pack_end(actions, False, False)
    
    def delete_message(widget, selection):
      t_model, t_iter = selection.get_selected()
      
      if t_iter != None:
        s_new = t_model.iter_next(t_iter)
        if s_new == None:
          s_new = t_model.get_iter_first()
          
        if s_new != None:
          selection.select_iter(s_new)
        
        messageId = t_model.get_value(t_iter, 0)
        t_model.remove(t_iter)
        self.dm.messageDelete(messageId)
        
        
    button = gtk.Button("Delete")
    button.show()
    actions.pack_start(button, True, True)
    button.connect_after('clicked', delete_message, tree_view.get_selection())
    
    def launch_profile(widget, selection):
      t_model, t_iter = selection.get_selected()
      
      if t_iter != None:
        # Username to show is the same you would reply to
        username = t_model.get_value(t_iter, 4)

        print(username)
          
        # TODO Show the profile of that user
        
    
    button = gtk.Button("Profile")
    button.show()
    button.connect_after('clicked', launch_profile, tree_view.get_selection())
    actions.pack_start(button, True, True)

    def launch_compose(widget, selection):
      t_model, t_iter = selection.get_selected()
      
      if t_iter != None:
        # Username to show is the same you would reply to
        username = t_model.get_value(t_iter, 4)

        print(username)
          
        # TODO Let the user write a message to this person

    button = gtk.Button("Reply")
    button.show()
    button.connect_after('clicked', launch_compose, tree_view.get_selection())
    actions.pack_start(button, True, True)
    
    frame = gtk.Frame("Detail")
    frame.show()
    hbox.pack_start(frame, True, True)
    
    detailWindow = gtk.ScrolledWindow()
    detailWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    detailWindow.show()    
    frame.add(detailWindow)
    
    detailBox = gtk.VBox()
    detailBox.show()
    detailWindow.add_with_viewport(detailBox)
    
    detailText = gtk.TextView()
    detailText.set_wrap_mode(gtk.WRAP_WORD)
    detailText.show()
    detailBox.pack_start(detailText, True, True)
    
    selection = tree_view.get_selection()
    selection.connect_after('changed', self.callback_message, detailText.get_buffer())

    
    return hbox
    
  def buildComposePage(self):
    vbox = gtk.VBox()
    vbox.show()
    username = "asdf"
    
    label = gtk.Label("To: " + username)
    label.show()
    vbox.pack_start(label, False, False)
    
    
    messageWindow = gtk.ScrolledWindow()
    messageWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    messageWindow.show() 
    vbox.pack_start(messageWindow, True, True)
    
    content = gtk.TextView()
    content.show()
    messageWindow.add(content)
    
    hbox = gtk.HBox()
    hbox.show()
    vbox.pack_start(hbox, False, False)
    
    button = gtk.Button("Send")
    button.show()
    hbox.pack_start(button, True, True)
    
    button = gtk.Button("Clear")
    button.show()
    hbox.pack_start(button, True, True)
    
    return vbox
    
  def show_profile(self, widget, username = None):
    
    if username == None:
      username = self.user['username']
  
    profilePage = self.buildProfilePage(username)
    profilePage.show()
    
    profiles = self.profileContainer.get_children()
    
    for profile in profiles:
      self.profileContainer.remove(profile)
    
    self.profileContainer.add(profilePage)
    
    self.notebook.set_current_page(self.pages.index('profile'))
    
  def switch(self, notebook, num, Data = None):
    page = notebook.get_current_page()
    
    try:
      getattr(self,'switch_' + self.pages[page])()
    except:
      return
    
  def switch_user(self):
    pass
    
  def switch_profile(self):
    pass

  def switch_request(self): 
    users = self.dm.connectionRequests(self.user['username'])
    
    self.model_request.clear()
    
    for user in users:
      self.model_request.append([
      user['username'],
      user['name'],
      ])
      
  def switch_message(self):
    self.model_messages.clear()
    
    messages = self.dm.messageList(self.user['username'])
    
    for message in messages:
      self.model_messages.append([
      message['id'],
      message['from'],
      message['to'],
      message['content'],
      message['reply']
      ])
    
  def switch_compose(self):
    pass
    
  def userDetails(self):
    return {
    'user' : self.username.get_text(),
    'pass' : self.password.get_text()
    }
    
  def callback_login(self, widget, data = None):
    details = self.userDetails()
    self.login(details['user'], details['pass'])
    
  def callback_logout(self, widget, data = None):
    result = self.dm.logout(self.user['username'])
    self.user = {}
    
    self.switchTo(self.loginPage)
    
  def callback_message(self, selection, buffer):
    t_model, t_iter = selection.get_selected()
    
    if t_iter != None:
      messageId = t_model.get_value(t_iter, 0)
      content = t_model.get_value(t_iter, 3)
      buffer.set_text(content)
      
  def login(self, username, password):
    result = self.dm.login(username, password)
    
    if result['success']:
      self.switchTo(self.buildMainPage())
      self.user['username'] = result['username']
    else:
      pass
    
  def create(self, widget, data = None):
    details = self.userDetails()
    self.dm.create(details['user'], details['pass'])
    
