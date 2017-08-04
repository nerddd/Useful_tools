import matplotlib.pyplot as plt 

y1=[18975,713760,1264102,2264348,593351,106502,24588,5592,1588,421,98,17,3,0,0,0,1,0,8,21] 
x1=range(0,200,10) 

num = 0
for i in range(20):
    num+=y1[i]
print num
plt.plot(x1,y1,label='Frist line',linewidth=1,color='r',marker='o', 
markerfacecolor='blue',markersize=6) 
plt.xlabel('eye_width distribute') 
plt.ylabel('Num') 
plt.title('Eye\nCheck it out') 
plt.legend()
plt.savefig('figure2.png') 
plt.show() 