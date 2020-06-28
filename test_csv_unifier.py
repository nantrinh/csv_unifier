"""
Test CSV Unifier

Note that test outputs and stdout are expected to fit in memory.
"""

import sys
import csv
from io import StringIO
import unittest

from main import CSVUnifier
import ipdb

# TODO: use StringIO instead of actual IO


class TestCSVUnifier(unittest.TestCase):
    def setUp(self):
        self.output_file = StringIO() 
        self.batch_size = 2 

        self.orig_stdout = sys.stdout 

    def written(self):
        return [row.split(',') for row in self.output_file.getvalue().strip().split('\n')]


    def test_all_columns_are_present(self):
        """
        If one or more headers from the schema are missing,
        an error message is printed, and nothing is written to the output. 
        """

        header = ['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode']
        data = ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street']

        for i in range(len(header)):
            sys.stdout = new_stdout = StringIO()
            rows = [header[:i] + header[i + 1:], data[:i] + data[i + 1:]]
            cu = CSVUnifier(batch_size=self.batch_size, output_file=self.output_file)
            cu.reset_header()
            cu.process(rows)
            cu.clean_up()

            self.assertEqual('All columns in schema must be present', new_stdout.getvalue().strip())
            self.assertEqual(0, len(self.output_file.getvalue()))

    def test_all_data_is_present(self):
        """
        For a given row, if values for all fields are present and valid,
        the row is written to the output.
        """
        rows = [['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode'],
         ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO2', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO3', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO4', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO5', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ]

        sys.stdout = new_stdout = StringIO()
        cu = CSVUnifier(batch_size=self.batch_size, output_file=self.output_file) 
        cu.reset_header()
        cu.process(rows)
        cu.clean_up()

        written = self.written() 
        self.assertEqual(len(rows), len(written))
        for i, row in enumerate(written):
            self.assertEqual(rows[i], row)

    def test_missing_data(self):
        """
        When the length of a row does not match the length of the header,
        the row does not get written to the output.
        """

        # the first row is valid, the rest each have a value missing
        rows = [['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode'],
         ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ['AUTO2', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO4', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO5', '15.00', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', '78702'],
         ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street']
         ]

        sys.stdout = new_stdout = StringIO()
        cu = CSVUnifier(batch_size=self.batch_size, output_file=self.output_file) 
        cu.reset_header()
        cu.process(rows)
        cu.clean_up()

        written = self.written() 
        self.assertEqual(2, len(written))
        for i, row in enumerate(written):
            self.assertEqual(rows[i], row)


    @unittest.skip('')
    def test_nonconforming_data(self):
        """
        When a row contains data that does not conform to the schema,
        an error is printed and the row does not get written to the output.
        """
        pass

    @unittest.skip("")
    def test_columns_not_in_the_schema(self):
        """
        Columns not listed in the schema are ignored.
        """
        rows_input = [['Provider Name', 'CampaignID', 'AccountId', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode', 'Favorite Animal'],
         ["Auto R' Us", 'AUTO1', '4', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702', 'Cat']]

        rows_expected_output = [['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode'],
         ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702']]

        with open(self.output_filename, 'w', newline='\n') as output_file:
            cu = CSVUnifier(batch_size=self.batch_size, output_file=output_file) 
            cu.reset_header()
            cu.process(rows_input)
            cu.clean_up()

        with open(self.output_filename) as output_file:
            for i, row in enumerate(csv.reader(output_file)):
                self.assertEqual(rows_expected_output[i], row)

if __name__ == "__main__":
    unittest.main()