'''
variables to use:- email_id,pwd1
'''
import json as j
file=open('data.json','r')
ob1=j.load(file)
if(id in ob1['details'].keys()):    
    if(pwd ==ob1['details'][id]['Password']):
        print('matched')
        
        


