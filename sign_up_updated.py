'''
>>>>>>>>>>>>>>>>>>>>
    ob1['details['email_id]'['name']=name
    ob1['email_id']['number']=number
    ob1['email_id']['pwd']=pwd
>>>>>>>>>>>>>>>>>>>>>>>


    
    >>>>variables to use:-  name,number,email_id,pwd1,pwd2
    '''


import json as j

if(pwd1==pwd_2):
    fil=open('data.json','r+')
    ob1=j.load(fil)
    ob1['details'][email_id]={'Name':name,'Contact_number':number,'Password':pwd1}
    f = open("myfile.json", "w")
    j.dump(ob1,f)
    fil.close()
    f.close()
    ''' redirected to login page'''
else:
    '''
    pop up winodow displaying password does not match'''
    print("pwd dosent matched")






