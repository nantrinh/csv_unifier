import csv

import validator as v
# TODO: fix mistakes (see bottom of file)
# TODO: take in a list of files as args


class Batch:
    def __init__(self, capacity, flush_function):
        self.data = []
        self.flush_function = flush_function
        self.capacity = capacity

    def add(self, item):
        self.data.append(item)
        # print(f'Number of items: {len(self.data)}')
        if len(self.data) == self.capacity:
            # print(f'flushing {self.data}')
            self.flush()
            self.reset()

    def reset(self):
        self.data = []

    def flush(self):
        self.flush_function(self.data)
        self.data = []


class CSVUnifier:
    """
    All columns in the schema must be present in the input data.
    Rows are validated before written to an output file in batches.
    Rows are always written in the order specified in the schema.
    """

    SCHEMA = [
        'Provider Name',
        'CampaignID',
        'Cost Per Ad Click',
        'Redirect Link',
        'Phone Number',
        'Address',
        'Zipcode',
        ]

    VALID = {
        'Provider Name': v.provider_name,
        'CampaignID': v.campaign_id,
        'Cost Per Ad Click': v.cost_per_ad_click,
        'Redirect Link': v.redirect_link,
        'Phone Number': v.phone_number,
        'Address': v.address,
        'Zipcode': v.zipcode,
    }

    def __init__(self, batch_size, output_file):
        write_function = csv.writer(output_file,
                                    delimiter=',',
                                    lineterminator='\n').writerows
        self.batch = Batch(batch_size, write_function)
        self.header = None
        self.header_map = {}
        self.header_written = False

    def process(self, rows):
        for r in rows:
            if self.header is None:
                self.make_header_map(r)
                if len(self.SCHEMA) != len(self.header_map):
                    print(f'All columns in schema must be present')
                    return
                self.header = r
                if not self.header_written:
                    self.batch.add(self.SCHEMA)
                    self.header_written = True
            else:
                clean_row = self.clean(r)
                if self.valid_row(clean_row):
                    self.batch.add(clean_row)
                else:
                    print(f'Invalid row: {clean_row}')

    def valid_row(self, row):
        for i, v in enumerate(row):
            if not self.VALID[self.SCHEMA[i]](v):
                print(f'{v} is an invalid value for {self.SCHEMA[i]}')
                return False
        return True

    def clean(self, row):
        """
        Cleans, reorders, and filters values in the row
        """
        res = ['' for x in range(len(self.SCHEMA))]
        for i, v in enumerate(row):
            if i in self.header_map:
                res[self.header_map[i]] = v.strip('"')
        return res

    def make_header_map(self, header):
        """
        Maps index of a column name in header to index in schema
        """
        for i, name in enumerate(header):
            if name in self.SCHEMA:
                self.header_map[i] = self.SCHEMA.index(name)

    def reset_header(self):
        self.header = None
        self.header_map = {}

    def clean_up(self):
        # print('Cleaning up')
        self.batch.flush()


if __name__ == "__main__":
    input_filenames = ['auto.csv', 'home.csv']
    output_filename = 'output.csv'
    batch_size = 3

    with open(output_filename, 'w') as output_file:
        cu = CSVUnifier(batch_size=batch_size, output_file=output_file)
        for filename in input_filenames:
            cu.reset_header()
            with open(filename, 'r', newline='\n') as csv_file:
                rows = csv.reader(csv_file)
                cu.process(rows)
                cu.clean_up()

    """
    Mistakes:
      AUTO: Tiger King Rd should be valid address
      HOME: 6th street should be valid address

    Invalid
      AUTO
        NoZip: null campaignid, zip
      HOME
        WeProtect: null address
    """