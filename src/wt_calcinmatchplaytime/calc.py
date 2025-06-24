import pathlib
import csv
import re
from datetime import timedelta


# from https://stackoverflow.com/a/79589031/11750206
def parse_timedelta(value: str) -> timedelta:
	TIMEDELTA_PATTERN = re.compile(
		r"""
				^
				\s*
				((?P<weeks>\d+(\.\d+)?)(w|\s*wks?|\s*weeks?))?
				\s*
				((?P<days>\d+(\.\d+)?)(d|\s*days?))?
				\s*
				((?P<hours>\d+(\.\d+)?)(h|\s*hrs?|\s*hours?))?
				\s*
				((?P<minutes>\d+(\.\d+)?)(m|\s*mins?|\s*minutes?))?
				\s*
				((?P<seconds>\d+(\.\d+)?)(s|\s*secs?|\s*seconds?))?
				\s*
				((?P<milliseconds>\d+(\.\d+)?)(ms|\s*millis?|\s*milliseconds?))?
				\s*
				((?P<microseconds>\d+(\.\d+)?)(us|\s*micros?|\s*microseconds?))?
				\s*
				$
		""",
		flags=re.IGNORECASE | re.VERBOSE,
	)

	match = TIMEDELTA_PATTERN.match(value)
	if not match:
		raise ValueError(f"Invalid timedelta: {value!r}")

	params = {
		u: float(v) for u, v in match.groupdict().items() if v
	}
	return timedelta(**params)


def read_input(filepath: pathlib.Path, has_header: bool = True) -> list:
	fileext = filepath.suffix
	file_delimiter = '\t'
	if fileext == '.csv':
		file_delimiter = ','

	fields = []
	rows = []
	with open(filepath, 'r') as input:
		reader = csv.reader(input, delimiter=file_delimiter, quotechar='"')
		if has_header:
			fields = next(reader)
		for row in reader:
			rows.append(row)
	return rows


def secs2hrs(seconds: float) -> float:
	secsINhrs = 60 * 60
	hours = seconds / secsINhrs
	return hours


def sum_playtime(tsv: list) -> float:
	playtimesumdelta = timedelta(seconds=0)
	for row in tsv:
		playtimedelta = parse_timedelta(row[1])
		playtimesumdelta += playtimedelta
	playtimesum = round(secs2hrs(playtimesumdelta.total_seconds()), 3)
	return playtimesum
