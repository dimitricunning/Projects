#Dimitrios Cunning
#260874878
import doctest
import datetime
import numpy as np
import matplotlib.pyplot as plt

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '1234567890'
man = 'MAN Man MALE Male M BOY Boy B H HOMME Homme'
woman = 'WOMAN Woman FEMALE Female F G GIRL Girl W FEMME Femme' 
class Patient:
    '''Represnts Data

    Attributes: num (str), day_diagnosed (str), age (str),
                sex_gender (str), postal (str), state (str),
                temps (str), days_symptomatic (str)
                
    >>> P = Patient('0', '1', '20', 'M', 'V6K', 'I', '69C', '3')
    >>> print(str(P))
    0	20	M	V6K	1	I	3	20.56
    '''
    
    def __init__(self, n, d, a, g, p, s, t, sy):
        self.n = int(n) #num (n)
        self.d = int(d) #day_diagnosed (d)
        self.a = int(a) #age (a)
        
        #sex_gender (g)
        if g in man:
            self.g = 'M'
        elif g in woman:
            self.g = 'F'
        else:
            self.g = 'X'

        #postal (p)
        if len(p)>2 and (p[0] in letters and p[2] in letters and p[1] in numbers):
            self.p = p[0: 3]#make sure p is in postalcode format
        else:
            self.p = '000' #postal if not proper format

        #state (s)
        self.s = s

        #temps (t)
        if ('C' in t):#get rid of letters
            t=t.replace('C', '')
        if ('F' in t):#same
            t=t.replace('F', '')
        if (',' in t):#make t so that it can be change to float
            t=t.replace(',', '.')
        for i in t:
            if i in letters:#if temp not applicable
                self.t=float(0)
                break
            elif ';' in t:#for adding another temp, if one already exists 
                self.t = t
            elif float(t)>45:
                self.t = round((float(t)-32)*5/9, 2)#F to C conversion and round
            elif float(t)<=45:
                self.t = round(float(t), 2) #temps (C)

        #days_symptomatic (sy)
        self.sy = int(sy)
        
    def __str__(self):#returning string of new order of inputs in proper form
        return (str(self.n)+'\t'+str(self.a)+'\t'+self.g+'\t'+self.p+'\t'+str(self.d)+'\t'+self.s+'\t'+str(self.sy)+'\t'+str(self.t))

    def update(self, Patient):
        if Patient.n!=self.n or Patient.g!=self.g or Patient.p!=self.p:
            raise AssertionError ('Incorrect data')
                
        if int(self.sy)<=int(Patient.sy): #update days symptomatic
            self.sy = Patient.sy

        self.s = Patient.s #update state

        self.t = str(self.t) + ';' + str(Patient.t) #update temp

def stage_four(input_filename, output_filename):
    '''(str, str) -> dict
    inputs file, reads it and returns a dictionary with updated results and
    writes these results to output_file

    >>> d = stage_four('data3.txt', 'data4.txt')
    >>> len(d)
    1821
    '''
    f = open(input_filename, "r", encoding = 'utf-8') #f = inputfile
    f1 = f.readlines() #list of lines
    g = open(output_filename, "w", encoding = 'utf-8') #g = output file
    d={}
    for i in f1:#itterate through each line
        L = i.split('\t')
        if not(int(L[1]) in d.keys()):#if the person is not in the dictionary
            d.update({int(L[1]): Patient(L[1], L[2], L[3], L[4], L[5], L[6], L[7], L[8])})
        else:#if the person is in the dictionary. updating the info
            dL = str(d[int(L[1])]).split('\t')#dL is the dictionary info in list form
            curentP = Patient(dL[0], dL[4], dL[1], dL[2], dL[3], dL[5], dL[7], dL[6])#different odrer since output and input of Patient have different order
            newP = Patient(L[1], L[2], L[3], L[4], L[5], L[6], L[7], L[8])
            curentP.update(newP)
            d.update({int(L[1]): curentP})
    for i in range(max(list(d.keys()))+1):#itterate through person numbers
        if i in list(d.keys()):#if they exist
            line = str(d[i])
            g.write(line + '\n')#write data to output_file
    g.close()
            
    return d

def round_age(n):
    ''' int -> int
    rounds age to nearest multiple of 5
    >>> round_age(51)
    50
    >>> round_age(23)
    25
    '''
    return 5*round(n/5)
    

def fatality_by_age(d):
    '''dict -> list
    inupts dictionary in the form outputed by stage_four and returns a list of
    the ratios from the y axis of the graph saved representing the chance of
    survival for each 5 year age group

    >>> fatality_by_age(stage_four('data3.txt', 'data4.txt'))
    [1.0, 0.9705882352941176, 1.0, 0.9743589743589743, 0.9591836734693877, 1.0, 1.0, 1.0, 0.9767441860465116, 1.0, 0.9555555555555556, 1.0, 1.0, 1.0, 0.9615384615384616, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    '''
    # dict with form: {age: [deaths, recoveries]} all int
    ages = {}
    for i in d.values():
        i_list = str(i).split('\t')
        if i_list[5] == 'D':
            D = 1
            R = 0
        elif i_list[5] == 'R':
            R = 1
            D = 0
        else:
            R=D=0
        L = [D, R]# L = [deaths, recoveries]
        if not (round_age(int(i_list[1])) in ages):
            ages.update({round_age(int(i_list[1])): L})
        else:
            ages[round_age(int(i_list[1]))][0]+=L[0]
            ages[round_age(int(i_list[1]))][1]+=L[1]
    
    # change dict to form: {age: ratio} where ratio = D/(D+R)
    for k in ages.keys():
        if (ages[k][0]+ages[k][1])!=0:
            ages.update({k: ages[k][0]/(ages[k][0]+ages[k][1])})
        else:
            ages.update({k: float(1)})
    
    #ordering dictionary into graphable lists of ages and ratios
    age_list = []
    ratio_list = []
    for a in range(0, (max(ages.keys())+1), 5):
        if a in list(ages.keys()):
            age_list.append(a)
            ratio_list.append(ages[a])
    
    plt.title('Probability of death vs age, by Dimitri Cunning') 
    plt.ylabel('Deaths / (Deaths+Recoveries)')
    plt.xlabel('Age')
    plt.ylim((0, 1.2))

    plt.plot(age_list, ratio_list, '-b')
    plt.savefig('fatality_by_age.png')
    
    return ratio_list
    
    
if __name__=='__main__':
    doctest.testmod()
    
