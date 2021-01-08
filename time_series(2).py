#Dimitrios Cunning
#260874878
import doctest
import datetime
import numpy as np
import matplotlib.pyplot as plt

def date_diff(d1, d2):
    '''(str, str) -> int
    inputs two strings of dates in ISO format and returns how
    many days apart they are
    
    >>> date_diff('2018-10-31', '2018-11-2')
    2
    '''
    L1 = d1.split('-')
    L2 = d2.split('-') # dont know how else to do this since we did not learn anything about this in class
    date1 = datetime.date(int(L1[0]), int(L1[1]), int(L1[2]))
    date2 = datetime.date(int(L2[0]), int(L2[1]), int(L2[2]))
    diff = date2 - date1
    return diff.days

def get_age(d1, d2):
    '''(str, str) -> int
    inputs two strings of dates in ISO format and returns how many
    years appart they are as an integer
    
    >>> get_age('2018-10-31', '2000-11-2')
    -17
    >>> get_age('2018-10-31', '2019-11-2')
    1
    '''
    diff = date_diff(d1, d2)
    if diff<0:
        return -int(-diff//365.2425)
    else:#have to do this since x//y where x<0 gives a different answer than x//y
        return int(diff//365.2425)
    
numbers='1234567890'
def stage_three(input_filename, output_filename):
    '''(str, str) -> dict
    inputs file name and output file name then writes the new version
    of the line to a new file named output_filename, returns dictionary
    with form: {day: {'I': infected, 'R': recovered, 'D': dead}}
    >>> stage_three('data2.txt', 'data3.txt')
    {0: {'I': 1, 'D': 0, 'R': 0}, 1: {'I': 3, 'D': 0, 'R': 0}, 2: {'I': 6, 'D': 1, 'R': 0}, 3: {'I': 14, 'D': 1, 'R': 0}, 4: {'I': 31, 'D': 3, 'R': 0}, 5: {'I': 70, 'D': 4, 'R': 0}, 6: {'I': 146, 'D': 18, 'R': 0}, 7: {'I': 266, 'D': 88, 'R': 1}, 8: {'I': 651, 'D': 67, 'R': 4}, 9: {'I': 1207, 'D': 412, 'R': 3}}
    '''
    f = open(input_filename, "r", encoding = 'utf-8') #f = inputfile
    f1 = f.readlines() #list of lines
    g = open(output_filename, "w", encoding = 'utf-8') #g = output file
    l = f1[0].split('\t')
    index_date = l[2]
    d = {} #empty dict
    for i in f1:
        L = i.split('\t')
        L[2] = date_diff(index_date, L[2])
        L[3] = get_age(L[3], index_date)
        if L[6][0]=='I':
            L[6]='I'
            if not(L[2] in d):#appending each part to dictionary 'd'
                d.update({L[2]: {'I': 1, 'D': 0, 'R': 0}})
            else:   #if L[2] in d:
                d[L[2]] = {'I': (d.get(L[2]).get('I')+1), 'D': d.get(L[2]).get('D'), 'R': d.get(L[2]).get('R')}
    
        elif L[6][0]=='R':#appending each part to dictionary 'd'
            L[6]='R'
            if not(L[2] in d):
                d.update({L[2]: {'I': 0, 'D': 0, 'R': 1}})
            else:   #if L[2] in d:
                d[L[2]] = {'I': d.get(L[2]).get('I'), 'D': d.get(L[2]).get('D'), 'R': (d.get(L[2]).get('R')+1)}

            
        elif (L[6][0]=='D' or L[6][0]=='M'):#appending each part to dictionary 'd'
            L[6]='D'
            if not(L[2] in d):
                d.update({L[2]: {'I': 0, 'D': 1, 'R': 0}})
            else:   #if L[2] in d:
                d[L[2]] = {'I': d.get(L[2]).get('I'), 'D': (d.get(L[2]).get('D')+1), 'R': d.get(L[2]).get('R')}
        
        if not(L[6][0] in 'IRDM'):#removing Non Applicable entries for 'state'
            L[6]='NA'
        if 'N' in L[7]:#Calling them 'NA'
            L[7]='NA'
        if len(L[7])>4 and L[7][4]=='.':#removing extra decimals in 'temp'
            L[7]=L[7][:4]+L[7][4:].replace('.', '')
        
        #itterating through list L to rebuild string for output_file            
        s=''
        for j in L:
            if s.count('\t')<8:#turning list back into string
                s+=(str(j)+'\t')
            else:
                s+=str(j)
        g.write(s)
    g.close()
    return d

def plot_time_series(d):
    '''(dict) -> list
     input dictionary of dictionaries, formatted as the return value of Stage
     Three and return  a list of lists, where each sublist represents each day
     of the pandemic.  Each sublist in the form: [infected, recovered, dead]
    >>> plot_time_series({0: {'I': 1, 'D': 0, 'R': 0}, 1: {'I': 3, 'D': 0, 'R': 0}, 2: {'I': 6, 'D': 1, 'R': 0}, 3: {'I': 14, 'D': 1, 'R': 0}, 4: {'I': 31, 'D': 3, 'R': 0}, 5: {'I': 70, 'D': 4, 'R': 0}, 6: {'I': 146, 'D': 18, 'R': 0}, 7: {'I': 266, 'D': 88, 'R': 1}, 8: {'I': 651, 'D': 67, 'R': 4}, 9: {'I': 1207, 'D': 412, 'R': 3}})
    [[1, 0, 0], [3, 0, 0], [6, 0, 1], [14, 0, 1], [31, 0, 3], [70, 0, 4], [146, 0, 18], [266, 1, 88], [651, 4, 67], [1207, 3, 412]]
    '''
    L = []
    keys = list(d.keys())#days
    for i in list(d.values()): #dict for each day
        new_i = list(i.values())
        new_i[1], new_i[2] = new_i[2], new_i[1]
        L.append(new_i)
    
    plt.title('Time series of early pandemic, by Dimitri Cunning') 
    plt.xlabel('Days into Pandemic')
    plt.ylabel('Number of People')

    L1=[]
    for i in range(len(L)):#infected line
        L1.append(L[i][0])
    plt.plot(keys, L1, '-b', label='Infected')
    
    L2=[]
    for i in range(len(L)):#recovered line
        L2.append(L[i][1])
    plt.plot(keys, L2, '-', color='orange', label='Recovered')

    L3=[]
    for i in range(len(L)):#dead line
        L3.append(L[i][2])
    plt.plot(keys, L3, '-g', label='Dead')
    
    plt.legend(loc='upper left')
    plt.savefig('time_series.png')
    return L


if __name__=='__main__':
    doctest.testmod()
