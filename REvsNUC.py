from datetime import datetime
import re
import os

start_time = datetime.now()
cwd = str(os.getcwd())  # берем путь к текущей папке (где лежит скрипт)
nuc_seq_path = str(cwd + '\\refseq\\genome.txt')  # путь к хуман геному без переноса строк

with open('RE.txt') as re_file:
        for re_line in re_file:
        with open(nuc_seq_path, 'r') as genome_file:  # открыли хумангеном на чтение
            calls = int(0)
            for line in genome_file:  # итерируем строки в файле хуман генома
                if not line.startswith('>') and line != '\n':  # если строка НЕ заголовок и НЕ состоит
                                                               # из одного переноса, то это строка с хромосомной
                                                               # последовательностью, дальше делаем с ней что хотим
                    regexp = re.split(r're:', re_line)[1][:-1]
                    calls += len(re.findall(regexp, line))

        print(str(x) + '. calls: ' + str(calls) + '. ' + re_line)
        with open('log_CDREvsNUC.txt', 'a') as output_file:
            output_file.write(str(x) + '. calls: ' + str(calls) + '. ' + re_line)
        if calls >> 1:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        

print('Полное время: ' + str(datetime.now() - start_time))
