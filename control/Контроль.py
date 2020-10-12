import random
import multiprocessing
import sys
sys.stdout = open('output_deletion_for_RESearch.txt', 'w')
print('')
sys.stdout = open('output_deletion_for_RESearch.txt', 'a')
from multiprocessing import Pool
from datetime import datetime

start_time = datetime.now()  # запуск таймера

## КОНФИГУРАЦИЯ
read_len = 100  # длина тестовых ридов
del_len = 100  # длина делеции в нуклеотидах (от,до,шаг)
del_percentage = 25  # процент тестовых ридов с делециями
number_reads = 1000 # число ридов (сумма изначальных и с делецией)
complementary_percentage = 0 # процент тестовых ридов с делециями, сделанных с комплементарной цепи
N_chance = 10 # процент тестовых ридов (всех) с заменой части нуклеотидов на N


## !!КАЖДЫЙ ЗАПУСК ЗАТИРАЕТ ФАЙЛЫ answer.txt, output_testing_reads.txt!!
with open('sequence.fasta') as f:
    input_sequence = f.read()
input_list_len = len(input_sequence)

del_start = random.randrange(0, input_list_len - read_len, 1)  # # случайная координата начала делеции и точка считывания в
# цикле ниже, точка старта - не позднее чем за 100 элементов до конца последовательности (костыль)
del_end = del_start + del_len  ## random.randrange(10,15,1) - длина проверочной делеции, c - координата конца делеции
with open('test_answer.txt',
          'w') as answer:  ## выводит координаты в файл answer.txt для проверки, предварительно затирает файл на случай, если там уже есть данные
    print(del_start, del_end, file=answer)  # нумерация Питона (от человеческой -1)
string_with_deletion = input_sequence[0:del_start] + input_sequence[del_end:-1]
del_string = input_sequence[del_start:del_end]
#noncompl_del_list = input_list_for_del[:] # копия
list_for_answer_left = string_with_deletion[del_start - 50:del_start]
list_for_answer_right = string_with_deletion[del_start:del_start + 50]
answer_left = ''.join(list_for_answer_left)
answer_right = ''.join(list_for_answer_right)
with open('test_answer.txt', 'a') as answer:  ## выводит делецию в файл answer.txt для проверки
    print(answer_left, del_string, answer_right, file=answer)
    
# для тестовых нужд
#print (sequence_with_deletion_straight)

#sequence_with_deletion_straight = ''.join (noncompl_del_list)

# создание комплементарной строки 

def complementary_conversion():
    with open('sequence.fasta') as f:
        input_sequence_func = f.read()
    string_with_deletion_func = input_sequence_func[0:del_start] + input_sequence_func[del_end:-1]
    input_list_for_del_compl = str('')
    complementary_list = [['A', 'T'], ['T', 'A'], ['G', 'C'], ['C', 'G'],['M', 'K'], ['K', 'M'], ['R', 'Y'], ['Y', 'R'], ['W', 'W'], ['S', 'S'],['B', 'V'], ['V', 'B'], ['H', 'D'], ['D', 'H'], ['N', 'N']]
    for letter in string_with_deletion_func:
        for a in complementary_list:
            if letter == a[0]:
                input_list_for_del_compl += a[1]
                break
    return input_list_for_del_compl
#print (sequence_with_deletion_compl) # тестовый

## создали случайную делецию, нарежем несколько ридов, куда она ранее входила


def generate_read_with_del(x):
    with open('sequence.fasta') as f:
        input_sequence_func = f.read()
    string_with_deletion_func = input_sequence_func[0:del_start] + input_sequence_func[del_end:-1] 
    read_bias = random.randrange(0, 50, 1)  ## начало рида за 0-50 нуклеотидов до начала делеции
    read_start = del_start - read_bias  ## возвращаем в точку начала делеции и вычитаем случайное число d
    read_end = read_start + read_len  ## конец рида - точка начала + длина рида
    if read_start < 0:  ## если координата начала рида из-за вычитания b - 10 - d вышла отрицательной - приравниваем её к 0
        read_start = 0
    complementary_path = random.randrange (1,100)
    if complementary_path >= complementary_percentage:
        a = string_with_deletion_func[read_start:read_end + 1]
    else:
        sequence_with_deletion_compl = complementary_conversion()
        b = sequence_with_deletion_compl[read_start:read_end + 2]
        a = b[::-1]
    string_read_with_del = ''.join(a)
    return (string_read_with_del)


def generate_read_without_del(x):
    with open('sequence.fasta') as f:
        input_sequence_func = f.read()
    string_with_deletion_func = input_sequence_func[0:del_start] + input_sequence_func[del_end:-1] 
    sequence_length = len(string_with_deletion_func)
    clearread_start = random.randrange(0, sequence_length - read_len, 1)
    clearread_end = clearread_start + read_len
    list_read_without_del = string_with_deletion_func[clearread_start:clearread_end]
    string_read_without_del = ''.join(list_read_without_del)
    return (string_read_without_del)

if __name__ == "__main__":
    num_proc = multiprocessing.cpu_count() - 1
    number_reads_without_del = round((number_reads*(100-del_percentage))/100)
    number_reads_with_del = round((number_reads*(0+del_percentage))/100)
    if num_proc <= 1:
        work_pool_del = Pool(1)
        work_pool_without = Pool(1)
    if 1<num_proc<4:
        work_pool_del = Pool(1)
        work_pool_without = Pool(2)
    if 4<num_proc<6:
        work_pool_del = Pool(1)
        work_pool_without = Pool(3)
    if 6<num_proc:
        work_pool_del = Pool(round(num_proc*0.25))
        work_pool_without = Pool(round(num_proc*0.75))
    without_del_list = work_pool_without.map(generate_read_without_del, (range(1,number_reads_without_del,1)))
    with_del_list =  work_pool_del.map(generate_read_with_del, (range(1,number_reads_with_del,1)))
    end = '\n'.join(without_del_list)
    del_end = '\n'.join(with_del_list)
    with open ('output_deletion_for_RESearch.txt', 'a') as output:
        print(del_end)
        print(end)

# with open('test_output_reads.txt', 'w') as output:  ## !!ОСТОРОЖНО, ЗАТИРАЕТ ФАЙЛ test_output_reads.txt!!
#     print('')
# a = 0
# while number_reads != 0:
#     number_reads = number_reads - 1
#     path = random.randrange(1, 100)
#     if path > del_percentage:
#         output_read = generate_read_without_del(1)
#         with open('test_output_reads.txt', 'a') as output:
#             output.write(output_read + '\n')
#     else:
#         output_read = generate_read_with_del()
#         with open('test_output_reads.txt', 'a') as output:
#             output.write(output_read + '\n')
#a = number_reads*(((0+del_percentage))/100)
#with open('test_answer.txt', 'a') as answer:  ## выводит количество делеций
#    print("АНДРЮХА, У НАС", a, "РИДОВ, ВОЗМОЖНА ДЕЛЕЦИЯ, ПО КОНЯМ", file=answer)
#    print('Done!')
 #   print('Полное время: ' + str(datetime.now() - start_time))

## j = 10 ## число тестовых ридов
## while j != 0:
##    read = generate_read(del_start)
##    read_without_del = read.replace(del_string,'')
##    j = j-1
##    print(read_without_del)
