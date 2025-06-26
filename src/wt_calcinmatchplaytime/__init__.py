import argparse
import pathlib
from binaryornot.check import is_binary
from wt_calcinmatchplaytime import calc


def forfile(args: argparse.Namespace, inpistsv: bool = True) -> None:
	path = pathlib.Path(args.filename).resolve()
	path_exists = path.exists()
	# print(f'\nUser input for the filename arguement is:\n{filepath}\n\nPath exists? : [{filepath.exists()}]')
	if not path_exists:
		raise FileNotFoundError("The provided path does not exist.")

	path_is_file = path.is_file()
	if not path_is_file:
		raise IsADirectoryError("The provided path does not point to a file.")

	playtime = calc.calc_playtime(path, args.no_headers, inpistsv)
	print(f'{playtime} hours')


def fordir(args: argparse.Namespace, inpistsv: bool = True) -> None:

	def upd_playtime_dict(inpdict: dict, inppath: pathlib.Path) -> None:
		filename = inppath.name.removesuffix("".join(inppath.suffixes))
		playtime = calc.calc_playtime(inppath, args.no_headers, inpistsv)
		inpdict.update({
			filename: str(playtime)
		})

	path = pathlib.Path(args.directory).resolve()
	path_exists = path.exists()
	if not path_exists:
		raise FileNotFoundError("The provided path does not exist.")

	path_is_dir = path.is_dir()
	if not path_is_dir:
		raise NotADirectoryError("The provided path does not point to a directory.")

	# print(path)

	file_playtimes = {}

	if args.recurse:
		for child in path.rglob('*'):
			if child.is_file():
				if not is_binary(str(child.resolve())):
					upd_playtime_dict(file_playtimes, child)
	else:
		for child in path.iterdir():
			if child.is_file():
				if not is_binary(str(child.resolve())):
					upd_playtime_dict(file_playtimes, child)

	# print(file_playtimes)
	file_playtimes_sorted = dict(sorted(file_playtimes.items()))

	max_key_len = max(map(len, file_playtimes_sorted.keys()))
	max_val_len = max(map(len, file_playtimes_sorted.values()))
	# print(f'Max Key Len : {max_key_len}\nMax Val Len : {max_val_len}\n')

	for k, v in file_playtimes_sorted.items():
		print(f'{k:<{max_key_len}} : {v:>{max_val_len}} hours')


def main() -> None:
	parser = argparse.ArgumentParser(description="A Python CLI application that takes a TSV/CSV file (defaults to TSV) containing your in-game match time and outputs the total playtime in hours.")

	input_types = parser.add_mutually_exclusive_group()
	input_types.add_argument("-i", "--filename", help="TSV/CSV file (defaults to TSV) that contains the in-match playtime. col 1 of the file is vehicle type and col 2 is time played")
	input_types.add_argument("-d", "--directory", help="Directory that contains the files to be passed as input to the app. Will not look in subdirectories")

	parser.add_argument("-r", "--recurse", help="Recurse subdirectories when the path passed to the CLI app points to a directory", action="store_true")
	parser.add_argument("-nh", "--no-headers", help="Indicate that the input file does not have headers", action="store_true")

	force_delim = parser.add_mutually_exclusive_group()
	force_delim.add_argument("-c", "--csv", action="store_true", help="Force the CLI application to use CSV delimiters")
	force_delim.add_argument("-t", "--tsv", action="store_true", help="Force the CLI application to use TSV delimiters")

	args = parser.parse_args()
	# print(args)
	# print(type(args))
	# print('')

	if args.filename is None and args.directory is None:
		raise Exception("An argument for either --filename or --directory must be passed.")

	input_is_tsv = True
	if args.csv:
		input_is_tsv = False
	if args.tsv:
		input_is_tsv = True

	if args.filename is not None:
		forfile(args=args, inpistsv=input_is_tsv)
	if args.directory is not None:
		fordir(args=args, inpistsv=input_is_tsv)
