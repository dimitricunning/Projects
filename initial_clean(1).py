#Dimitrios Cunning
#260874878
import doctest
def which_delimiter(s):
    '''str -> str
    Returns most common delimiter in the string 's'
    >>> which_delimiter('1 2 3,')
    ' '
    >>> which_delimiter('1,,3,,  2')
    ','
    '''
    if not((' ' in s) or (',' in s) or ('\t' in s)):
        raise AssertionError ('Should have at least one delimiter')
    # i coppied the following code exactly into shell and it worked fine for
    # s = '3\t,2\t' (it returned a tab), but the test does not work
    # in the doctest, it instead returns a space.
    for i in ['\t', ',', ' ']:
        if s.count(i)==max(s.count(' '), s.count(','), s.count('\t')):
            return i


def stage_one(input_filename, output_filename):
    '''(str, str) -> int
    inputs file name and output file name then writes the new version
    of the line to a new file named output_filename, returns number of
    lines in output_filename
    >>> stage_one('data0.txt', 'data1.txt')
    3000
    '''
    letters= 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers ='1234567890'
    #f = inputfile
    f = open(input_filename, "r", encoding = 'utf-8')
    f1 = f.readlines()
    #g = output file
    g = open(output_filename, "w", encoding = 'utf-8')
    k = 0 # line count initial condition
    for i in f1:#itterate through lines in input_file
        l=i.split(which_delimiter(i))
        l=[i.upper() for i in l]
        if ((l[5][0] in letters) and (l[5][1] in numbers) and (l[5][2] in letters) and (l[6][0] in numbers) and (l[6][1] in letters) and (l[6][2] in numbers)):
            l[5]=l[5]+l[6]
            l.remove(l[6])
                 
        for j in l:#itterating through list to input to output_file
            j=j.replace('/', '-')
            j=j.replace('.', '-')
            if j==l[len(l)-1]:
                g.write(j)
            else:
                g.write(j+'\t')
        
        k += 1#line counter
    g.close()
    return k
       

def stage_two(input_filename, output_filename):
    '''(str, str) -> int
    inputs file name and output file name then writes the new version
    of the line to a new file named output_filename, returns number of
    lines in output_filename
    >>> stage_two('data1.txt', 'data2.txt')
    3000
    '''
    f = open(input_filename, "r", encoding = 'utf-8')#f = inputfile
    f1 = f.readlines()
    g = open(output_filename, "w", encoding = 'utf-8')#g = output file
    k = 0 # line count initial condition
    
    for i in f1:
        l = i.split('\t')
        if i.count('\t') > 8:
            
            for j in l[8]:
                if j in '1234567890':#fixing lines with extra column
                    l[7]=l[7]+'.'+str(j)
                if j in 'C':
                    l[7]=l[7]+'C'
                if j in 'F':
                    l[7]=l[7]+'F'
            del(l[8])#removing extra column
        if '°' in l[7]:#remove unnessesary dot
            l[7]=l[7].replace('°' , '')
        if '-' in l[7]:#make temp consistet
            l[7]=l[7].replace('-', '.')
        if ',' in l[7]:#same
            l[7]=l[7].replace(',', '.')
        
        s=''
        for i in l:
            if s.count('\t')<8:#turning list back into string
                s+=(str(i)+'\t')
            else:
                s+=str(i)
        g.write(s)#writing string to output_filename
        k+=1
    g.close()
    
    return k


if __name__=='__main__':
               doctest.testmod()
