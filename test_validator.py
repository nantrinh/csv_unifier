import unittest

import validator as v

class TestValidator(unittest.TestCase):
    def test_provider_name(self):
        true_cases = ["Home R' Us",
                      'HomeGuard',
                      "WeProtect",
                      "HelloWorld123",
                      "hello_world",
                      "123_456",
                      "123 456_abcdefg"
                      ]

        false_cases = ["abc(#*$)defg",
                       "",
                       " "
                       ]

        for c in true_cases:
            self.assertTrue(v.provider_name(c), c)

        for c in false_cases:
            self.assertFalse(v.provider_name(c), c)

    def test_zipcode(self):
        true_cases = ["12345",
                      '00000',
                      ]

        false_cases = ["",
                       "abcde",
                       "1234",
                       "123456"
                       ]

        for c in true_cases:
            self.assertTrue(v.zipcode(c), c)

        for c in false_cases:
            self.assertFalse(v.zipcode(c), c)

    def test_cost_per_ad_click(self):
        true_cases = ["12.34",
                      '00.00',
                      '0',
                      '1',
                      '1234039814',
                      '1234.3',
                      '1234.',
                      ]

        false_cases = ["",
                       "12.345",
                       "12.3.4",
                       "abc",
                       ]

        for c in true_cases:
            self.assertTrue(v.cost_per_ad_click(c), c)

        for c in false_cases:
            self.assertFalse(v.cost_per_ad_click(c), c)

    def test_redirect_link(self):
        true_cases = ["autorus.com/auto1",
                      '0.0',
                      'a.0/123',
                      'github.io/helloworld'
                      ]

        false_cases = ["",
                       "12",
                       "abc",
                       "abc/com"
                       ]

        for c in true_cases:
            self.assertTrue(v.redirect_link(c), c)

        for c in false_cases:
            self.assertFalse(v.redirect_link(c), c)

    def test_account_id(self):
        true_cases = ['1234342',
                      '1',
                      '2'
                      ]

        false_cases = ["",
                       "abc",
                       "123.0"
                       ]

        for c in true_cases:
            self.assertTrue(v.account_id(c), c)

        for c in false_cases:
            self.assertFalse(v.account_id(c), c)

    def test_phone_number(self):
        true_cases = ['1234567',
                      '0000000'
                      ]

        false_cases = ["",
                       "abcdefg",
                       "123-4567"
                       ]

        for c in true_cases:
            self.assertTrue(v.phone_number(c), c)

        for c in false_cases:
            self.assertFalse(v.phone_number(c), c)

    def test_address(self):
        true_cases = ['Burton Street',
                      'burton street',
                      'hello world'
                      ]

        false_cases = ["",
                       "Burton",
                       "123 4567"
                       ]

        for c in true_cases:
            self.assertTrue(v.address(c), c)

        for c in false_cases:
            self.assertFalse(v.address(c), c)

    def test_campaign_id(self):
        true_cases = ['AUTO',
                      'AUTO1',
                      'WORD8923',
                      'A1',
                      'B1'
                      ]

        false_cases = ["",
                       "123",
                       "AUTO 1",
                       "AUTO_1"
                       ]

        for c in true_cases:
            self.assertTrue(v.campaign_id(c), c)

        for c in false_cases:
            self.assertFalse(v.campaign_id(c), c)

if __name__ == "__main__":
    unittest.main()
