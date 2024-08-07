import os
import json
import argparse
import srv
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input folder")
parser.add_argument("-o", "--output", help="Output folder")

args = parser.parse_args()

if args.input == None:
	print("Input not specified.")
	sys.exit()
else:
	input_dir = args.input

if args.output == None:
	current_directory = os.getcwd()
	output_directory = os.path.join(current_directory, r'output')
	if not os.path.exists(output_directory):
		os.makedirs(output_directory)
	output_dir = output_directory
else:
	output_dir = args.output

output_path = os.path.join(output_dir,"output.xlsx")

to_convert = []

for f in os.listdir(input_dir):
    if f.endswith(".json"):
        to_convert.append(os.path.join(input_dir, f))

servers = []

for path in to_convert:
	servers.append(srv.ReportRecord(srv.Server(path)))

df = pd.DataFrame([rec.__dict__ for rec in servers]).astype('str')



print(list(df.columns))

df[list(df.columns)] = df[list(df.columns)].replace({'{': ''}, regex=True)
df[list(df.columns)] = df[list(df.columns)].replace({'}': ''}, regex=True)


print(df)

df.to_excel(output_path, sheet_name='Hardware', index=False)
