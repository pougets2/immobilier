outil = ['London', 'West-Midlands', 'Greater-Manchester', 'West-Yorkshire', 'Kent', 'Essex', 'Merseyside',
         'South-Yorkshire',
         'Hampshire', 'Lancashire', 'Surrey', 'Hertfordshire', 'Tyne-and-Wear', 'Norfolk', 'Staffordshire',
         'West-Sussex',
         'Nottinghamshire', 'Derbyshire', 'Devon', 'Suffolk', 'Lincolnshire', 'Northamptonshire', 'Oxfordshire',
         'Leicestershire',
         'Cambridgeshire', 'North-Yorkshire', 'Gloucestershire', 'Worcestershire', 'Warwickshire', 'Cornwall',
         'Somerset',
         'East-Sussex', 'County-Durham', 'Buckinghamshire', 'Cumbria', 'Wiltshire', 'Bristol', 'Dorset',
         'East-Riding-of-Yorkshire', 'Leicester', 'Cheshire-West-and-Chester', 'Northumberland', 'Shropshire',
         'Nottingham',
         'Brighton-&-Hove', 'Medway', 'South-Gloucestershire', 'Plymouth', 'Hull', 'Central-Bedfordshire',
         'Milton-Keynes',
         'Derby', 'Stoke-on-Trent', 'Southampton', 'Swindon', 'Portsmouth', 'Luton', 'North-Somerset', 'Warrington',
         'York',
         'Stockton-on-Tees', 'Peterborough', 'Herefordshire', 'Bournemouth', 'Bath-and-North-East-Somerset',
         'Southend-on-Sea',
         'North-Lincolnshire', 'Telford-and-Wrekin', 'North-East-Lincolnshire', 'Thurrock', 'Bedford', 'Reading',
         'Wokingham',
         'West-Berkshire', 'Poole', 'Blackburn-with-Darwen', 'Windsor-and-Maidenhead', 'Blackpool', 'Slough',
         'Middlesbrough',
         'Isle-of-Wight', 'Redcar-and-Cleveland', 'Torbay', 'Halton', 'Bracknell-Forest', 'Darlington',
         'Hartlepool', 'Rutland']

urls = []
for element in outil:
    url = "https://www.zoopla.co.uk/for-sale/property/" + element + "/?identifier=" + element + "&q=" + element + "&search_source=refine&radius=0&page_size=100&pn=0"
    urls.append(url)
print(urls)