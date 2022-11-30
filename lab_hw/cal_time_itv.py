'''
Autor: Zel
Email: 2995441811@qq.com
Date: 2022-11-06 22:47:09
LastEditors: Zel
LastEditTime: 2022-11-06 23:03:46
'''
alpha = 0.125
beta = 0.25

ertt = 100
drtt = 10

srtt_list = [140, 90, 80, 110, 80]
ertt_list = []
drtt_list = []
Timeout_list = []

for i in range(len(srtt_list)):
    ertt = (1 - alpha) * ertt + alpha * srtt_list[i]
    drtt = (1 - beta) * drtt + beta * abs(srtt_list[i] - ertt)
    timeout = ertt + 4 * drtt
    ertt_list.append(int(ertt*10)/10)

    drtt_list.append(int(drtt*10)/10)
    Timeout_list.append(int(timeout*10)/10)

print(ertt_list)
print(drtt_list)
print(Timeout_list)

