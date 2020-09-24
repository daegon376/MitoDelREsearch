from datetime import datetime
import re

reg_exp_file = open('output.txt')
reads_file = open('B:/Chimera/control/test_output_reads.txt')

reads = str()  # все риды записываем в одну строку
for s in reads_file:
    reads = str(reads + s)
# print(reads)

f = open('REsults.txt', 'w')
f.write('')  # clean output


def re_search(reg_exp, info):
    pattern = re.compile(reg_exp)
    deletions = pattern.findall(reads)
    if len(deletions) != 0:  # если что-то нашли
        new_reg_exp = str('.*' + str(re.search(r'^\w*', reg_exp).group(0)) + deletions[0] +
                          str(re.search(r'\w*$', reg_exp).group(0)) + '.*')  # регулярка для поиска ридов с делецией
        reads_with_del = re.findall(new_reg_exp, reads)
        deletion_length = str(int(re.search(r'\d*$', info).group(0)) - len(deletions[0]))  # вычисляем длину делеции
        with open('REsults.txt', 'a') as output:  # пишем в аутпут
            print('\n Regular expression:', reg_exp,
                  '\n               Info:', info,
                  '\n    Deletion length:', deletion_length,
                  '\n    Amount of calls:', len(deletions),
                  '\nReads with deletion:', reads_with_del, file=output)


start_time = datetime.now()  # запуск таймера

for s in reg_exp_file:
    info = str(re.split(r're:', s)[0])[:-1]  # парсим регулярки и сопровождающую инфу
    reg_exp = re.split(r're:', s)[1]
    reg_exp = reg_exp[:-1]
    # print(info)
    # print(reg_exp)
    re_search(reg_exp, info)

print('Полное время: ' + str(datetime.now() - start_time))
