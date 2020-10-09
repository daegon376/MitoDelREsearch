from datetime import datetime
import re
import os

start_time = datetime.now()
cwd = str(os.getcwd())
nuc_seq_path = str(cwd + '\\refseq\\genome.txt')

with open('RE.txt') as re_file:
    x = int(1)
    for re_line in re_file:
        with open(nuc_seq_path, 'r') as genome_file:
            calls = int(0)
            for line in genome_file:
                if not line.startswith('>') and line != '\n':
                    regexp = re.split(r're:', re_line)[1][:-1]
                    calls += len(re.findall(regexp, line))

        print('время: ' + str(datetime.now() - start_time))
        print(str(x) + '. calls: ' + str(calls) + '. ' + re_line)
        with open('log_CDREvsNUC.txt', 'a') as output_file:
            output_file.write(str(x) + '. calls: ' + str(calls) + '. ' + re_line)
        if calls >> 1:
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        x += 1



print('Полное время: ' + str(datetime.now() - start_time))
