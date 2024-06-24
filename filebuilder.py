import os


def replicate_file(file_path, num_replications=500):
    with open(input_file_path, 'rb') as input_file:
        content = input_file.read()

    replicated_content = content * num_replications
    dir_name, file_name = os.path.split(file_path)
    output_file_path = os.path.join(dir_name, f'new_{file_name}')

    with open(output_file_path, 'wb') as output_file:
        output_file.write(replicated_content)

    return os.path.abspath(output_file_path)


if __name__ == "__main__":
    input_file_path = ''

    new_file_path = replicate_file(input_file_path)
    print(f'Новый файл создан: {new_file_path}')
