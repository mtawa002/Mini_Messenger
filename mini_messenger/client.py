from clientUI import clientUI
from dbMaster import dbMaster

dm = dbMaster()

ui = clientUI(dm)
ui.main()
