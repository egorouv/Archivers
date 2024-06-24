import os
import subprocess
import time


def truncate_file(input_file_path, percentage):
    abs_input_file_path = os.path.abspath(input_file_path)
    dir_name, file_name = os.path.split(abs_input_file_path)
    output_file_path = os.path.join(dir_name, f'truncated_{file_name}')

    with open(abs_input_file_path, 'rb') as input_file:
        content = input_file.read()
        truncated_content = content[:len(content) * percentage // 100]

    with open(output_file_path, 'wb') as output_file:
        output_file.write(truncated_content)

    return os.path.abspath(output_file_path)


def archive_file(file_path, archive_type):
    output_file = os.path.splitext(file_path)[0] + ".zip"
    command = None

    if archive_type == 'bmf':
        command = ['', file_path, output_file]
    elif archive_type == 'durilca':
        command = ['', file_path, output_file]
    elif archive_type == 'emma':
        command = ['', file_path, output_file]
    elif archive_type == 'katy':
        command = ['', file_path, output_file]
    elif archive_type == 'kvick':
        command = ['', 'c', file_path, output_file]
    elif archive_type == 'lac':
        command = ['', '-c', file_path, output_file]
    elif archive_type == 'lea':
        command = ['', file_path, output_file]
    elif archive_type == 'lily':
        command = ['', file_path, output_file]
    elif archive_type == 'lua':
        command = ['', file_path, output_file]
    elif archive_type == 'lznv':
        command = ['', file_path, output_file]
    elif archive_type == 'ppmd':
        command = ['', file_path, output_file]
    elif archive_type == 'ppmonstr':
        command = ['', file_path, output_file]

    if command:
        try:
            print(f'Running command: {" ".join(command)}')
            subprocess.run(command, check=True)
            if os.path.exists(output_file):
                return output_file
            else:
                print(f'Output file {output_file} not found after running command: {" ".join(command)}')
                return None
        except subprocess.CalledProcessError as e:
            print(f'Command {command} failed with error: {e}')
            return None
    else:
        print(f'No command found for archive type: {archive_type}')
        return None


def measure_time_and_size(file_path, archive_type):
    start_time = time.time()
    output_file = archive_file(file_path, archive_type)
    elapsed_time = time.time() - start_time

    if output_file and os.path.exists(output_file):
        archive_size = os.path.getsize(output_file)
        return elapsed_time, archive_size
    else:
        print(f"Failed to archive using {archive_type}. No output file created.")
        return elapsed_time, None


def choose_top_n_smallest(sizes_dict, n):
    return dict(sorted((k, v) for k, v in sizes_dict.items() if v is not None)[:n])


def main():
    file_path = ''
    archive_types = ['bmf', 'durilca', 'emma', 'katy', 'kvick', 'lac', 'lea', 'lily', 'lua', 'lznv', 'ppmd', 'ppmonstr']

    truncated_file_1_percent = truncate_file(file_path, 1)
    sizes_dict_1_percent = {}

    for archive_type in archive_types:
        _, archive_size = measure_time_and_size(truncated_file_1_percent, archive_type)
        sizes_dict_1_percent[archive_type] = archive_size

    top_3_smallest = choose_top_n_smallest(sizes_dict_1_percent, 3)

    print("\nTop 3 smallest archives (1% file):")
    for archive_type, archive_size in top_3_smallest.items():
        print(f'{archive_type}: {archive_size} bytes')

    truncated_file_5_percent = truncate_file(file_path, 5)
    best_archive_type = None
    best_time = float('inf')

    for archive_type in top_3_smallest:
        elapsed_time, _ = measure_time_and_size(truncated_file_5_percent, archive_type)
        print(f'{archive_type} took {elapsed_time:.2f} seconds')
        if elapsed_time < best_time:
            best_time = elapsed_time
            best_archive_type = archive_type

    print(f'\nBest archive type: {best_archive_type} ({best_time:.2f} seconds)')

    print(f'Archiving the entire file using {best_archive_type}...')
    archive_file(file_path, best_archive_type)


if __name__ == "__main__":
    main()
