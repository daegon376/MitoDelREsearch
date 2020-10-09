import os
from multiprocessing import Process
from datetime import datetime
import re
from itertools import islice

def split_every(n, iterable):
    i = iter(iterable)
    piece = list(islice(i, n))
    while piece:
        yield piece
        piece = list(islice(i, n))

def re_search(re_list, reads):
    for s in re_list:
        info = str(re.split(r're:', s)[0])[:-1]  # парсим регулярки и сопровождающую инфу
        reg_exp = re.split(r're:', s)[1]
        reg_exp = reg_exp[:-1]
        pattern = re.compile(reg_exp)
        deletions = pattern.findall(reads)
        if len(deletions) != 0:  # если что-то нашли
            new_reg_exp = str('.*' + str(re.split(r'\W\WATGCN\W\W0.\d{1,3}\W\W', reg_exp)[0]) + deletions[0] +
                              str(re.split(r'\W\WATGCN\W\W0.\d{1,3}\W\W', reg_exp)[1]) + '.*')  # регулярка для поиска ридов с делецией
            reads_with_del = re.findall(new_reg_exp, reads)
            amount_of_finded_reads = str(len(reads_with_del))
            deletion_length = str(int(re.search(r'\d*$', info).group(0)) - len(deletions[0]))  # вычисляем длину делеции
            with open('REsults_multiproc.txt', 'a') as output:  # пишем в аутпут
                print('\n Regular expression:', reg_exp,
                      '\n               Info:', info,
                      '\n    Deletion length:', deletion_length,
                      '\n    Amount of calls:', len(deletions),
                      '\nReads with deletion:', amount_of_finded_reads, reads_with_del, file=output)

if __name__ == '__main__':
    start_time = datetime.now()  # запуск таймера

    cwd = os.getcwd()

    reg_exp_file = open('RE.txt')
    reads_file = open(cwd + '\\control\\test_output_reads.txt')
    f = open('REsults_multiproc.txt', 'w')
    f.write('')  # clean output
    reads = str()  # все риды записываем в одну строку
    for s in reads_file:
        reads = str(reads + s)

    n = int(0)
    reg_exp_l = []
    for s in reg_exp_file:
        reg_exp_l.append(s)
        n += 1

    number_to_split = (n//6) + 1
    splited_re = list(split_every(number_to_split, reg_exp_l))

    procs = []

    for re_list in splited_re:
        proc = Process(target=re_search, args=(re_list, reads))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
    print('Полное время: ' + str(datetime.now() - start_time))