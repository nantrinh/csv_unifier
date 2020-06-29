# The Zebra Data Engineering Interview Assignment

## Instructions

See [`instructions.pdf`](https://github.com/nantrinh/csv_unifier/blob/master/Instructions.pdf).

The short version is:

Given a list of CSV files and a schema, aggregate the data from the multiple files into a single CSV that matches the schema.

## How to run

### Requirements

- Python 3.8.2

### Steps

- Run `python main.py`
- See `output.csv` for results.

## Description of files

- [`main.py`](https://github.com/nantrinh/csv_unifier/blob/master/main.py) defines

  - the list of CSVs to be aggregated
  - the name of the output file to which results will be written
  - the batch size (lines are processed one at a time; the batch size specifies how many processed lines are kept in memory before flushing to disk)
  - the schema (the order of the columns listed is the order that the columns will appear in the output file)
  - a dictionary mapping each column name to a function that accepts a value and returns `True` if the value is a valid instance of that column, and `False` otherwise

- [`csv_unifier.py`](https://github.com/nantrinh/csv_unifier/blob/master/csv_unifier.py) defines
  - `unify_csvs`: a function called by `main.py` that opens up files and calls the necessary methods of the `CSVUnifier` class to process the data
  - `CSVUnifier`: a class that handles much of the operations required to aggregate, validate, and write the cleaned output to a file
- [`batch.py`](https://github.com/nantrinh/csv_unifier/blob/master/batch.py) defines a `Batch` class used by the `CSVUnifier` class to handle writing data to a file in batches.
- [`validator.py`](https://github.com/nantrinh/csv_unifier/blob/master/validator.py) defines a function for each column in the schema. Each function returns `True` if the value passed in conforms to a specified set of rules for that column and `False` otherwise.
- [`test_validator.py`](https://github.com/nantrinh/csv_unifier/blob/master/test_validator.py) contains tests for the functions defined in `validator.py`.
- [`test_csv_unifier.py`](https://github.com/nantrinh/csv_unifier/blob/master/test_validator.py) contains tests for the `CSVUnifier` class.
