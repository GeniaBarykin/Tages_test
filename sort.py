import os
import heapq

def split_and_sort_file(input_file, chunk_size):
    temp_files = []
    with open(input_file, 'r', encoding='utf-8') as f:
        while True:
            lines = []
            while len(lines) * os.sys.getsizeof('') < chunk_size:
                line = f.readline()
                if not line:
                    break
                lines.append(line.strip())
            if not lines:
                break

            # Сортируем текущую часть
            lines.sort()

            # Сохраняем отсортированные строки во временный файл
            temp_file = 'temp_{}.txt'.format(len(temp_files))
            with open(temp_file, 'w', encoding='utf-8') as temp_f:
                temp_f.write('\n'.join(lines))
            temp_files.append(temp_file)

    return temp_files


def merge_sorted_files(temp_files, output_file):
    with open(output_file, 'w', encoding='utf-8') as output_f:
        # Создаем генераторы для каждой временной части
        file_generators = [open(tf, 'r', encoding='utf-8') for tf in temp_files]
        
        # Используем кучу для слияния
        min_heap = []
        
        # Инициализируем кучу с первыми строками каждого файла
        for i, f in enumerate(file_generators):
            line = f.readline().strip()
            
            if line:
                heapq.heappush(min_heap, (line, i))  # храним кортеж (строка, индекс файла)

        while min_heap:
            smallest_line, smallest_index = heapq.heappop(min_heap)            
            next_line = file_generators[smallest_index].readline().strip()
            if next_line:
                heapq.heappush(min_heap, (next_line , smallest_index))
            if len(min_heap) > 0:
                smallest_line = smallest_line + '\n'
            output_f.write(smallest_line)  # записываем строку в выходной файл


    # Закрываем временные файлы
    for f in file_generators:
        f.close()

def sort_large_file(input_file, output_file,chunck_size):
    temp_files = split_and_sort_file(input_file, chunck_size)
    merge_sorted_files(temp_files, output_file)
    for temp_file in temp_files:
        os.remove(temp_file)


input_file = 'file.txt'  # Путь к входному файлу
output_file = 'sorted_file.txt'  # Путь к выходному файлу
chunck_size = 450 * 1024 * 1024
sort_large_file(input_file, output_file, chunck_size)

