## Identifys Guests and deletes user accounts (Maybe deploy each night to keep things clean?)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

from firebase_admin import firestore

cred = credentials.Certificate("question-writing-interface-firebase-adminsdk-jxvw3-623f426f96.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Start listing users from the beginning, 1000 at a time.

uids =[]

page = auth.list_users()
while page:
    for user in page.users:
        
        uids.append(user.uid)
        
    page = page.get_next_page()

guests = []

for uid in uids:
    user = auth.get_user(uid)
    ##DEBUGGING PLEASE DONT DELETE
    #print(('UID: %s')%user.uid)
    #print(('CREATION: %d' )% user.user_metadata.creation_timestamp)
    #print(('PROVIDER: %s' )% user.display_name)
    if(user.display_name == None):
         guests.append(user.uid)
         
         

    #print(guests)


    
    
   

result = auth.delete_users(guests)
print('Successfully deleted {0} guests'.format(result.success_count))
print('Failed to delete {0} users'.format(result.failure_count))
for err in result.errors:
    print('error #{0}, reason: {1}'.format(result.index, result.reason))

    




