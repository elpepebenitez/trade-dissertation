import os
import requests
from dotenv import load_dotenv
import comtradeapicall

# Load environment variables from .env file
load_dotenv()
# Access the private key
subscription_key = os.getenv('COMTRADE_API_KEY')
# Use the API key in your code
# print(api_key)

# https://comtradeapi.un.org/data/v1/get/{typeCode}/
# {freqCode}/{clCode}[?reporterCode][&period][&partnerCode][&partner2Code]
# [&cmdCode][&flowCode][&customsCode][&motCode][&aggregateBy][&breakdownMode][&includeDesc]

# typeCode='C' for commodities
# freqCode='A' for annual
# clCode='HS for HS codes as trade classification system
# period='2000' for a year. Multi value input should be in the form of csv (Codes separated by comma (,))
# reporterCode='36' is for M49 code of the countries separated by comma (,)). https://comtradeapi.un.org/files/v1/app/reference/Reporters.json 591 Panama
# flowCode='X' for exports. M for imports.
# cmdCode=None https://comtradeapi.un.org/files/v1/app/reference/H6.json

mydf = comtradeapicall.getFinalData(subscription_key, typeCode='C', freqCode='A', clCode='HS', period='2000',
                                    reporterCode='591', cmdCode=None, flowCode='X', partnerCode=None,
                                    partner2Code=None,
                                    customsCode=None, motCode=None, maxRecords=250000, format_output='JSON',
                                    aggregateBy=None, breakdownMode='classic', countOnly=None, includeDesc=True)

print(mydf.head(5))
print(mydf.count())