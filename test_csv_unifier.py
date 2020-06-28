"""
Test CSV Unifier

Note that test outputs and stdout are expected to fit in memory (StringIO is used).
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

    def test_all_columns_are_present(self):
        """
        Required headers must be present

        For each item in header, passes the rest of the header excluding that item,
        and the data excluding that column.

        An error message should be printed.
        Nothing should be written to the output.
        """

        header = ['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode']
        data = ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street']

        for i in range(len(header)):
            sys.stdout = new_stdout = StringIO()
            rows = [header[:i] + header[i + 1:], data[:i] + data[i + 1:]]
            cu = CSVUnifier(batch_size=self.batch_size,
                            output_file=self.output_file)
            cu.reset_header()
            cu.process(rows)
            cu.clean_up()

            self.assertEqual('All columns in schema must be present', new_stdout.getvalue().strip())
            self.assertEqual('', self.output_file.getvalue())

    @unittest.skip("")
    def test_all_data_is_present(self):
        """
        When values for all fields are present and valid, they are written to the output.
        """
        rows = [['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode'],
         ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO2', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO3', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO4', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ["Auto R' Us", 'AUTO5', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
         ]

        with open(self.output_filename, 'w', newline='\n') as output_file:
            cu = CSVUnifier(batch_size=self.batch_size, output_file=output_file) 
            cu.reset_header()
            cu.process(rows)
            cu.clean_up()

        with open(self.output_filename) as output_file:
            for i, row in enumerate(csv.reader(output_file)):
                self.assertEqual(rows[i], row)

    @unittest.skip("")
    def test_missing_data(self):
        """
        When the length of a row does not match the length of the header,
        the row does not get written to the output.

        TODO: Use contextmanager to temporarily replace sys.stdout to verify
        error message is being printed
        https://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python
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

        with open(self.output_filename, 'w', newline='\n') as output_file:
            cu = CSVUnifier(batch_size=self.batch_size, output_file=output_file) 
            cu.reset_header()
            cu.process(rows)
            cu.clean_up()

        with open(self.output_filename) as output_file:
            ctr = 0
            for i, row in enumerate(csv.reader(output_file)):
                ctr += 1
                if i <= 1:
                    self.assertEqual(rows[i], row)
            self.assertEqual(2, ctr)

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