#get input from user
poly_input = input("Input the polynomials:")

# split formula
def split(x):
    x = x.replace(")(", ";").replace(")", "").replace("(", "")
    ls_formula = (x.split(';',))
    return ls_formula
poly = split(poly_input)

# break each poly by operator
def poly_break(x):
    temp = x.replace("-","_-").replace("+","_")
    test_split = temp.split('_')
    return test_split
	
def preprocess(f):
    count = 0
    for num in f:#add ^ and * operator to formula
        if num[0] == '-'and num[1].isdigit() == False:
            num = num.replace("-","")
            f[count] = "-1*"+num
        elif num[0].isdigit() == False:
            f[count] = "1*"+num
            num = f[count]
        len_num = len(num)
        if len_num > 1:
            for j in range(len_num):
                if num[j].isdigit() == False:
                    if j == len(num)-1:
                        f[count] = num+'^1'
                    elif num[j]!='^' and num[j]!='*'and num[j+1]!='^':
                        num = num.replace(num[j],num[j]+"^1")
        elif num[0].isdigit() == False:
            f[count] = num+'^1'
        count += 1
    return f

def coef_var(f):#split coef and var
    coef_f = []
    var_f = []
    for elem in f:
        if '*'not in elem:
            coef_f.append(int(elem))
            var_f.append(1)
        else:
            coef_f.append(int(elem.split('*',1)[0]))
            var_f.append(elem.split('*',1)[1])
    return coef_f, var_f

poly_num = len(poly)#calculate poly's len
coef_all = []#list for coef
var_all = []#list for var
for i in poly:
    poly_b_result = (poly_break(i))
    poly_b_result = preprocess(poly_b_result)
    coef, var = coef_var(poly_b_result)
    coef_all.append(coef)
    var_all.append(var)

#set the list for seperated coef and var
coef_num = 1
var_num = 1
for i in coef_all:
    i_len = len(i)
    coef_num *= i_len
result_coef = [0]*coef_num
for i in var_all:
    i_len = len(i)
    var_num *= i_len
result_var = [0]*(var_num)

#multiplication function
def multiply(tmp_c, new_c, tmp_v, new_v):
    temp_coef = []
    temp_var = []
    for i in range(len(tmp_c)):
        for j in range(len(new_c)):
            temp_coef.append(int(tmp_c[i])*int(new_c[j]))
            temp_var.append(str(tmp_v[i]) + str(new_v[j]))
    return temp_coef, temp_var

count = 1
_coef = coef_all[0]
_var = var_all[0]
while(count<poly_num):#multiply coef and var seperately
    coef_elem = coef_all
    var_elem = var_all
    _coef, _var = multiply(_coef, coef_elem[count],_var, var_elem[count])
    count += 1

for i in range(len(_var)):#get rid of coef'1'
    count = 1
    if _var[i][0].isdigit() == True:
        while(_var[i][count].isdigit() == True):
            count += 1
        tmp = ''
        for j in range(count,len(_var[i])):
            tmp = tmp +_var[i][j]
        _var[i] = tmp

ls_var_dict = {}
for i in _var:# get unique variable
    ls_var = []
    len_i = len(i)
    for j in range(len_i):
        if j != len_i-1:
            if i[j] == '^':
                ls_var.append(i[j-1])
    ls_var = list(dict.fromkeys(ls_var))
    ls_var_dict[i] = ls_var
ls_var_dict

repeat = {}# get repeated variables
for key, value in ls_var_dict.items():
    repeat[key] = []
    for i in range(len(value)):
           if key.count(value[i])>1 and value[i].isdigit()==False:
                repeat[key].append(value[i])

final_var = {}
for key, value in ls_var_dict.items():
    final_var[key]=key
    if repeat[key] != []:
        for i in range(len(repeat[key])):#get repeated var in each poly
            num = 0
            str_ls = []
            for j in range(len(key)):
                if repeat[key][i] == key[j]:#store repeat var == those in string
                    ls = ''
                    count = j+1
                    while(key[count].isdigit==True):
                        count += 1
                    for k in range(j, count+2):
                        ls = ls+key[k]
                    str_ls.append(ls)
            count_2 = 0
            for m in str_ls:
                number = ''#remove repeated var
                final_var[key] = final_var[key].replace(m,'')
                for n in range(len(m)):
                    if m[n].isdigit() == True:
                        number = number +m[n]
                        num += int(number)
                if (count_2<len(str_ls)-1):
                    count_2 += 1
            for p in range(len(str_ls[count_2])):
                to_replace_num = ''
                if str_ls[count_2][p].isdigit() == True:
                    to_replace_num += str_ls[count_2][p]#add concated repeated var
            replace_str = str_ls[count_2].replace(to_replace_num,str(num))
            final_var[key] += replace_str

ls = []
for key in final_var:#put the concat result into list
    ls.append(final_var[key])

var_split = {}#split the variables for check if replicated
for i in ls:
    var_split[i]=[]
    for j in range(len(i)):
        if i[j] =='^':
            count = j
            tmp = ''
            while(i[count+1].isdigit()==True and count<len(i)-2):
                count += 1
                tmp += i[count]
            if count+1 == len(i)-1:
                tmp +=i[count+1]
            var_split[i]+=[i[j-1]+i[j]+tmp]

result = [{k: v} for (k, v) in var_split.items()]

same = {}#see if any result need to be add
for i in range(len(result)):
    for j in range(i+1, len(result)):
        if(result[i][ls[i]] == result[j][ls[j]]):
            same[ls[i]]+=result[i][ls[i]]
            same[ls[i]]+=result[j][ls[j]]

if same == {}:
	for i in range(len(_coef)):#conver coef from int to str
		_coef[i] = str(_coef[i]) 

	#concat coef and va
	ans_var = []
	for i in range(len(ls)):
		ans_var.append(_coef[i]+ls[i])
	ans = ''
	for i in range(len(ans_var)):
		if i == 0 or ans_var[i][0]=='-':
			ans += ans_var[i]
		else:
			ans +='+'+ans_var[i]
print("Output Result: ",ans)