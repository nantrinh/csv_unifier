"""
Test CSV Unifier

Test outputs and stdout are expected to fit in memory.
"""

import sys
import csv
from io import StringIO
import unittest

from main import CSVUnifier


class TestCSVUnifier(unittest.TestCase):
    def setUp(self):
        self.output_file = StringIO()
        self.BATCH_SIZE = 2
        self.COLUMN_MISSING_ERROR = 'All columns in schema must be present'
        self.INVALID_ROW_ERROR = 'Invalid row: '

        self.orig_stdout = sys.stdout

    def written(self, obj):
        """
        Helper method: parses the file and returns a list of rows
        """
        return [row.split(',') for row in obj.getvalue().strip().split('\n')]

    def stdout_list(self, obj):
        return [line for line in obj.getvalue().strip().split('\n')
                if len(line) > 0]

    def test_all_columns_are_present(self):
        """
        If one or more headers from the schema are missing,
        an error message is printed, and nothing is written to the output.
        """

        header = [
            'Provider Name',
            'CampaignID',
            'Cost Per Ad Click',
            'Redirect Link',
            'Phone Number',
            'Address',
            'Zipcode']
        data = [
            "Auto R' Us",
            'AUTO1',
            '15.00',
            'autorus.com/auto1',
            '8675309',
            'Burton Street']

        for i in range(len(header)):
            sys.stdout = new_stdout = StringIO()
            rows = [header[:i] + header[i + 1:], data[:i] + data[i + 1:]]
            cu = CSVUnifier(
                batch_size=self.BATCH_SIZE,
                output_file=self.output_file)
            cu.reset_header()
            cu.process(rows)
            cu.clean_up()

            self.assertEqual(0, len(self.output_file.getvalue()))

            stdout_list = self.stdout_list(new_stdout)
            self.assertEqual(1, len(stdout_list))
            self.assertEqual(self.COLUMN_MISSING_ERROR, stdout_list[0])

    def test_all_data_is_present(self):
        """
        For a given row, if values for all fields are present and valid,
        no messages are printed, and the row is written to the output.
        """
        rows = [
            ['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode'],
            ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
            ["Auto R' Us", 'AUTO2', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
            ["Auto R' Us", 'AUTO3', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
            ["Auto R' Us", 'AUTO4', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
            ["Auto R' Us", 'AUTO5', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
        ]

        sys.stdout = new_stdout = StringIO()
        cu = CSVUnifier(
            batch_size=self.BATCH_SIZE,
            output_file=self.output_file)
        cu.reset_header()
        cu.process(rows)
        cu.clean_up()

        written = self.written(self.output_file)
        self.assertEqual(len(rows), len(written))
        for i, row in enumerate(written):
            self.assertEqual(rows[i], row)

        stdout_list = self.stdout_list(new_stdout)
        self.assertEqual(0, len(stdout_list))

    def test_missing_data(self):
        """
        When the length of a row does not match the length of the header,
        an error message is printed, and the row does not get written to the output.
        """

        # the first two rows (including the header) are valid,
        # the rest each have a value missing
        rows = [
            ['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode'],
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
        cu = CSVUnifier(
            batch_size=self.BATCH_SIZE,
            output_file=self.output_file)
        cu.reset_header()
        cu.process(rows)
        cu.clean_up()

        written = self.written(self.output_file)
        self.assertEqual(2, len(written))
        for i, row in enumerate(written):
            self.assertEqual(rows[i], row)

        stdout_list = self.stdout_list(new_stdout)
        self.assertEqual(len(rows) - 2, len(stdout_list))
        for i, line in enumerate(stdout_list):
            self.assertEqual(self.INVALID_ROW_ERROR + str(rows[i + 2]), line)

    def test_nonconforming_data(self):
        """
        When a row contains data that does not conform to the schema,
        an error is printed and the row does not get written to the output.
        """

        # the first two rows (including the header) are valid,
        # the rest each contain a non-conforming value
        rows = [
            ['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode'],
            ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
            ["   ", 'AUTO2', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
            ["Auto R' Us", '123', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
            ["Auto R' Us", 'AUTO4', '15.392040', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
            ["Auto R' Us", 'AUTO5', '15.00', 'autorus', '8675309', 'Burton Street', '78702'],
            ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '123456', 'Burton Street', '78702'],
            ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton', '78702'],
            ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '7870']
        ]

        sys.stdout = new_stdout = StringIO()
        cu = CSVUnifier(
            batch_size=self.BATCH_SIZE,
            output_file=self.output_file)
        cu.reset_header()
        cu.process(rows)
        cu.clean_up()

        written = self.written(self.output_file)
        self.assertEqual(2, len(written))
        for i, row in enumerate(written):
            self.assertEqual(rows[i], row)

        stdout_list = self.stdout_list(new_stdout)
        self.assertEqual(len(rows) - 2, len(stdout_list))
        for i, line in enumerate(stdout_list):
            self.assertEqual(self.INVALID_ROW_ERROR + str(rows[i + 2]), line)

    def test_columns_not_in_the_schema(self):
        """
        Columns not listed in the schema are ignored.
        No error messages are printed.
        """
        rows = [
            ['Provider Name', 'CampaignID', 'AccountId', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode', 'Favorite Animal'],
            ["Auto R' Us", 'AUTO1', '4', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702', 'Cat']
        ]

        rows_expected_output = [
            ['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode'],
            ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702']
        ]

        sys.stdout = new_stdout = StringIO()
        cu = CSVUnifier(
            batch_size=self.BATCH_SIZE,
            output_file=self.output_file)
        cu.reset_header()
        cu.process(rows)
        cu.clean_up()

        written = self.written(self.output_file)
        self.assertEqual(len(rows_expected_output), len(written))
        for i, row in enumerate(written):
            self.assertEqual(rows_expected_output[i], row)

        stdout_list = self.stdout_list(new_stdout)
        self.assertEqual(0, len(stdout_list))

    def test_columns_are_written_in_the_schema_order(self):
        rows = [
            ['Provider Name', 'CampaignID', 'Cost Per Ad Click', 'Redirect Link', 'Phone Number', 'Address', 'Zipcode'],
            ["Auto R' Us", 'AUTO1', '15.00', 'autorus.com/auto1', '8675309', 'Burton Street', '78702'],
        ]

        rows = [list(reversed(row)) for row in rows] 

        sys.stdout = new_stdout = StringIO()
        cu = CSVUnifier(
            batch_size=self.BATCH_SIZE,
            output_file=self.output_file)
        cu.reset_header()
        cu.process(rows)
        cu.clean_up()

        written = self.written(self.output_file)
        self.assertEqual(len(rows), len(written))
        for i, row in enumerate(written):
            self.assertEqual(list(reversed(rows[i])), row)

        stdout_list = self.stdout_list(new_stdout)
        self.assertEqual(0, len(stdout_list))




if __name__ == "__main__":
    unittest.main()
