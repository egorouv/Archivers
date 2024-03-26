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
    if archive_type == 'winrar':
        subprocess.run(['D:\\Programs\\Archivers\\WinRAR\\WinRAR.exe', 'a', 'archive.zip', file_path])
    elif archive_type == '7z':
        subprocess.run(['D:\\Programs\\Archivers\\7zip\\7-Zip\\7z.exe', 'a', 'archive.zip', file_path])
    elif archive_type == 'bandizip':
        subprocess.run(['D:\\Programs\\Archivers\\Bandizip\\Bandizip.exe', 'a', 'archive.zip', file_path])
    elif archive_type == 'peazip':
        subprocess.run(['D:\\Programs\\Archivers\\PeaZip\\peazip.exe', 'a', 'archive.zip', file_path])
    elif archive_type == 'izarc':
        subprocess.run(['D:\\Programs\\Archivers\\IZArc\\IZArc.exe', 'a', 'archive.zip', file_path])
    elif archive_type == 'haozip':
        subprocess.run(['D:\\Programs\\Archivers\\HaoZip\\HaoZip.exe', 'a', 'archive.zip', file_path])
    elif archive_type == 'b1':
        subprocess.run(['D:\\Programs\\Archivers\\B1\\B1 Free Archiver\\B1Manager.exe', 'a', 'archive.zip', file_path])
    elif archive_type == 'hamster':
        subprocess.run(['D:\\Programs\\Archivers\\Hamster\\hamsterziparchiver.exe', 'a', 'archive.zip', file_path])


def measure_time(file_path, archive_type):
    start_time = time.time()
    archive_file(file_path, archive_type)
    elapsed_time = time.time() - start_time
    return elapsed_time


def choose_top_n_fastest(times_dict, n):
    return dict(sorted(times_dict.items(), key=lambda x: x[1])[:n])


def main():
    file_path = 'D:\\source\\Archivers\\new_file.txt'
    archive_types = ['winrar', '7z', 'bandizip', 'peazip', 'izarc', 'haozip', 'b1', 'hamster']

    best_archive_type = None
    best_time = float('inf')

    times_dict = {}
    truncated_file = truncate_file(file_path, 1)

    for archive_type in archive_types:
        elapsed_time = measure_time(truncated_file, archive_type)
        print(f'{archive_type} took {elapsed_time:.2f} seconds')
        times_dict[archive_type] = elapsed_time

    top_n_fastest = choose_top_n_fastest(times_dict, 3)
    print("\nTop 3 fastest archivers:")
    for archive_type, elapsed_time in top_n_fastest.items():
        print(f'{archive_type}: {elapsed_time:.2f} seconds')
    print()

    truncated_file = truncate_file(file_path, 5)

    for archive_type in top_n_fastest:
        elapsed_time = measure_time(truncated_file, archive_type)
        print(f'{archive_type} took {elapsed_time:.2f} seconds')
        times_dict[archive_type] = elapsed_time

        if elapsed_time < best_time:
            best_time = elapsed_time
            best_archive_type = archive_type

    print(f'\nBest archive type: {best_archive_type} ({best_time:.2f} seconds)')
    print(f'Archiving the entire file using {best_archive_type}...')
    archive_file(file_path, best_archive_type)


if __name__ == "__main__":
    main()
