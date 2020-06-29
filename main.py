"""
Unifies auto.csv and home.csv

Invalid rows from these csvs:
    AUTO:
        NoZip: null campaignid, zip
    HOME:
        WeProtect: null address
"""

import csv

from csv_unifier import unify_csvs
import validator as v


input_filenames = ['auto.csv', 'home.csv']
output_filename = 'output.csv'
batch_size = 3

schema = [
    'Provider Name',
    'CampaignID',
    'Cost Per Ad Click',
    'Redirect Link',
    'Phone Number',
    'Address',
    'Zipcode',
    ]

validator_map = {
    'Provider Name': v.provider_name,
    'CampaignID': v.campaign_id,
    'Cost Per Ad Click': v.cost_per_ad_click,
    'Redirect Link': v.redirect_link,
    'Phone Number': v.phone_number,
    'Address': v.address,
    'Zipcode': v.zipcode,
}

unify_csvs(input_filenames=input_filenames,
           output_filename=output_filename,
           batch_size=batch_size,
           schema=schema,
           validator_map=validator_map)
