import csv
import ipdb

import validator as v

class Batch:
    def __init__(self, capacity, flush_function):
        self.data = []
        self.flush_function = flush_function 
        self.capacity = capacity
    
    def add(self, item):
        self.data.append(item)
        print(f'Number of items: {len(self.data)}')
        if len(self.data) == self.capacity:
            print(f'flushing {self.data}')
            self.flush()
            self.reset()
    
    def reset(self):
        self.data = []

    def flush(self):
        self.flush_function(self.data)

class CSVUnifier:

    valid = {'Provider Name': v.provider_name,
             'Zipcode': v.zipcode,
             'Cost Per Ad Click': v.cost_per_ad_click,
             'Redirect Link': v.redirect_link,
             'Phone Number': v.phone_number,
             'Address': v.address,
             'CampaignID': v.campaign_id}

    def __init__(self, batch_size, output_file):
        writer = csv.writer(output_file, delimiter=',')
        self.batch = Batch(batch_size, writer.writerows) 
        self.header = None

    def process(self, rows):
        for r in rows:
            if self.header is None:
                self.header = r 
                self.filtered_header = [h for h in r if h in self.valid]
                if len(self.filtered_header) != len(valid.keys):
                    print(f'All columns in schema must be present')
                    return
                self.batch.add(self.filtered_header)
            else:
                filtered_row = self.filter(r)
                if self.valid_row(filtered_row):
                    self.batch.add(filtered_row)
                else:
                    print(f'Invalid row: {r}')
    
    def valid_row(self, row):
        if len(row) != len(self.filtered_header):
            return False

        for i, column_name in enumerate(self.filtered_header):
            if not self.valid[column_name](row[i]):
                return False
        return True

    def filter(self, row):
        return [v for i, v in enumerate(row) if self.header[i] in self.valid]

    def reset_header(self):
        self.header = None

    def clean_up(self):
        print('Cleaning up')
        self.batch.flush()

if __name__ == "__main__":
    input_filenames = ['auto.csv', 'home.csv']
    output_filename = 'output.csv'
    batch_size = 3

    with open(output_filename, 'w', newline='\n') as output_file:
        csv_unifier = CSVUnifier(batch_size=batch_size, output_file=output_file)

        for filename in input_filenames: 
            csv_unifier.reset_header()
            with open(filename, 'r', newline='\n') as csv_file:
                rows = csv.reader(csv_file)
                csv_unifier.process(rows)
                csv_unifier.clean_up()    