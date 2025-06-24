import argparse
import pathlib
from wt_calcinmatchplaytime import calc


def main() -> None:
	parser = argparse.ArgumentParser(description="A Python CLI application that takes a TSV (or CSV) file containing your in-game match time and outputs the total playtime in hours.")
	parser.add_argument("-i", "--filename", required=True, help="TSV (or CSV) file that contains the in-match playtime. col 1 of the file is vehicle type and col 2 is time played")
	parser.add_argument("-nh", "--no-headers", help="Indicate that the input file does not have headers", action="store_true")

	force_delim = parser.add_mutually_exclusive_group()
	force_delim.add_argument("-c", "--csv", action="store_true", help="Force the CLI application to use CSV delimiters")
	force_delim.add_argument("-t", "--tsv", action="store_true", help="Force the CLI application to use TSV delimiters")

	args = parser.parse_args()
	# print(args)

	input_is_tsv = True
	if args.csv:
		input_is_tsv = False
	if args.tsv:
		input_is_tsv = True

	filepath = pathlib.Path(args.filename).resolve()
	file_exists = filepath.exists()

	# print(f'\nUser input for the filename arguement is:\n{filepath}\n\nPath exists? : [{filepath.exists()}]')

	if not file_exists:
		raise FileNotFoundError("The provided file does not exist.")

	playtime_data = calc.read_input(filepath, args.no_headers, input_is_tsv)

	# print(playtime_data)
	# print("\n")

	playtime = calc.sum_playtime(playtime_data)
	print(f'{playtime} hours')
