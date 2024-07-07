import pandas as pd
import os

# Define the folder containing the CSV files
folder_path = 'data/'


# Function to read, transform, and save CSV files
def transform_and_save_csv(file_path, prefix):
    # Read the CSV file with the specified delimiter and encoding
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8-sig')


    print(df)
    print('--------------------')

    # Remove the prefix from the file name
    file_name = os.path.basename(file_path)
    new_file_name = file_name.replace(prefix, '')

    # Save the transformed data to a new CSV file with comma delimiter and UTF-8 encoding
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    df.to_csv(new_file_path, index=False, encoding='utf-8', sep=',')
    print(f"Transformed file saved: {new_file_path}")


# Common prefix to remove
prefix = 'Sheet 1-'

# Iterate over all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.startswith(prefix) and file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        transform_and_save_csv(file_path, prefix)

print("All files have been transformed and saved.")
