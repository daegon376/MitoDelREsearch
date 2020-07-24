from datetime import datetime
import re

reg_exp_file = open('output.txt')
reads_file = open('output_testing_reads.txt')

reads = str()
for s in reads_file:
    reads = str(reads + s)
# print(reads)

f = open('REsults.txt', 'w')
f.write('')  # clean output


def re_search(reg_exp, info):
    pattern = re.compile(reg_exp)
    deletions = pattern.findall(reads)
    if len(deletions) != 0:
        with open('REsults.txt', 'a') as output:
            print(info, len(deletions[0]), reg_exp, len(deletions), deletions[0], file=output)


start_time = datetime.now()  # запуск таймера

for s in reg_exp_file:
    info = re.split(r're:', s)[0]
    reg_exp = re.split(r're:', s)[1]
    reg_exp = reg_exp[:-1]
    # print(info)
    # print(reg_exp)
    re_search(reg_exp, info)

print('Полное время: ' + str(datetime.now() - start_time))
