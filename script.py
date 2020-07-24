from datetime import datetime
import time

input_file = open('input.fasta')
f = open('output.txt', 'w')
f.write('')  # clean output

full_seq = str()
for s in input_file:
    full_seq = str(full_seq + str(s[:-1]))
print('Длина полной последовательности:' + str(len(full_seq)))

# Settings
# fragment_start = int(input('Начало исследуемой области: '))  # -1 от человеческой нумерации -50
# fragment_end = int(input('Конец исследуемой области: '))  # [: этот индекс не входит в отрезок] +50
seq = full_seq  # [fragment_start:fragment_end]
# print('Последовательность в работе: ' + seq)
print('Длина исследуемой области: ' + str(len(seq)))

del_length_min = int(input('Минимальная длина делеции: '))
del_length_max = int(input('Максимальная длина делеции: '))
marg_length = int(input('Длина "боков": '))
mask_length = int(input('Длина маскирования нуклеотидов (ноль - выкл.): '))

if mask_length == 0:  # шаг по делециям != 0
    step_length = int(1)
else:
    step_length = int(2 * mask_length)

start_time = datetime.now()  # запуск таймера


def reg_exp_generator(sequence, deletion_length, margin_length=30, masking=10):
    for i in range(len(sequence) - int(deletion_length + 2 * margin_length)):
        deletion_start = int(i + margin_length)
        deletion_end = int(deletion_start + deletion_length)
        reg_exp_start = int(i)
        reg_exp_end = int(deletion_end + margin_length)
        left_margin = str(sequence[reg_exp_start:deletion_start - masking])
        right_margin = str(sequence[deletion_end + masking:reg_exp_end])
        del_info = str('del_start {0}; del_end {1}; {2} re:'.format(str(deletion_start), str(deletion_end),
                                                                    str(deletion_length + 2 * masking)))
        reg_exp_seq = left_margin + '([ATGC]{0,' + str(masking * 2) + '})' + right_margin + '\n'
        with open('output.txt', 'a') as output:
            output.write(str(del_info + reg_exp_seq))
    return


for dl in range(del_length_min, del_length_max + 1, step_length):  # тут у нас скачок по делециям
    extended_seq = str(seq + seq[:dl + 2 * marg_length])  # закольцовываем удлинняя в конце
    reg_exp_generator(extended_seq, dl, marg_length, mask_length)
    print('Время выполнения по делециям длинны ' + str(dl) + ' : ', (datetime.now() - start_time))
print('Полное время: ' + str(datetime.now() - start_time))
