import random

## КОНФИГУРАЦИЯ
read_len = 100  # длина тестовых ридов
del_len = random.randrange(10, 20, 1)  # длина делеции в нуклеотидах (от,до,шаг)
del_percentage = 5  # процент тестовых ридов с делециями
number_reads = 1000  # число ридов (сумма изначальных и с делецией)
complementary_percentage = 50  # процент тестовых ридов с делециями, сделанных с комплементарной цепи

## !!КАЖДЫЙ ЗАПУСК ЗАТИРАЕТ ФАЙЛЫ answer.txt, output_testing_reads.txt!!
with open('sequence.fasta') as f:
    input_sequence = f.read()
input_list = list(input_sequence)
input_list_len = len(input_list)
input_list_for_del = input_list[:]  ## создаём копию листа для работы в функции

del_start = random.randrange(0, input_list_len - 100, 1)  # # случайная координата начала делеции и точка считывания в
# цикле ниже, точка старта - не позднее чем за 100 элементов до конца последовательности (костыль)
del_end = del_start + del_len  ## random.randrange(10,15,1) - длина проверочной делеции, c - координата конца делеции
with open('test_answer.txt',
          'w') as answer:  ## выводит координаты в файл answer.txt для проверки, предварительно затирает файл на случай, если там уже есть данные
    print(del_start, del_end, file=answer)  # нумерация Питона (от человеческой -1)
del input_list_for_del[del_start:del_end]

del_list = input_list[del_start:del_end]
noncompl_del_list = input_list_for_del[:]  # копия
del_string = ''.join(del_list)
list_for_answer_left = input_list[del_start - 50:del_start]
list_for_answer_right = input_list[del_end:del_end + 50]
answer_left = ''.join(list_for_answer_left)
answer_right = ''.join(list_for_answer_right)
with open('test_answer.txt', 'a') as answer:  ## выводит делецию в файл answer.txt для проверки
    print(answer_left, del_string, answer_right, file=answer)

# для тестовых нужд
# print (sequence_with_deletion_straight)

sequence_with_deletion_straight = ''.join(noncompl_del_list)


# создание комплементарной строки

def complementary_conversion(noncompl_del_list):
    input_list_for_del_compl = str('')
    complementary_list = [['A', 'T'], ['T', 'A'], ['G', 'C'], ['C', 'G'], ['M', 'K'], ['K', 'M'], ['R', 'Y'],
                          ['Y', 'R'], ['W', 'W'], ['S', 'S'], ['B', 'V'], ['V', 'B'], ['H', 'D'], ['D', 'H'],
                          ['N', 'N']]
    for letter in noncompl_del_list:
        for a in complementary_list:
            if letter == a[0]:
                input_list_for_del_compl += a[1]
                break
    return input_list_for_del_compl


sequence_with_deletion_compl = complementary_conversion(noncompl_del_list)


# print (sequence_with_deletion_compl) # тестовый

## создали случайную делецию, нарежем несколько ридов, куда она ранее входила


def generate_read_with_del(del_start):
    read_bias = random.randrange(0, 50, 1)  ## начало рида за 0-50 нуклеотидов до начала делеции
    read_start = del_start - read_bias - del_len  ## возвращаем в точку начала делеции и вычитаем случайное число d
    read_end = read_start + read_len  ## конец рида - точка начала + длина рида
    if read_start < 0:  ## если координата начала рида из-за вычитания b - 10 - d вышла отрицательной - приравниваем её к 0
        read_start = 0
    complementary_path = random.randrange(1, 100)
    if complementary_path <= complementary_percentage:
        a = sequence_with_deletion_straight[read_start:read_end + 1]
    else:
        b = sequence_with_deletion_compl[read_start:read_end + 2]
        a = b[::-1]
    string_read_with_del = ''.join(a)
    return (string_read_with_del)


def generate_read_without_del():
    sequence_length = len(input_list)
    clearread_start = random.randrange(0, sequence_length - read_len, 1)
    clearread_end = clearread_start + read_len
    list_read_without_del = input_sequence[clearread_start:clearread_end]
    string_read_without_del = ''.join(list_read_without_del)
    return (string_read_without_del)


### Мы открываем казино
with open('test_output_reads.txt', 'w') as output:  ## !!ОСТОРОЖНО, ЗАТИРАЕТ ФАЙЛ test_output_reads.txt!!
    print('')
a = 0
while number_reads != 0:
    number_reads = number_reads - 1
    path = random.randrange(1, 100)
    if path > del_percentage:
        output_read = generate_read_without_del()
        with open('test_output_reads.txt', 'a') as output:
            output.write(output_read + '\n')
    else:
        output_read = generate_read_with_del(del_start)
        with open('test_output_reads.txt', 'a') as output:
            output.write(output_read + '\n')
        a = a + 1

with open('test_answer.txt', 'a') as answer:  ## выводит количество делеций
    print("АНДРЮХА, У НАС", a, "РИДОВ, ВОЗМОЖНА ДЕЛЕЦИЯ, ПО КОНЯМ", file=answer)
print('Done!')
## j = 10 ## число тестовых ридов
## while j != 0:
##    read = generate_read(del_start)
##    read_without_del = read.replace(del_string,'')
##    j = j-1
##    print(read_without_del)