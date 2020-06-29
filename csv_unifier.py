import csv

from batch import Batch


def unify_csvs(input_filenames, output_filename, batch_size, schema, validator_map):
    """
    Uses CSVUnifier to aggregate data from multiple CSVs according
    to a specified schema.
    """
    with open(output_filename, 'w') as output_file:
        cu = CSVUnifier(
                 batch_size=batch_size,
                 output_file=output_file,
                 schema=schema,
                 validator_map=validator_map)
        for filename in input_filenames:
            cu.reset_header()
            with open(filename, 'r', newline='\n') as csv_file:
                rows = csv.reader(csv_file)
                cu.process(rows)
                cu.clean_up()


class CSVUnifier:
    """
    Aggregates data from multiple CSVs, cleans and validates the values,
    and writes the rows to a specified output file.

    All columns in the schema must be present in the input data.
    Rows are validated before written to an output file in batches.
    Rows are always written in the order specified in the schema.
    """

    def __init__(self, batch_size, output_file, schema, validator_map):
        write_function = csv.writer(output_file,
                                    delimiter=',',
                                    lineterminator='\n').writerows
        self.batch = Batch(batch_size, write_function)
        self.header = None
        self.header_map = {}
        self.header_written = False

        self.schema = schema
        self.validator_map = validator_map

    def process(self, rows):
        for r in rows:
            if self.header is None:
                self.make_header_map(r)
                if len(self.schema) != len(self.header_map):
                    print(f'All columns in schema must be present')
                    return
                self.header = r
                if not self.header_written:
                    self.batch.add(self.schema)
                    self.header_written = True
            else:
                clean_row = self.clean(r)
                if self.valid_row(clean_row):
                    self.batch.add(clean_row)
                else:
                    print(f'Invalid row: {r}')

    def valid_row(self, row):
        for i, v in enumerate(row):
            if not self.validator_map[self.schema[i]](v):
                return False
        return True

    def clean(self, row):
        """
        Cleans, reorders, and filters values in the row
        """
        res = ['' for x in range(len(self.schema))]
        for i, v in enumerate(row):
            if i in self.header_map:
                res[self.header_map[i]] = v.strip('"')
        return res

    def make_header_map(self, header):
        """
        Maps index of a column name in header to index in schema
        """
        for i, name in enumerate(header):
            if name in self.schema:
                self.header_map[i] = self.schema.index(name)

    def reset_header(self):
        self.header = None
        self.header_map = {}

    def clean_up(self):
        self.batch.flush()
