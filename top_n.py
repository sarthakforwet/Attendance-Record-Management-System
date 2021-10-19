d={'a':[0.5,0.9,0.7],'b':[0.78,0.31,0.44],'c':[1,0.4,0.6],'d':[0.8,0.6,0.45],'e':[0.6,0.5,0.8]}
'''threshold value =0.9'''
import pandas as pd
nSnips=1
def top_n():
    score={}
    temp=[]
    di={5:3,3:2,1:1}
    for i in d:
        temp=d[i]
        temp.sort(reverse=True)
        if(sum(temp[:di[nSnips]])>=0.9):
            score[i]=sum(temp[:di[nSnips]])


    print(score)

top_n()
 
            

            

        







    
    

    

    