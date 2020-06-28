import re

def provider_name(s):
  """
  one or more alphanumeric
  zero or more alphanumeric, apostrophes, spaces, or underscores
  """
  return re.match("^[a-z\d]+[a-z\d' _]*$", s, re.IGNORECASE) 

def zipcode(s):
    return len(s) == 5 and s.isnumeric()

def cost_per_ad_click(s):
    """
    one or more digits
    optional decimal
    up to two digits 
    """
    return re.match('^[\d]+\.?[\d]{0,2}$', s)

def redirect_link(s):
    """
    one or more alphanumeric characters
    decimal
    one or more alphanumeric characters
    optional slash
    zero or more alphanumeric characters
    """
    return re.match('^[a-z\d]+\.[a-z\d]+\/?[a-z\d]*$', s, re.IGNORECASE)

def phone_number(s):
    return len(s) == 0 or s.isnumeric() and len(s) == 7

def address(s):
    return re.match('^[a-z]+ [a-z]+$', s, re.IGNORECASE)

def campaign_id(s):
    return re.match('^[a-z]+[\d]*$', s, re.IGNORECASE)