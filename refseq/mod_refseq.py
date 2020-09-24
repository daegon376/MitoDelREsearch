import csv
import re

def row_parser(row):
    replacement = []
    s = []
    s = re.split(r':', row[0])
    coord = int(s[1])  # вытащили коордиаты
    replacement.append(coord)

    s = re.split(r',', row[1][1:-1])
    vars = []
    for i in s:
        vars.append(i[1:-1])  # вытащили варианты
    fin_letter = str()
    if len(vars) == 2:
        if len(vars[0]) == 1 and len(vars[1]) == 1:
            if vars.count('A') >> 0:
                if vars.count('C') >> 0:
                    fin_letter = 'M'  #AC
                elif vars.count('G') >> 0:
                    fin_letter = 'R'  #AG
                elif vars.count('T') >> 0:
                    fin_letter = 'W'  #AT
            elif vars.count('G') >> 0:
                if vars.count('C') >> 0:
                    fin_letter = 'S'  #GC
                elif vars.count('T') >> 0:
                    fin_letter = 'K'  #GT
            elif vars.count('T') >> 0 and vars.count('C') >> 0:
                fin_letter = 'Y'  #TC

    replacement.append(fin_letter)
    return replacement

def replacer (seq, replacements):
    for r in replacements:
        coords = int(r[0]) - 1  # уменьшаем на 1, т.к. индексы питона
        letter = r[1]
        seq = str(seq[:coords] + letter + seq[coords+1:])
    new_seq = seq

    return new_seq

replacements = []
with open('polymorphisms.csv') as csvfile:
    pm_sheet = csv.reader(csvfile, delimiter=';')
    x = int(0)  # счетчик для пропуска головы таблицы
    for row in pm_sheet:
        if x == 0:  # пропускаем первую строку таблицы
            x =+ 1
        else:
            replacements.append(row_parser(row))

with open('sequence.fasta') as seq_inp_file:
    sequence = str()
    x = int(0)  # счетчик для пропуска первой строки
    for s in seq_inp_file:
        if x == 0:  # пропускаем первую строку
            x = + 1
        else:
            sequence = str(sequence + str(s[:-1]))

with open('modified_refseq.fasta', 'w') as output_file:
    output_file.write(replacer(sequence, replacements))

print(replacements)
print('RefSeq is successfully modified!')



