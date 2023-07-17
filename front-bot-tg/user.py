class UserTable:
    def __init__(self):
        self.users = {}
        

    def add_user(self, tg_id, discord_id=' ', email=' ', phone=' ', name=' ', surname=' ', patronomic=' ', university=' ', student_group=' '):
        self.users[tg_id] = {"discordid":discord_id, "email":email, "phone":phone,
                                  "name":name, "surname":surname, "patronomic":patronomic,
                                    "university":university, "studentgroup":student_group}
        
    def edit_user_info(self, tg_id, data_type, data):
        self.users[tg_id][data_type] = data
    
    def get_user_info(self, tg_id):
        return self.users[tg_id] 

class ApplicationTable:
    def init(self):
        self.conference = {}
        self.applications = {}
    
    def add_application(self,user,conference,title='',adviser='',coauthors=''):
        self.applications = {"user":user,"conference":conference,"title":title,"adviser":adviser,"coauthors":coauthors}


