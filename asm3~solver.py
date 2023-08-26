import os
import requests

def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

def generate_c_code(numbers):
    c_code = f"""
#include <stdio.h>

int asm3(int a, int b, int c);

int main(void) {{
    printf("0x%x\\n", asm3({', '.join(numbers)}));
    return 0;
}}
"""
    with open('main.c', 'w') as file:
        file.write(c_code)

def compile_files():
    os.system("gcc -masm=intel -m32 -c run.S -o run.o")
    os.system("gcc -m32 -c main.c -o main.o")
    os.system("gcc -m32 run.o main.o -o solve")

def process_asm_file(input_filename, output_filename):
    with open(input_filename, 'r') as input_file:
        lines = input_file.readlines()

    with open(output_filename, 'w') as output_file:
        output_file.write(".intel_syntax noprefix\n")
        output_file.write(".global asm3\n")
        output_file.write("asm3:\n")
        for line in lines:
            instruction = line[line.find(":") + 1:].strip()
            output_file.write(f"    {instruction}\n")

    print("Modified assembly code has been written to", output_filename)

if __name__ == "__main__":
    input_filename = "test.S"
    output_filename = "run.S"
    url = input("Enter the URL: ")
    
    try:
        download_file(url, input_filename)
        numbers = input("Enter the numbers separated by spaces: ").split()
        
        generate_c_code(numbers)
        process_asm_file(input_filename, output_filename)
        compile_files()
        
        os.system("./solve")
        
    except Exception as e:
        print("An error occurred:", str(e))
