import os
import subprocess
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, BaggingRegressor
from sklearn.metrics import mean_squared_error


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

    # if archive_type == 'winrar':
    #     command = ['', 'a', output_file, file_path]
    # elif archive_type == '7z':
    #     command = ['', 'a', output_file, file_path]
    # elif archive_type == 'bandizip':
    #     command = ['', 'a', output_file, file_path]
    # elif archive_type == 'peazip':
    #     command = ['', 'a', output_file, file_path]
    # elif archive_type == 'izarc':
    #     command = ['', 'a', output_file, file_path]
    # elif archive_type == 'haozip':
    #     command = ['', 'a', output_file, file_path]
    # elif archive_type == 'b1':
    #     command = ['', 'a', output_file, file_path]
    # elif archive_type == 'hamster':
    #     command = ['', 'a', output_file, file_path]

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
    if output_file:
        elapsed_time = time.time() - start_time
        archive_size = os.path.getsize(output_file)
        return elapsed_time, archive_size
    else:
        return None, None


def collect_data(file_path, archive_types, percentages):
    data = []
    for archive_type in archive_types:
        for percentage in percentages:
            truncated_file = truncate_file(file_path, percentage)
            elapsed_time, archive_size = measure_time_and_size(truncated_file, archive_type)
            if elapsed_time is not None and archive_size is not None:
                data.append({
                    'archive_type': archive_type,
                    'percentage': percentage,
                    'elapsed_time': elapsed_time,
                    'archive_size': archive_size
                })
    return pd.DataFrame(data)


def choose_top_n_smallest(df, n):
    return df.nsmallest(n, 'archive_size')


def compress(data, archive_type, percentage, model):
    return len(data) * (100 - percentage) // 100


def optimize_params(data, models, selected_archive_types, percentages):
    best_archive_type = None
    best_percentage = None
    best_model = None
    best_result = float('inf')

    for archive_type in selected_archive_types:
        for percentage in percentages:
            for model in models:
                try:
                    compressed_size = compress(data, archive_type, percentage, model)
                    if compressed_size < best_result:
                        best_result = compressed_size
                        best_archive_type = archive_type
                        best_percentage = percentage
                        best_model = model
                except Exception as e:
                    print(f"Ошибка при сжатии {archive_type} с процентом {percentage} и моделью {model}: {e}")
                    continue

    if best_archive_type is None or best_percentage is None or best_model is None:
        print("Не удалось найти оптимальные параметры.")
        return None, None, None

    return best_archive_type, best_percentage, best_model


def adaptive_compression(file_path, archive_types, initial_percentage, increment_percentage, top_n, steps, models):
    percentages = [initial_percentage + i * increment_percentage for i in range(steps)]
    data = collect_data(file_path, archive_types, percentages)
    if data.empty:
        print("No data collected, please check the archive commands and input files.")
        return None, None, None

    data['archive_type'] = data['archive_type'].astype('category').cat.codes

    X = data[['archive_type', 'percentage']]
    y = data['archive_size']

    if len(X) > 1:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        for model in models:
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            mse = mean_squared_error(y_test, predictions)
            print(f'Model: {model.__class__.__name__}, MSE: {mse}')

        avg_predictions = sum([model.predict(X_test) for model in models]) / len(models)
        avg_mse = mean_squared_error(y_test, avg_predictions)
        print(f'Average MSE: {avg_mse}')

    top_n_smallest = choose_top_n_smallest(data, top_n)
    selected_archive_types = top_n_smallest['archive_type'].apply(lambda x: archive_types[x]).tolist()

    best_archive_type, best_percentage, best_model = optimize_params(data, models, selected_archive_types, percentages)
    truncated_file = truncate_file(file_path, best_percentage)
    archive_file(truncated_file, best_archive_type)
    return best_archive_type, best_percentage, best_model


def main():
    file_path = ''
    archive_types = ['bmf', 'durilca', 'emma', 'katy', 'kvick', 'lac', 'lea', 'lily', 'lua', 'lznv', 'ppmd', 'ppmonstr']
    initial_percentage = 1
    increment_percentage = 1
    top_n = 3
    steps = 5

    models = [
        RandomForestRegressor(n_estimators=100, random_state=42),
        GradientBoostingRegressor(n_estimators=100, random_state=42),
        BaggingRegressor(n_estimators=100, random_state=42)
    ]

    best_archive_type, best_percentage, best_model = adaptive_compression(file_path, archive_types, initial_percentage,
                                                                          increment_percentage, top_n, steps, models)
    if best_archive_type and best_percentage:
        print(f'Best archive type: {best_archive_type}, Best percentage: {best_percentage}')
        print(f'Best model: {best_model}')


if __name__ == "__main__":
    main()
