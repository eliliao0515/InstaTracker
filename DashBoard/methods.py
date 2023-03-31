import instaloader
from .models import profile

class loader():
    def __init__(self, username, password):
        self.L = instaloader.Instaloader()
        self.valid = True
        # Log in to Instagram account
        try:
            self.L.login(username, password)
        except:
            print("Login failed!")
            self.valid = False
            return
        if not self.L.context.is_logged_in:
            print("Login failed!")
            self.valid = False
            return 
        print("Login Success\n\n")

        # Get the profile of the logged-in user
        account = instaloader.Profile.from_username(self.L.context, username)

        # Get the followers of the profile
        self.followers = get_follower_names(account.get_followers())
        self.followings = get_following_names(account.get_followees())
        self.id = account.userid
        self.image = account.get_profile_pic_url
        self.username = account.username

        # Get sql data and compare
        user = profile.objects.filter(userID=self.id).first()
        if not user:
            print('new user added\n\n\n')
            # create new user data in sql
            user = profile(userID=self.id, username=username)
            user.set_my_list(self.followers,
                            self.followings)
            user.save()
        else:
            # Get diff information
            followers = user.get_my_list()[0]
            followings = user.get_my_list()[1]
            self.diff = check_diff(followers, followings, self.followers, self.followings)
            self.increase = len(self.diff['new_follower']) - len(self.diff['lost_follower'])
            self.decrease = len(self.diff['new_following']) - len(self.diff['lost_following'])

    def is_valid(self):
        return self.valid
    
    def get_id(self):
        return self.id
    
    def get_image(self):
        return self.image
    
    def get_username(self):
        return self.username
    
    def get_increase(self):
        return self.increase
    
    def get_decrease(self):
        return self.decrease
    
    def get_diff(self):
        return self.diff
    
def get_follower_names(data):
    names = []
    for follower in data:
        names.append(follower.username)
    return names

def get_following_names(data):
    names = []
    for following in data:
        names.append(following.username)
    return names

def check_diff(followers, followings, new_followers, new_followings):
    new_follower_list = []
    new_following_list = []
    lost_follower_list = []
    lost_following_list = []

    for n in new_followers: 
        if not n in followers:
            new_follower_list.append(n)

    for n in new_followings:
        if not n in followings:
            new_following_list.append(n)

    for n in followers:
        if not n in new_followers:
            lost_follower_list.append(n)

    for n in followings:
        if not n in new_followings:
            lost_following_list.append(n)

    return {"new_follower":new_follower_list,
            "new_following":new_following_list,
            "lost_follower":lost_follower_list,
            "lost_following":lost_following_list}