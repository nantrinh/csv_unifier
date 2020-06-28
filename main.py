import csv
import pandas as pd
import ipdb

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
    def __init__(self, batch_size, output_file):
        writer = csv.writer(output_file, delimiter=',')
        self.batch = Batch(batch_size, writer.writerows) 

    def process(self, rows):
        for r in rows:
            if not self.valid_row(rows):
                print(f'Invalid row: {r}')
            else:
                self.batch.add(r)
    
    def valid_row(self, row):
        return True

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
            with open(filename, 'r', newline='\n') as csv_file:
                rows = csv.reader(csv_file)
                csv_unifier.process(rows)
        csv_unifier.clean_up()    