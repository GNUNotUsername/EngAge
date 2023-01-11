from datetime import datetime

INTERESTS = [
    ('AC', 'Acting'),		('AE', 'Aerobics'),		('AR', 'Archery'),
    ('BA', 'Badminton'),	('BK', 'Baking'),		('BQ', 'Barbecueing'),	('BS', 'Baseball'),
    ('BB', 'Basketball'),	('BE', 'Beach'),		('BI', 'Bingo'),		('BG', 'Board Games'),
    ('BO', 'Book Clubs'),	('BW', 'Bowling'),		('CP', 'Camping'),		('CN', 'Canoeing'),
    ('CG', 'Card Games'),	('CA', 'Cars'),			('CH', 'Chess'),		('CF', 'Coffee'),
    ('NM', 'Coin Collecting / Numismatology'),		('CO', 'Comics'),		('CK', 'Cooking'),
    ('CR', 'Cricket'),		('CY', 'Cycling'),		('DA', 'Dancing'),		('DA', 'Darts'),
    ('DO', 'Dogs'),			('DM', 'Dominoes'),		('FI', 'Fishing'),		('FO', 'Football'),
    ('GA', 'Gardening'),	('GM', 'Gaming'),		('GO', 'Golf'),			('GY', 'Gym'),
    ('HI', 'Hiking'),		('LA', 'Lawn Bowls'),   ('MU', 'Music'),		('MO', 'Model Building'),
    ('OP', 'Opera'),		('OR', 'Origami'),		('PA', 'Painting'),		('PH', 'Photography'),
    ('PO', 'Pool'),			('PU', 'Puzzles'),		('RD', 'Reading'),		('RN', 'Running'),
    ('SC', 'Scrapbooking'),	('SI', 'Singing'),		('SH', 'Shooting'),		('SQ', 'Squash'),
    ('SW', 'Swimming'),	('TN', 'Tennis'),		('TH', 'Theatre'),		('TR', 'Trivia'),
    ('VI', 'Visual Art'),	('VO', 'Volunteering'), ('WA', 'Walking'),		('WR', 'Writing'),
    ('YO', 'Yoga'),
]

STATES = [
	("ACT", "Australian Capital Territory"),	("JBT", "Jervis Bay Territory"),	("NSW", "New South Wales"),
	("NT", "Northern Territory"),				("QLD", "Queensland"),				("SA", "South Australia"),
	("TAS", "Tasmania"),						("VIC", "Victoria"),				("WA", "Western Australia")
]

DATE_SPLIT	= "%Y-%m-%d"
GENESIS		= datetime.strptime("2022-10-10", DATE_SPLIT)

# km, according to https://en.wikipedia.org/wiki/Earth_radius
EARTH_RADIUS	= 6378.1

ADMIN_AUTH	= "adf200c9c93c7f73cbdbeb5d45d79315e86bcf20"
