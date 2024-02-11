import argparse

def little_to_big_endian(input_file, output_file):
    with open(input_file, 'rb') as f:

        data = f.read()


    data_big_endian = data[::-1]

    with open(output_file, 'wb') as f:
     
        f.write(data_big_endian)

if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(description="Convert a little endian file to big endian")
    parser.add_argument("input_file", help="Input file Name(little endian)")
    parser.add_argument("output_file", help="Output file name(big endian)")

 
    args = parser.parse_args()
    little_to_big_endian(args.input_file, args.output_file)
