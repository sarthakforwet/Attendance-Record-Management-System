
'''
when the script is started if the below conditions are satisified do to main window
'''

with open('logged_in.json','r') as logged_in_file:
    line=logged_in_file.readline()
if(line=='yes'):
    '''go to main window'''
else:
    '''go to log in window'''




'''
when on login window 
if checkbox is clicked.
'''
with open('logged_in.json','w') as logged_in_file:
    logged_in_file.write('yes')




''' log out functionality'''

if('log logout button is clicked'):
    with open('logged_in.josn','w') as logged_in_file:
        logged_in_file.write('no')
    '''go to login window'''

    