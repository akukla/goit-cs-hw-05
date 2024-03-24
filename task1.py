import asyncio
import argparse
import os
from aiofile import AIOFile
from shutil import copy2

# Create ArgumentParser object
parser = argparse.ArgumentParser(description="Sort files based on their extensions.")
parser.add_argument('source_folder', type=str, help='Source folder path')
parser.add_argument('output_folder', type=str, help='Output folder path')
parser.print_help()

try:
    args = parser.parse_args()
except SystemExit:
    exit()


# Initialize source and output paths
source_folder = args.source_folder
output_folder = args.output_folder

# Asynchronous function to read files from source folder
async def read_folder(read_path, result_folder_path):
    # Check if source folder exists
    if not os.path.exists(read_path):
        print(f"Error: The source folder '{read_path}' does not exist.")
        exit()

    # Check if output folder exists, if not, try to create it
    if not os.path.exists(result_folder_path):
        try:
            os.makedirs(result_folder_path)
        except Exception as e:
            print(f"Error: The output folder '{result_folder_path}' could not be created. {str(e)}")
            exit()

    copies = []
    for root, dirs, files in os.walk(read_path):
        for file in files:
            copies.append(copy_file(os.path.join(root, file))) 
    await asyncio.gather(*copies)

# Asynchronous function to copy file to the appropriate subfolder in the output folder
async def copy_file(file_path):
    file_extension = os.path.splitext(file_path)[1][1:]
    destination_folder = os.path.join(output_folder, file_extension)

    print(f"Copying file: {file_path} to {destination_folder}  {file_extension}")

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_path = os.path.join(destination_folder, os.path.basename(file_path))

    async with AIOFile(file_path, 'rb') as afp:
        data = await afp.read()
        async with AIOFile(destination_path, 'wb') as afp_write:
            await afp_write.write(data)

# Main block
if __name__ == "__main__":
    try:
        asyncio.run(read_folder(source_folder, output_folder))
    except Exception as e:
        print(f"An error occurred: {e}")