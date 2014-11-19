from flask.ext.script import Manager, Server, Shell
import os, datetime, bcrypt
from flask.ext.security.utils import encrypt_password
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.admin.contrib.peewee import ModelView

from metroplaces import app, db, user_datastore
from metroplaces.models import (
	User,
	Role,
	UserRoles,
	Category,
	Place,
	PlaceFeatures,
	Feature,
	# Tag,
	# TagRelationship,
)
manager = Manager(app)
# manager.add_command("migrate", ManageMigrations())
manager.add_command("runserver", Server(host='0.0.0.0', port=5000))
manager.add_command("shell", Shell())

@manager.command
def add_places():
	"""add some places and features"""
	ezpasses = Feature.create(name="ezpasses",description="EZ Passes")
	misc = Category.create(name="uncategorized",description="Need some love")
	tapvendors = Category.create(name="tapvendors",description="TAP Vendors")

	Place.create(category=tapvendors,lon=-118.265179,lat=33.933915,address="11151 Avalon Blvd. Suite #108",city="Los Angeles",phone="3237772067",comment="No EZ Passes",name="1% Check Cashing",)
	Place.create(category=tapvendors,lon=-118.299846,lat=34.069185,address="280 S. Normandie",city="Los Angeles",phone="3233808588",comment="No EZ Passes",name="3RD & Normandie Check Cashing",)
	Place.create(category=tapvendors,lon=-118.295706,lat=34.069159,address="3653 W. 3RD St. ",city="Los Angeles",phone="2133834757",comment="No EZ Passes",name="3RD Street Check Cashing",)
	Place.create(category=tapvendors,lon=-118.247035,lat=34.146629,address="106 N. Glendale Ave.",city="Glendale",phone="8182410608",comment="",name="A TO Z CHECK CASHING",)
	Place.create(category=tapvendors,lon=-118.308272,lat=34.025800,address="1771 W. Jefferson Blvd.",city="Los Angeles",phone="3237351800",comment="",name="AAA Cash Advance Inc.",)
	Place.create(category=tapvendors,lon=-118.450497,lat=34.193762,address="14556 Vanowen St.",city="Van Nuys",phone="8187819011",comment="",name="Adams Liquor",)
	Place.create(category=tapvendors,lon=-118.291296,lat=34.034203,address="2404 S. Vermont Ave.",city="Los Angeles",phone="3237343117",comment="",name="Aloha Market",)
	Place.create(category=tapvendors,lon=-118.150879,lat=33.888472,address="15920 Downey Ave.",city="Paramount",phone="5626339542",comment="",name="Alondra Quick Check",)
	Place.create(category=tapvendors,lon=-118.249430,lat=34.052011,address="255 S Hill St",city="Los Angeles",phone="2136177910",comment="No EZ Passes",name="Angelus Mini Market",)
	Place.create(category=tapvendors,lon=-118.152096,lat=34.603818,address="1233 W. Rancho Vista Blvd.",city="Palmdale",phone="6612669150",comment="No EZ Passes",name="Antelope Valley Mall",)
	Place.create(category=tapvendors,lon=-118.118807,lat=34.649729,address="42210 6th Street West",city="Lancaster",phone="6617292222",comment="No EZ Passes",name="Antelope Valley Transit Authority",)
	Place.create(category=tapvendors,lon=-118.283690,lat=34.057352,address="2612 W. 8th St.",city="Los Angeles",phone="2133838380",comment="",name="Apulo Market",)
	Place.create(category=tapvendors,lon=-118.182988,lat=34.661415,address="2851 W. Ave L",city="Lancaster ",phone="6617224555",comment="EZ Passes ",name="AV Mail & More",)
	Place.create(category=tapvendors,lon=-118.348329,lat=33.945719,address="4147 W. Century Blvd......",city="Inglewood",phone="3106711505",comment="",name="Avalon Check Cashing",)
	Place.create(category=tapvendors,lon=-118.343936,lat=33.954162,address="11050 S. Prairie Ave.",city="Inglewood",phone="3104120300",comment="",name="Avalon Check Cashing #2",)
	Place.create(category=tapvendors,lon=-118.274190,lat=33.945860,address="105 W. Century Blvd.",city="Los Angeles",phone="3237777900",comment="",name="Avalon Check Cashing #3",)
	Place.create(category=tapvendors,lon=-117.916744,lat=34.139313,address="943 N. Vernon Ave",city="Azusa",phone="6268125140",comment="Resident/Seniors Only",name="Azusa Transportation Center",)
	Place.create(category=tapvendors,lon=-118.195347,lat=33.962089,address="4137 Santa Ana St",city="Huntington Park",phone="3235874362",comment="No EZ Passes",name="Band B Check Cashing Inc.",)
	Place.create(category=tapvendors,lon=-118.203676,lat=34.107416,address="5001 Monte Vista St.",city="Los Angeles",phone="3232567216",comment="No EZ Passes",name="Barneys Liquor",)
	Place.create(category=tapvendors,lon=-118.188424,lat=33.979164,address="6330 Pine Ave.",city="Bell",phone="3235886211",comment="Residents Only",name="Bell Community Center",)
	Place.create(category=tapvendors,lon=-118.150988,lat=34.169602,address="1377 N Fair Oaks Ave.",city="Pasadena",phone="6267941124",comment="",name="Berry &  Sweeney Pharmacy",)
	Place.create(category=tapvendors,lon=-118.296830,lat=34.076191,address="4028 Beverly Blvd",city="Los Angeles",phone="2133809815",comment="",name="Beverly Kenmore Check Cashing",)
	Place.create(category=tapvendors,lon=-118.215809,lat=34.073349,address="2430 N Broadway",city="Los Angeles",phone="3232767415",comment="",name="Broadway Check Cashing",)
	Place.create(category=tapvendors,lon=-118.320271,lat=34.170566,address="1301 W. Olive Ave.",city="Burbank",phone="NULL",comment="Resident/Seniors Only",name="Burbank Joslyn Center",)
	Place.create(category=tapvendors,lon=-118.224966,lat=33.973969,address="2602 E. Florence Ave.",city="Huntington Park",phone="7148631121",comment="",name="California Money Express",)
	Place.create(category=tapvendors,lon=-97.382924,lat=31.106085,address="3801 W. Temple Ave. BU #35",city="Pomona",phone="9098692859",comment="",name="Cal Poly Pomona",)
	Place.create(category=tapvendors,lon=-118.258984,lat=33.865287,address="1000 E. Victoria St.",city="Carson",phone="3102433006",comment="",name="Cal State Dominguez",)
	Place.create(category=tapvendors,lon=-118.170823,lat=34.063607,address="5151 State University Dr. ",city="Los Angeles",phone="3233436118",comment="",name="Cal State University Los Angeles",)
	Place.create(category=tapvendors,lon=-118.525807,lat=34.248946,address="18111 Nordhoff Street BH240",city="Northridge",phone="8186772488",comment="",name="California State University Northridge",)
	Place.create(category=tapvendors,lon=-118.245523,lat=34.039550,address="720 E 7th Street",city="Los Angeles",phone="2136279909",comment="",name="Campers Corner",)
	Place.create(category=tapvendors,lon=-118.461077,lat=34.407747,address="18792 Flying Tiger Drive",city="Santa Clarita",phone="6612841480",comment="No EZ Passes",name="Canyon Country Community Center",)
	Place.create(category=tapvendors,lon=-118.053242,lat=34.079798,address="9961 E. Valley Blvd",city="El Monte",phone="6264544895",comment="",name="Cash Connection Plus",)
	Place.create(category=tapvendors,lon=-118.144035,lat=34.674408,address="43535 Gadsden Avenue Suite F",city="Lancaster",phone="6617233130",comment="No EZ Passes",name="Cash it Quick",)
	Place.create(category=tapvendors,lon=-118.536555,lat=34.187090,address="18503 Victory Blvd.",city="Reseda",phone="8183421200",comment="",name="Cash it Quick",)
	Place.create(category=tapvendors,lon=-118.343399,lat=34.091211,address="1114 N. La Brea Avenue Unit 105",city="West Hollywood",phone="NULL",comment="",name="Cashnet Financial Services",)
	Place.create(category=tapvendors,lon=-118.312553,lat=34.090395,address="7071 1/2 Santa Monica Blvd.",city="Los Angeles",phone="3239627711",comment="",name="Cashnet Financial Services",)
	Place.create(category=tapvendors,lon=-118.199261,lat=33.943869,address="4149 Tweedy blvd",city="South Gate",phone="3235698708",comment="",name="Check 4 Cash",)
	Place.create(category=tapvendors,lon=-118.239200,lat=34.060008,address="652-B N. Broadway",city="Los Angeles",phone="2136809230",comment="",name="China Bookstore",)
	Place.create(category=tapvendors,lon=-118.292065,lat=34.068636,address="311 S Vermont ave",city="Los Angeles",phone="2133813223",comment="",name="City Check Cashers",)
	Place.create(category=tapvendors,lon=-118.291620,lat=34.057080,address="828 S Vermont Ave",city="Los Angeles",phone="2133813223",comment="",name="City Check Cashers",)
	Place.create(category=tapvendors,lon=-118.420198,lat=34.247169,address="9767 Laurel Canyon Blvd",city="Pacoima",phone="2133813223",comment="",name="City Check Cashers",)
	Place.create(category=tapvendors,lon=-118.127050,lat=34.092629,address="111 South 1st St",city="Alhambra",phone="6265703268",comment="Residents Only",name="City of Alhambra",)
	Place.create(category=tapvendors,lon=-117.905547,lat=34.134339,address="213 East Foothill Dr.",city="Azusa",phone="6268125200",comment="",name="City of Azusa",)
	Place.create(category=tapvendors,lon=-117.964368,lat=34.085845,address="4100 Baldwin Park Blvd",city="Baldwin Park",phone="6269622625",comment="",name="City of Baldwin Park",)
	Place.create(category=tapvendors,lon=-118.400250,lat=34.072722,address="455 N. Rexford Dr",city="Beverly Hills",phone="3102852409",comment="Resident/Seniors Only",name="City of Beverly Hills",)
	Place.create(category=tapvendors,lon=-118.320271,lat=34.170566,address="1301 W. Olive Ave",city="Burbank",phone="8182385360",comment="Resident/Seniors Only",name="City of Burbank Joslyn Center",)
	Place.create(category=tapvendors,lon=-118.156185,lat=34.000714,address="2535 Commerce Way",city="Commerce",phone="3237224805 x2336",comment="Residents Only",name="City of Commerce",)
	Place.create(category=tapvendors,lon=-117.889399,lat=34.087701,address="125 E. College St.",city="Covina",phone="6263845520",comment="Senior and Disabled Residents Only",name="City of Covina",)
	Place.create(category=tapvendors,lon=-118.174684,lat=33.959369,address="5220 Santa Ana Street",city="Cudahy",phone="3237735143",comment="Resident/Seniors Only",name="City of Cudahy",)
	Place.create(category=tapvendors,lon=-117.830178,lat=34.000146,address="21801 Copley Dr.",city="Diamond Bar",phone="9098397050",comment="",name="City of Diamond Bar",)
	Place.create(category=tapvendors,lon=-118.128440,lat=33.940196,address="11111 Brookshire Ave",city="Downey",phone="5629047251",comment="",name="City of Downey",)
	Place.create(category=tapvendors,lon=-118.035829,lat=34.075646,address="3650 Center St.",city="El Monte",phone="6265802242",comment="Residents Only",name="City of El Monte",)
	Place.create(category=tapvendors,lon=-118.415379,lat=33.920527,address="350 Main St.",city="El Segundo",phone="3105242705",comment="Residents Only",name="City of El Segundo",)
	Place.create(category=tapvendors,lon=-117.864828,lat=34.135381,address="116 E. Foothill Blvd.",city="Glendora",phone="6268524814",comment="Residents Only",name="City of Glendora",)
	Place.create(category=tapvendors,lon=-118.341713,lat=33.916442,address="3901 W. El Segundo Blvd.",city="Hawthorne",phone="3103491640",comment="Residents Only",name="City of Hawthorne",)
	Place.create(category=tapvendors,lon=-118.395789,lat=33.863729,address="1315 Valley Dr.",city="Hermosa Beach",phone="3103180256",comment="Sr/Dis College Student Residents Only",name="City of Hermosa Beach",)
	Place.create(category=tapvendors,lon=-118.218603,lat=33.978847,address="6550 Miles Ave.",city="Huntington Park",phone="3235846237",comment="Residents Only",name="City of Huntington Park",)
	Place.create(category=tapvendors,lon=-118.354828,lat=33.963068,address="One West Manchester Blvd.",city="Inglewood",phone="3104128729",comment="Residents Only",name="City of Inglewood",)
	Place.create(category=tapvendors,lon=-117.950291,lat=34.019799,address="15900 E. Main St.",city="La Puente",phone="6268551500",comment="Residents Only",name="City of La Puente",)
	Place.create(category=tapvendors,lon=-117.765209,lat=34.111982,address="3660 D St",city="La Verne",phone="9095968700",comment="Residents Only",name="City La Verne",)
	Place.create(category=tapvendors,lon=-118.410759,lat=33.887250,address="1400 Highland Ave",city="Manhattan Beach",phone="3108025561",comment="Residents Only",name="City of Manhattan Beach",)
	Place.create(category=tapvendors,lon=-118.001836,lat=34.149467,address="119 W. Palm Ave.",city="Monrovia",phone="6262568246",comment="Residents Only",name="City of Monrovia",)
	Place.create(category=tapvendors,lon=-118.143534,lat=34.147643,address="100 N Garfield Ave.",city="Pasadena",phone="6267444428",comment="Residents Only",name="City of Pasadena<br/>Metro Senior Passes Only",)
	Place.create(category=tapvendors,lon=-118.089847,lat=33.980042,address="6767 Passons Blvd.",city="Pico Rivera",phone="5628014227",comment="Residents Only",name="City of Pico Rivera",)
	Place.create(category=tapvendors,lon=-118.076800,lat=34.080687,address="8838 E. Valley Blvd.",city="Rosemead",phone="6265692250",comment="Residents Only",name="City of Rosemead",)
	Place.create(category=tapvendors,lon=-118.438941,lat=34.284113,address="117 Macneil St.",city="San Fernando",phone="8188981244",comment="Residents Only",name="City of San Fernando",)
	Place.create(category=tapvendors,lon=-118.109328,lat=34.099117,address="250 S. Mission Dr.",city="San Gabriel",phone="6263082875",comment="Residents/Seniors Only",name="City of San Gabriel",)
	Place.create(category=tapvendors,lon=-118.499675,lat=34.411712,address="20850 Centre Pointe Pkwy",city="Santa Clarita",phone="6612503700",comment="No EZ Passes",name="City of Santa Clarita Aquatics Center",)
	Place.create(category=tapvendors,lon=-118.553837,lat=34.412681,address="23920 Valencia Blvd.",city="Santa Clarita",phone="6612864099",comment="No EZ Passes",name="City of Santa Clarita City Hall",)
	Place.create(category=tapvendors,lon=-118.577125,lat=34.448945,address="28250 Constellation Road",city="Santa Clarita",phone="6612956328",comment="",name="City of Santa Clarita Transit Maintenance Facility",)
	Place.create(category=tapvendors,lon=-118.046304,lat=34.044570,address="1415 Santa Anita",city="South El Monte",phone="6265796540",comment="Residents Only",name="City of South El Monte",)
	Place.create(category=tapvendors,lon=-118.187806,lat=33.946568,address="9520 Hildreth Ave.",city="South Gate",phone="3235635754",comment="Resident/Seniors Only",name="City of South Gate",)
	Place.create(category=tapvendors,lon=-118.156150,lat=34.113726,address="1102 Oxley St.",city="South Pasadena",phone="6264037360",comment="Residents Only",name="City of South Pasadena",)
	Place.create(category=tapvendors,lon=-117.842324,lat=34.026361,address="21201 La Puente Rd",city="Walnut",phone="9095957543",comment="Regular EZ Passes Only",name="City of Walnut",)
	Place.create(category=tapvendors,lon=-118.370701,lat=34.090435,address="8300 Santa Monica Blvd.",city="West Hollywood",phone="3238486370",comment="Residents Only",name="City of West Hollywood",)
	Place.create(category=tapvendors,lon=-85.893207,lat=37.474611,address="13225 Walnut St.",city="Whittier",phone="5625679482",comment="Residents Only",name="City of Whittier Senior Center",)
	Place.create(category=tapvendors,lon=-118.252951,lat=34.045070,address="227 W. 7th Street",city="Los Angeles",phone="2136275234",comment="",name="Color Check Cashing",)
	Place.create(category=tapvendors,lon=-118.447821,lat=34.288378,address="1542 San Fernando Rd",city="San Fernando",phone="8187862188",comment="",name="Confetti Liquor",)
	Place.create(category=tapvendors,lon=-118.410817,lat=34.274345,address="12773 Van Nuys Blvd.",city="Pacoima",phone="8188901255",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.131900,lat=34.168306,address="1298 N Lake Ave",city="Pasadena",phone="6267942970",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.278645,lat=33.960326,address="8565 S. Broadway - #1",city="Los Angeles",phone="3237586632",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.248246,lat=33.975199,address="1457 E. Florence Ave. Unit 115",city="Los Angeles",phone="3235827665",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.331247,lat=33.989247,address="3401 W. Slauson Ave.",city="Los Angeles",phone="3232923651",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.450232,lat=34.235447,address="9100 Van Nuys Blvd.",city="Panorama city",phone="8188301400",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.164709,lat=33.970751,address="6821-A S. Eastern Ave.",city="Bell Gardens",phone="3237718448",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.149469,lat=34.018997,address="5623 E. Whittier Blvd.",city="Los Angeles",phone="3238889632",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.333199,lat=34.101842,address="6565 Hollywood Blvd.",city="Hollywood",phone="3234642718",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.329770,lat=34.101877,address="6401 Hollywood Blvd.",city="Hollywood",phone="3234664808",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.252092,lat=34.046915,address="559 S. Broadway",city="Los Angeles",phone="2136241666",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.090110,lat=34.064954,address="3106 San Gabriel Blvd.",city="Rosemead",phone="6262800380",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.243511,lat=33.943263,address="1669 E. 103rd St",city="Los Angeles",phone="3235696245",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.327257,lat=34.039687,address="4020 Washington Blvd.",city="Los Angeles",phone="3237349974",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.222784,lat=33.895767,address="148 E. Compton Blvd",city="Compton",phone="3105379239",comment="",name="Continental Currency Services Inc. #317",)
	Place.create(category=tapvendors,lon=-118.467549,lat=34.001001,address="303 Lincoln Blvd",city="Venice",phone="3103925985",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.289598,lat=33.988362,address="5824 S. Vermont Ave",city="Los Angeles",phone="3237515044",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.189510,lat=33.782616,address="1301 Long Beach Blvd",city="Long Beach",phone="5625991550",comment="",name="Continental Currency Services Inc. #408",)
	Place.create(category=tapvendors,lon=-118.237696,lat=33.903592,address="739 W Rosecrans Ave",city="Compton",phone="3106383021",comment="",name="Continental Currency Services Inc. #015",)
	Place.create(category=tapvendors,lon=-118.370042,lat=34.216516,address="8026 Vineland Ave",city="Sun Valley",phone="8187683740",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.372998,lat=34.021736,address="5804 Rodeo Rd.",city="Los Angeles",phone="3108374422",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.188469,lat=33.775486,address="335 E. 7th St.",city="Long Beach",phone="5624367078",comment="",name="Continental Currency Services Inc. #414",)
	Place.create(category=tapvendors,lon=-118.153058,lat=33.874793,address="3461 E. Artesia Blvd.",city="Long Beach",phone="5625312320",comment="",name="Continental Currency Services Inc. #513",)
	Place.create(category=tapvendors,lon=-118.337838,lat=34.013684,address="4050 Victoria Ave.",city="Los Angeles",phone="3232966052",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.405648,lat=34.016370,address="10716 W. Washington Blvd.",city="Culver City",phone="3102042115",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.238748,lat=33.926882,address="11712 Wilmington Ave.",city="Los Angeles",phone="3235677200",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.225174,lat=33.964792,address="8116 Long Beach Blvd.",city="South Gate",phone="3235877545",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.320093,lat=33.960173,address="2401 W. Manchester Blvd.",city="Inglewood",phone="3237591000",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.142625,lat=33.903982,address="13542 Lakewood Blvd. #F",city="Bellflower",phone="5626340254",comment="",name="Continental Currency Services Inc. #274",)
	Place.create(category=tapvendors,lon=-118.249342,lat=34.048984,address="400 S Broadway",city="Los Angeles",phone="2136239852",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.228820,lat=33.974847,address="2451 E. Florence Ave.",city="Huntington Park",phone="3235888664",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.396848,lat=34.186444,address="12100 Victory Blvd.",city="North Hollywood",phone="8187693228",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.308991,lat=34.040152,address="1890 S. Western Ave.",city="Los Angeles",phone="3237348632",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.326821,lat=34.048063,address="4201 W. Pico Blvd.",city="Los Angeles",phone="3239384070",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.141325,lat=34.157803,address="447 E. Orange Grove Ave.",city="Pasadena",phone="6265640712",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.255202,lat=34.133711,address="1023-B S. Brand Blvd",city="Glendale",phone="8182433639",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.308910,lat=34.010863,address="16751677 W. Martin Luther King Jr Blvd.",city="Los Angeles",phone="3232962669",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.326419,lat=33.932677,address="11220 S. Crenshaw Blvd.",city="Inglewood",phone="3237561333",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.229867,lat=33.974491,address="2400 E. Florence Avenue",city="Huntington Park",phone="3235825895",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.081716,lat=33.912968,address="12854 Pioneer Blvd.",city="Norwalk",phone="5628682018",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.292258,lat=34.004054,address="4373 S. Vermont Ave.",city="Los Angeles",phone="3232326006",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.207001,lat=34.046648,address="2417 E. Cesar Chavez",city="Los Angeles",phone="3232604830",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.065738,lat=33.971264,address="11515 Washington Blvd.",city="Whittier",phone="5629081000",comment="",name="Continental Currency Services Inc.",)
	Place.create(category=tapvendors,lon=-118.210003,lat=34.065698,address="3000 N. Main St.",city="Los Angeles",phone="3232254888",comment="No EZ Passes",name="Corner Store Liquor #2",)
	Place.create(category=tapvendors,lon=-118.151957,lat=34.094559,address="16 S. Fremont Ave.",city="Alhambra",phone="6264382016",comment="No EZ Passes",name="Corner Store Liquor #1",)
	Place.create(category=tapvendors,lon=-117.883058,lat=34.094157,address="815 N Barranca Avenue",city="Covina",phone="6268587219",comment="Resident/Seniors Only",name="Covina Joslyn",)
	Place.create(category=tapvendors,lon=-118.277786,lat=34.065491,address="2543 W. 3rd Street",city="Los Angeles",phone="2133880188",comment="No EZ Passes",name="Crest Jr. Market",)
	Place.create(category=tapvendors,lon=-118.170823,lat=34.063607,address="5151 University Drive Building C",city="Los Angeles",phone="3233435277",comment="",name="CSULA",)
	Place.create(category=tapvendors,lon=-118.291717,lat=34.089931,address="1006 N. Vermont Ave.",city="Los Angeles",phone="3236441330",comment="",name="Digital Currency/Unipago CA",)
	Place.create(category=tapvendors,lon=-118.072606,lat=33.831419,address="12173 Carson St.",city="Hawaiian Gardens",phone="5624677488",comment="",name="E MONEY EXPRESS #1",)
	Place.create(category=tapvendors,lon=-118.187145,lat=33.965018,address="7705 Atlantic Ave. ",city="Cudahy",phone="5622935141",comment="",name="E Money Express #5",)
	Place.create(category=tapvendors,lon=-118.240240,lat=34.019914,address="1901 S Alameda",city="Los Angeles",phone="2137478408",comment="No EZ Passes",name="E Z Check Cashing",)
	Place.create(category=tapvendors,lon=-118.310407,lat=34.090397,address="5520 Santa Monica Blvd",city="Los Angeles",phone="3234662703",comment="",name="East Hollywood Currency Services",)
	Place.create(category=tapvendors,lon=-118.117133,lat=34.689626,address="1018 E. Ave J",city="Lancaster",phone="6617261321",comment="No EZ Passes",name="Eastside Checking Cashing",)
	Place.create(category=tapvendors,lon=-118.263653,lat=34.078159,address="1115 N. Alvarado St. ",city="Los Angeles",phone="2134132677",comment="",name="El Rancho Market",)
	Place.create(category=tapvendors,lon=-118.411220,lat=33.920117,address="339 Sheldon St.",city="El Segundo",phone="3105242701",comment="Resident/Seniors Only",name="El Segundo Joslyn Center",)
	Place.create(category=tapvendors,lon=-118.178306,lat=34.084435,address="3327 N. Eastern Ave.",city="Los Angeles",phone="3232214246",comment="No EZ Passes",name="El Sereno Liquor",)
	Place.create(category=tapvendors,lon=-118.345730,lat=34.045777,address="4968 Venice Blvd.",city="Los Angeles",phone="3239370688",comment="",name="Envios Mi Tierra Dinero En Segundos",)
	Place.create(category=tapvendors,lon=-118.308990,lat=34.076151,address="254 N. Western Ave.",city="Los Angeles",phone="3234672101",comment="",name="Ethical Drug",)
	Place.create(category=tapvendors,lon=-118.251482,lat=34.046862,address="544 S. Broadway",city="Los Angeles",phone="2134893558",comment="",name="FAMIMA Broadway",)
	Place.create(category=tapvendors,lon=-118.254855,lat=34.052996,address="305 S Grand Ave. Suite R2B",city="Los Angeles",phone="2136284000",comment="",name="FAMIMA California Plaza",)
	Place.create(category=tapvendors,lon=-118.256606,lat=34.051447,address="505 S. Flower Street Suite 520",city="Los Angeles",phone="2136233236",comment="",name="FAMIMA City National Plaza",)
	Place.create(category=tapvendors,lon=-118.254809,lat=34.048788,address="525 W. 6th Street",city="Los Angeles",phone="NULL",comment="",name="FAMIMA Pacific Center",)
	Place.create(category=tapvendors,lon=-118.258417,lat=34.048705,address="727 W. 7th Street Suite G-735",city="Los Angeles",phone="2136277334",comment="",name="FAMIMA Roosevelt",)
	Place.create(category=tapvendors,lon=-118.236600,lat=34.055833,address="800 N. Alameda Street",city="Los Angeles",phone="2136131433",comment="",name="FAMIMA Union Station",)
	Place.create(category=tapvendors,lon=-118.257536,lat=34.048670,address="700 Wilshire Boulevard",city="Los Angeles",phone="NULL",comment="",name="FAMIMA Wilshire",)
	Place.create(category=tapvendors,lon=-118.370660,lat=34.201671,address="7215 Vineland Ave",city="Sun Valley",phone="8187652481",comment="No EZ Passes",name="Fiesta Liquor",)
	Place.create(category=tapvendors,lon=-118.137791,lat=34.098723,address="1332 W. Alhambra Rd.",city="Alhambra",phone="6262822143",comment="",name="Fisher Market",)
	Place.create(category=tapvendors,lon=-118.222708,lat=33.973930,address="2688 E Florence Ave",city="Huntington Park",phone="3235858515",comment="",name="Florence Check Cashing",)
	Place.create(category=tapvendors,lon=-118.264650,lat=33.975171,address="605 E. Florence Ave",city="Los Angeles",phone="3237530855",comment="",name="Florence Shell",)
	Place.create(category=tapvendors,lon=-117.927476,lat=33.993587,address="1600 Azusa Ave. #571",city="City of Industry",phone="8007433463",comment="",name="Foothill Transit",)
	Place.create(category=tapvendors,lon=-117.749964,lat=34.059627,address="100 W. Commercial Ave.",city="Pomona",phone="8007433463",comment="",name="Foothill Transit",)
	Place.create(category=tapvendors,lon=-118.042477,lat=34.071761,address="3501 Santa Anita Ave. 2nd Floor",city="El Monte",phone="8007433463",comment="",name="Foothill Transit",)
	Place.create(category=tapvendors,lon=-117.716433,lat=34.094486,address="200 W. First Street",city="Claremont",phone="8007433463",comment="",name="Foothill Transit",)
	Place.create(category=tapvendors,lon=-117.926329,lat=34.070033,address="100 S. Vincent Ave.",city="West Covina",phone="8007433463",comment="",name="Foothill Transit",)
	Place.create(category=tapvendors,lon=-118.309222,lat=34.091234,address="1111 N. Western Ave.",city="Los Angeles",phone="3234678494",comment="",name="Four Aces Market",)
	Place.create(category=tapvendors,lon=-118.288600,lat=34.040340,address="1479 W. Washington Blvd.",city="Los Angeles",phone="2137499993",comment="",name="Garden Liquor",)
	Place.create(category=tapvendors,lon=-118.309721,lat=33.905114,address="13999 S. Western Ave.",city="Gardena",phone="3109658888",comment="Stored Value and EZ Pass Only",name="Gardena Municipal Bus Lines",)
	Place.create(category=tapvendors,lon=-118.253452,lat=34.050181,address="555 West 5th St.",city="Los Angeles",phone="2136134410",comment="",name="Gas Tower",)
	Place.create(category=tapvendors,lon=-117.860708,lat=34.136807,address="410 E. Dalton Ave.",city="Glendora",phone="6268524814",comment="",name="Glendora Transportation Services",)
	Place.create(category=tapvendors,lon=-118.426009,lat=34.242621,address="13439 Osborne St. #11",city="Arleta",phone="8188968585",comment="No EZ Passes",name="Globe Check Cashing",)
	Place.create(category=tapvendors,lon=-118.247400,lat=33.992848,address="5500 Compton Ave.",city="Los Angeles",phone="3232345990",comment="",name="Grace Super Market",)
	Place.create(category=tapvendors,lon=-118.270015,lat=34.061611,address="1840 W. 3rd Street",city="Los Angeles",phone="2134836343",comment="",name="Green Circle Market",)
	Place.create(category=tapvendors,lon=-118.254697,lat=34.019278,address="2524 S. Central Ave.",city="Los Angeles",phone="3232333900",comment="",name="Guadalajara Chk Cashing",)
	Place.create(category=tapvendors,lon=-118.208081,lat=34.042950,address="2514 E. 1st St.",city="Los Angeles",phone="3235264213",comment="",name="Guadalajara Chk Cashing",)
	Place.create(category=tapvendors,lon=-118.245182,lat=34.003628,address="1610 E. Vernon Ave.",city="Los Angeles",phone="3232321917",comment="",name="Gumbo Market",)
	Place.create(category=tapvendors,lon=-118.222002,lat=34.083811,address="2600 N. Figueroa",city="Los Angeles",phone="3232224595",comment="No EZ Passes",name="Hancore Investments",)
	Place.create(category=tapvendors,lon=-118.344085,lat=33.915960,address="12823 S. Prairie Ave.",city="Hawthorne",phone="3109781100",comment="",name="Hawthorne Quick Check",)
	Place.create(category=tapvendors,lon=-118.310589,lat=34.096059,address="1360 N St. Andrews",city="Los Angeles",phone="3239573906",comment="Resident/Seniors Only",name="Hollywood Senior Center",)
	Place.create(category=tapvendors,lon=-118.255257,lat=34.043156,address="824A S. Broadway",city="Los Angeles",phone="2136276270",comment="",name="Hopertunity Inc.",)
	Place.create(category=tapvendors,lon=-118.309402,lat=33.997767,address="5001 S. Western Ave.",city="Los Angeles",phone="3232994919",comment="",name="Hums Market",)
	Place.create(category=tapvendors,lon=-118.291368,lat=34.056078,address="864 S. Vermont Ave. ",city="Los Angeles",phone="2135683536",comment="",name="Ideal Check Cashing",)
	Place.create(category=tapvendors,lon=-118.347950,lat=33.970797,address="330 Centinela Ave.",city="Inglewood",phone="3104125338",comment="Resident/Seniors Only",name="Inglewood Senior Center",)
	Place.create(category=tapvendors,lon=-118.280821,lat=34.042052,address="1154 W. Venice Blvd.",city="Los Angeles",phone="2137486033",comment="",name="J & H Liquor",)
	Place.create(category=tapvendors,lon=-118.192738,lat=34.035939,address="3474 E. First Street",city="Los Angeles",phone="3232649915",comment="",name="J & V Macias Inc.",)
	Place.create(category=tapvendors,lon=-118.289659,lat=34.055880,address="2812 James M. Wood Blvd.",city="Los Angeles",phone="2133883900",comment="No EZ Passes",name="James Wood Processing Company",)
	Place.create(category=tapvendors,lon=-118.326605,lat=34.089927,address="1060 vine st",city="Los Angeles",phone="3239602503",comment="No EZ Passes",name="Jennifers Bar",)
	Place.create(category=tapvendors,lon=-118.463707,lat=34.415921,address="28601 Soledad Canyon Road",city="Santa Clarita",phone="6612512720",comment="No EZ Passes",name="Jo Anne Darcy Library Canyon Country",)
	Place.create(category=tapvendors,lon=-118.277176,lat=34.010899,address="4000 Broadway Pl.",city="Los Angeles",phone="3109384093",comment="",name="Johnny's Liqour",)
	Place.create(category=tapvendors,lon=-118.180487,lat=34.066477,address="2017 N. Eastern Ave.",city="Los Angeles",phone="3232236626",comment="",name="Johnnie's Market",)
	Place.create(category=tapvendors,lon=-118.301355,lat=34.057446,address="3334 W. 8th Street",city="Los Angeles",phone="3234606772",comment="",name="Jons Market",)
	Place.create(category=tapvendors,lon=-118.263709,lat=34.077883,address="2105 W. Sunset Blvd.",city="Los Angeles",phone="6266273598",comment="No EZ Passes",name="King Liquor",)
	Place.create(category=tapvendors,lon=-118.309467,lat=34.062036,address="3807 wilshire blvd.",city="Los Angeles",phone="2137389988",comment="No EZ Passes",name="Korean Senior Club",)
	Place.create(category=tapvendors,lon=-118.376823,lat=34.073405,address="8506 W. 3rd. St. ",city="Los Angeles",phone="3106528100",comment="",name="La Cienega Check Casking",)
	Place.create(category=tapvendors,lon=-118.375906,lat=34.062517,address="8400 Gregory Way",city="Beverly Hills",phone="3102856810",comment="Resident/Seniors Only",name="La Cienega Community Center",)
	Place.create(category=tapvendors,lon=-118.245794,lat=34.056527,address="225 N. Hill St. Room 114",city="Los Angeles",phone="2139742140",comment="",name="LA County Tax Collector",)
	Place.create(category=tapvendors,lon=-118.258853,lat=34.039645,address="1106 S. Broadway",city="Los Angeles",phone="2137415411",comment="",name="LA Job Corps",)
	Place.create(category=tapvendors,lon=-118.247473,lat=33.999989,address="4800 Compton Ave.",city="Los Angeles",phone="3232314765",comment="",name="La Mexicana",)
	Place.create(category=tapvendors,lon=-118.269491,lat=34.032800,address="400 W. Washington Blvd.",city="Los Angeles",phone="2137637225",comment="",name="LA Trade Tech",)
	Place.create(category=tapvendors,lon=-118.339985,lat=34.102450,address="6801 Hollywood Blvd. Suite #104",city="Hollywood",phone="3234676412",comment="",name="LA Tourism Visitors Center",)
	Place.create(category=tapvendors,lon=-118.292669,lat=34.089214,address="855 N. Vermont",city="Los Angeles",phone="3239534000",comment="",name="LA City College",)
	Place.create(category=tapvendors,lon=-118.241971,lat=34.052553,address="201 N Los Angeles St # 18B",city="Los Angeles",phone="2138082273",comment="",name="LADOT",)
	Place.create(category=tapvendors,lon=-118.397522,lat=34.275721,address="11950 Foothill Blvd.",city="Lake View Terrace",phone="8188343350",comment="No EZ Passes",name="Lakeview Farm Market",)
	Place.create(category=tapvendors,lon=-118.128361,lat=34.065775,address="400 W. Emerson Ave.",city="Monterey Park",phone="6263071395",comment="Resident/Seniors Only",name="Langely Senior Center",)
	Place.create(category=tapvendors,lon=-118.396522,lat=34.214934,address="7945 Laurel Canyon Blvd.",city="North Hollywood",phone="8187648027",comment="",name="Laurel Canyon Check Cashing",)
	Place.create(category=tapvendors,lon=-118.318124,lat=34.101943,address="5901 Hollywood Blvd.",city="Hollywood",phone="3234622891",comment="",name="Liquor To GoGo",)
	Place.create(category=tapvendors,lon=-118.257862,lat=34.140851,address="424S. Central Ave.",city="Glendale ",phone="8185007612",comment="",name="Liquor Zone",)
	Place.create(category=tapvendors,lon=-118.191689,lat=33.767993,address="130 E. 1st Street",city="Long Beach",phone="5625912301",comment="No Metro Passes",name="Long Beach Transit & Visitor Center",)
	Place.create(category=tapvendors,lon=-117.991893,lat=34.521514,address="7715 Pearblossom Hwy.",city="Littlerock",phone="6615266570",comment="No EZ Passes",name="Los Hermanos Market",)
	Place.create(category=tapvendors,lon=-118.045983,lat=34.572207,address="37951 47th Street East Suite A7",city="Palmdale",phone="6612853000",comment="No EZ Passes",name="Mail America",)
	Place.create(category=tapvendors,lon=-118.082807,lat=34.558889,address="2551 E. Ave S Suite G",city="Palmdale",phone="6612730999",comment="No EZ Passes",name="Mail America",)
	Place.create(category=tapvendors,lon=-118.098384,lat=34.689517,address="1752 East Avenue J",city="Lancaster",phone="6619406343",comment="No EZ Passes",name="Mail America",)
	Place.create(category=tapvendors,lon=-118.112194,lat=34.704241,address="1025 W. Ave I",city="Lancaster",phone="6619456060",comment="No EZ Passes",name="Mail America",)
	Place.create(category=tapvendors,lon=-118.457454,lat=34.417388,address="18565 Soledad Canyon Road",city="Santa Clarita",phone="6612992295",comment="",name="Mail America Albertson's Center",)
	Place.create(category=tapvendors,lon=-118.182988,lat=34.661415,address="2851 W. Avenue L",city="Lancaster",phone="6617224555",comment="No EZ Passes",name="Mail N More",)
	Place.create(category=tapvendors,lon=-118.256844,lat=34.034742,address="1234 S. Maple St. ",city="Los Angeles",phone="2137470306",comment="",name="Maple Liquor",)
	Place.create(category=tapvendors,lon=-118.291993,lat=34.057447,address="801 S. Vermont Avenue #104",city="Los Angeles",phone="2133829718",comment="No EZ Passes",name="Martin Pharmacy",)
	Place.create(category=tapvendors,lon=-118.202952,lat=33.988488,address="3436 Slauson Ave.",city="Maywood",phone="3235810933",comment="No EZ Passes",name="Maywood Check Cashing",)
	Place.create(category=tapvendors,lon=-118.233255,lat=34.054714,address="One Gateway Plaza",city="Los Angeles",phone="",comment="",name="Metro Customer Center East Portal",)
	Place.create(category=tapvendors,lon=-118.170770,lat=34.023592,address="4501 B. Whittier Blvd.",city="Los Angeles",phone="",comment="",name="Metro Customer Center",)
	Place.create(category=tapvendors,lon=-118.290832,lat=34.062462,address="3183 W. Wilshire Blvd Unit #174",city="Los Angeles",phone="",comment="",name="Metro Customer Center",)
	Place.create(category=tapvendors,lon=-118.335784,lat=34.009930,address="3650 W. Martin Luther King Blvd. Suite 101 B",city="Los Angeles",phone="",comment="",name="Metro Customer Center",)
	Place.create(category=tapvendors,lon=-118.268239,lat=34.010737,address="4007 S. San Pedro",city="Los Angeles",phone="3232333120",comment="No EZ Passes",name="Mexico Check Cashing",)
	Place.create(category=tapvendors,lon=-118.278068,lat=33.974465,address="7200 S Broadway",city="Los Angeles",phone="3237598894",comment="",name="Midtown Cashing",)
	Place.create(category=tapvendors,lon=-118.392788,lat=34.237803,address="9311 San Fernando Rd.#102",city="Sun Valley",phone="8187670152",comment="",name="Mike's Liquor",)
	Place.create(category=tapvendors,lon=-118.224966,lat=33.973969,address="2602 E. Florence Ave.",city="Huntington Park",phone="3235821777",comment="",name="Money Express",)
	Place.create(category=tapvendors,lon=-118.115785,lat=34.006442,address="400 S. Taylor Avenue",city="Montebello",phone="3239627711",comment="No EZ Passes",name="Montebello Transportation",)
	Place.create(category=tapvendors,lon=-117.847584,lat=34.046502,address="1100 Grand Ave.",city="Walnut",phone="9095945611",comment="",name="Mt. San Antonio College",)
	Place.create(category=tapvendors,lon=-118.191414,lat=34.024225,address="3821 E. Whittier Blvd.",city="Los Angeles",phone="3238992184",comment="",name="Mundo Check Cashing",)
	Place.create(category=tapvendors,lon=-118.242650,lat=34.004317,address="1713 E. Vernon Ave #113",city="Los Angeles ",phone="2132351111",comment="",name="Mundo Check Cashing",)
	Place.create(category=tapvendors,lon=-118.155366,lat=34.019986,address="5342 E. Whittier Blvd",city="Los Angeles",phone="3237267001",comment="",name="Mundo Check Cashing",)
	Place.create(category=tapvendors,lon=-118.285780,lat=34.047279,address="2261 W. Pico Blvd.",city="Los Angeles",phone="2133883848",comment="",name="Mundo Check Cashing",)
	Place.create(category=tapvendors,lon=-118.156733,lat=34.022290,address="705 S Atlantic Blvd",city="Los Angeles",phone="3232660661",comment="",name="Mundo Check Cashing",)
	Place.create(category=tapvendors,lon=-118.283843,lat=34.052698,address="2411 W. Olympic Blvd.",city="Los Angeles",phone="2133658065",comment="",name="Mundo Check Cashing",)
	Place.create(category=tapvendors,lon=-118.183698,lat=34.119726,address="6479 N. Figueroa Avenue",city="Highland Park",phone="3232540082",comment="",name="Mundo Check Cashing",)
	Place.create(category=tapvendors,lon=-118.150826,lat=34.181609,address="2087 N. Fair Oaks Ave. #B",city="Altadena",phone="6267979077",comment="",name="Mundo Check Cashing",)
	Place.create(category=tapvendors,lon=-118.359348,lat=34.184544,address="4420 W. Victory Blvd.",city="Burbank",phone="8188469911",comment="",name="Nelson Liquor",)
	Place.create(category=tapvendors,lon=-118.525734,lat=34.379720,address="22421 Market Street",city="Santa Clarita",phone="6612864006",comment="No EZ  Passes",name="Newhall Community Center",)
	Place.create(category=tapvendors,lon=-118.292503,lat=34.069332,address="3525 W. 3rd Street #5",city="Los Angeles",phone="2133838840",comment="",name="New Hampshire Check Cashing",)
	Place.create(category=tapvendors,lon=-118.080611,lat=34.000209,address="9211 Whittier Blvd.",city="Pico Rivera",phone="5626997112",comment="No EZ Passes",name="New Tower Check Cashing",)
	Place.create(category=tapvendors,lon=-118.196802,lat=34.107878,address="5401 N Figueuroa",city="Los Angeles",phone="3232549516",comment="No EZ Passes",name="New Tower Check Cashing",)
	Place.create(category=tapvendors,lon=-118.300619,lat=34.052951,address="3003 W. Olympic Blvd. #101",city="Los Angeles",phone="2133863001",comment="No EZ Passes",name="Normandy Pharmacy ",)
	Place.create(category=tapvendors,lon=-118.215445,lat=34.064246,address="2409 N. Daly St.",city="Los Angeles",phone="3232256285",comment="",name="North East Food Stamps",)
	Place.create(category=tapvendors,lon=-118.050582,lat=34.078126,address="10103 Valley Blvd.",city="El Monte",phone="6264436692",comment="",name="North East Food Stamps",)
	Place.create(category=tapvendors,lon=-118.061447,lat=33.916592,address="12650 E. Imperial Hwy.",city="Norwalk",phone="5629295550",comment="",name="Norwalk Transit",)
	Place.create(category=tapvendors,lon=-118.277585,lat=34.054950,address="760 S. Alvarado Street",city="Los Angeles",phone="2134837449",comment="No EZ Passes",name="Ocean Liquor",)
	Place.create(category=tapvendors,lon=-118.530276,lat=34.381616,address="24500 Main Street",city="Santa Clarita",phone="6612590750",comment="No EZ Passes",name="Old Town Newhall Library",)
	Place.create(category=tapvendors,lon=-118.309844,lat=34.052882,address="3323 W. Olympic Blvd.",city="Los Angeles",phone="3237347385",comment="",name="Olympia Pharmacy",)
	Place.create(category=tapvendors,lon=-118.206261,lat=34.018755,address="3352 E. Olympic Blvd.",city="Los Angeles",phone="3232610985",comment="",name="Olympic Check Cashing",)
	Place.create(category=tapvendors,lon=-118.181105,lat=34.018911,address="4269 E. Olympic Blvd.",city="Los Angeles",phone="3232646060",comment="",name="Olympic Hernandez Market",)
	Place.create(category=tapvendors,lon=-118.216039,lat=34.139128,address="2272 Colorado Blvd.",city="Los Angeles",phone="3232566458",comment="",name="One Stop Services",)
	Place.create(category=tapvendors,lon=-117.826212,lat=34.615121,address="40340 170th Street E #2",city="Lake Los Angeles",phone="6612644536",comment="No EZ Passes",name="OSO Market",)
	Place.create(category=tapvendors,lon=-118.237235,lat=34.026953,address="1920 E. Olympic Blvd",city="Los Angeles",phone="2136140018",comment="No EZ Passes",name="OT Liquor",)
	Place.create(category=tapvendors,lon=-118.272823,lat=34.082513,address="2856 Sunset Blvd.",city="Los Angeles",phone="3236637347",comment="",name="P & M Market",)
	Place.create(category=tapvendors,lon=-118.119188,lat=34.145962,address="1580 E. Colorado Blvd.",city="Pasadena",phone="6265857123",comment="",name="Pasadena City College",)
	Place.create(category=tapvendors,lon=-118.013948,lat=34.091841,address="4840 Peck Rd.",city="El Monte",phone=" ",comment="",name="Payless Foods",)
	Place.create(category=tapvendors,lon=-118.263150,lat=34.059068,address="1451 W. 3rd St.",city="Los Angeles",phone="2134821791",comment="",name="Phil's Discount Store",)
	Place.create(category=tapvendors,lon=-118.256859,lat=34.004094,address="4373 S. Central Ave.",city="Los Angeles",phone="3232355895",comment="",name="Phoenix Check Cashing",)
	Place.create(category=tapvendors,lon=-118.292163,lat=34.039774,address="1614 W. Washington",city="Los Angeles",phone="3237354327",comment="",name="Plaza Check Cashing",)
	Place.create(category=tapvendors,lon=-118.276307,lat=34.044591,address="1545 W Pico Blvd",city="Los Angeles",phone="2133880773",comment="No EZ Passes",name="PLS Check Cashers",)
	Place.create(category=tapvendors,lon=-87.616481,lat=41.675380,address="15039 South Prairie Ave.",city="Hawthorne",phone="3102191028",comment="No EZ Passes",name="PLS Check Cashers",)
	Place.create(category=tapvendors,lon=-118.351570,lat=34.032248,address="2601 S. La Brea Avenue",city="Los Angeles",phone="3239365853",comment="No EZ Passes",name="Pls Check Cashers",)
	Place.create(category=tapvendors,lon=-118.284605,lat=34.043512,address="1605 S. Hoover St.",city="Los Angeles",phone="2137452800",comment="No EZ Passes",name="PLS Check Cashers",)
	Place.create(category=tapvendors,lon=-118.216470,lat=34.034238,address="2324 Whittier Blvd.",city="Los Angeles",phone="3232698000",comment="No EZ Passes",name="PLS Check Cashers",)
	Place.create(category=tapvendors,lon=-118.352500,lat=33.944995,address="10048 S. Hawthorne Blvd.",city="Inglewood",phone="3104120610",comment="No EZ Passes",name="PLS Check Cashers",)
	Place.create(category=tapvendors,lon=-118.447552,lat=34.247114,address="9714 Woodman Ave.",city="Arleta",phone="8188996900",comment="No EZ Passes",name="PLS Check Cashers of CA",)
	Place.create(category=tapvendors,lon=-118.184422,lat=34.040927,address="3805 E. Cesar Chavez Ave.",city="Los Angeles",phone="2134793461",comment="No EZ Passes",name="PLS Check Cashers Of CA",)
	Place.create(category=tapvendors,lon=-118.193942,lat=33.903973,address="13022 S. Atlantic Ave",city="Compton",phone="3106085400",comment="No EZ Passes",name="PLS Check Cashiers",)
	Place.create(category=tapvendors,lon=-118.308486,lat=34.044046,address="1570 S Western 110",city="Los Angeles",phone="3236430598",comment="No EZ Passes",name="PLS Check Cashiers",)
	Place.create(category=tapvendors,lon=-118.209762,lat=33.972867,address="3217 E. Florence Ave.",city="Huntington Park",phone="3232773919",comment="No EZ Passes",name="PLS Check Cashers",)
	Place.create(category=tapvendors,lon=-118.211151,lat=33.928148,address="11301 Long Beach Blvd",city="Lynwod",phone="3106055300",comment="No EZ Passes",name="PLS CheckCashers",)
	Place.create(category=tapvendors,lon=-118.251369,lat=34.048633,address="325 W. 5Th Street",city="Los Angeles",phone="2136236515",comment="",name="Power Discount Store",)
	Place.create(category=tapvendors,lon=-118.209089,lat=33.936373,address="3448 Martin Luther King Jr Blvd.",city="Lynwood",phone="3106318653",comment="No EZ Passes",name="Quick Cash",)
	Place.create(category=tapvendors,lon=-118.446991,lat=34.186679,address="14411 Victory Blvd.",city="Van Nuys",phone="8187818489",comment="",name="Quick Stop Liquor",)
	Place.create(category=tapvendors,lon=-118.300753,lat=34.101530,address="5102 Hollywood Boulevrd",city="Los Angeles",phone="3236628993",comment="",name="Quick Stop Liquor",)
	Place.create(category=tapvendors,lon=-118.192500,lat=33.978620,address="4137 E. Gage Ave.",city="Bell",phone="3235622244",comment="No EZ Passes",name="Quik Check",)
	Place.create(category=tapvendors,lon=-118.265519,lat=34.004215,address="525 East Vernon Avenue",city="Los Angeles",phone="3232352594",comment="No EZ Passes",name="Quik Check",)
	Place.create(category=tapvendors,lon=-118.326725,lat=34.260476,address="10455 Sunland Blvd.",city="Sunland",phone="8183524544",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.391726,lat=33.863980,address="1100 Pacific Coast Highway",city="Hermosa Beach",phone="3107986800",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.414440,lat=34.165597,address="12921 Magnolia Blvd",city="Sherman Oaks",phone="8189862293",comment="No EZ Passes",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.501532,lat=34.256727,address="16940 Devonshire St.",city="Granada Hills",phone="8183633173",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.308244,lat=34.101970,address="5429 Hollywood Blvd",city="Los Angeles",phone="3239579657",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.340408,lat=33.789445,address="2909 Rolling Hills Rd.",city="Torrance",phone="3103250611",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.439202,lat=33.979880,address="4700 Admiralty Way",city="Marina Del Rey",phone="3108234684",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.233046,lat=34.142619,address="1416 E Colorado Blvd",city="Glendale",phone="8185480945",comment="No EZ Passes",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.264690,lat=33.830425,address="650 E. Carson St.",city="Carson",phone="3105184191",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.344090,lat=34.093147,address="1233 N La Brea Ave",city="Los Angeles",phone="3238768790",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.443723,lat=34.063483,address="10861 Le Conte Avenue",city="Los Angeles",phone="3108245994",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.260760,lat=34.046251,address="645 W. 9Th Street",city="Los Angeles",phone="2134520840",comment="None ",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.394653,lat=33.760508,address="30019 Hawthorne Blvd.",city="Palos Verdes",phone="3103776941",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.447290,lat=34.171473,address="14440 Burbank Blvd",city="Van Nuys",phone="8189895640",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.354042,lat=33.925971,address="11873 Hawthorne Blvd",city="Hawthorne",phone="3106799164",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.307660,lat=33.753322,address="1050 N. Western",city="San Pedro",phone="3108333506",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.432057,lat=34.202002,address="7221 Woodman Blvd",city="Van Nuys",phone="8187853162",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.524266,lat=34.045051,address="15120 W. Sunset Blvd",city="Pacific Palisades",phone="3104543001",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.144856,lat=34.037110,address="2230 Atlantic Blvd.",city="Monterey Park",phone="3237213785",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.397869,lat=34.055023,address="9616 W. Pico blvd",city="Los Angeles",phone="3102712672",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.329760,lat=33.987533,address="3300 W. Slauson Ave",city="Los Angeles",phone="3232930171",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.354791,lat=34.020315,address="5080 Rodeo Rd.",city="Los Angeles",phone="3232920633",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.290334,lat=34.068517,address="3410 W. Third Street",city="Los Angeles",phone="2134801421",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.357075,lat=33.975331,address="950 N. La Brea Ave.",city="Inglewood",phone="3106736365",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.128599,lat=33.937741,address="8625 Firestone Blvd.",city="Downey",phone="5628692733",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.343620,lat=34.070014,address="260 S. La Brea Avenue",city="Los Angeles",phone="3239373264",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.130945,lat=34.185084,address="2270 Lake Ave",city="Altadena",phone="6267941175",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.367925,lat=34.164501,address="10900 Magnolia Blvd.",city="North Hollywood",phone="8187604148",comment="No EZ Passes",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.395544,lat=33.922295,address="500 N. Sepulveda Blvd",city="El Segundo",phone="3106150537",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.308551,lat=34.060111,address="670 S. Western Avenue",city="Los Angeles",phone="2133835058",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.397731,lat=34.222518,address="8325 Laurel Canyon Blvd",city="Sun Valley",phone="8187680378",comment="No EZ Passes",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.473608,lat=34.027151,address="1644 Cloverfield Blvd.",city="Santa Monica",phone="3105823900",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.307962,lat=33.959340,address="1730 W. Manchester Ave",city="Los Angeles",phone="3237503151",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.301976,lat=34.173113,address="25 E Alameda",city="Burbank",phone="8185561558",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.466905,lat=34.044853,address="12057 Wilshire Blvd",city="Los Angeles",phone="3104778746",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.449287,lat=34.034793,address="11727 West Olympic Blvd",city="Los Angeles",phone="3104735238",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.443342,lat=33.984228,address="4311 Lincoln Blvd.",city="Marina Del Rey",phone="3105740909",comment="No EZ Passes",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.290768,lat=34.031695,address="2600 S. Vermont Ave",city="Los Angeles",phone="3237323863",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.351039,lat=34.062894,address="5601 Wilshire Blvd.",city="Los Angeles",phone="3239364954",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.165125,lat=33.830982,address="2250 E. Carson St.",city="Long Beach",phone="5624242012",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.258559,lat=34.103045,address="2520 Glendale Blvd.",city="Los Angeles",phone="3236665392",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.508951,lat=34.207008,address="17250 Saticoy Street",city="Van Nuys",phone="8186098425",comment="",name="Ralphs",)
	Place.create(category=tapvendors,lon=-118.278357,lat=34.066527,address="264 S. Rampart",city="Los Angeles",phone="2133866478",comment="",name="Rampart Check Cashing",)
	Place.create(category=tapvendors,lon=-118.386797,lat=33.828621,address="320 Knob Hill Ave.",city="Redondo Beach",phone="3103180650",comment="No EZ Passes",name="Redondo Beach Senior",)
	Place.create(category=tapvendors,lon=-118.377326,lat=33.872515,address="1922 Artesia Blvd",city="Redondo Beach",phone="NULL",comment="",name="Redondo Beach Senior Family",)
	Place.create(category=tapvendors,lon=-118.247439,lat=34.052151,address="213 S. Broadway",city="Los Angeles",phone="2136804053",comment="",name="Redwood Shop",)
	Place.create(category=tapvendors,lon=-118.326320,lat=34.084734,address="748 N. Vine St.",city="Los Angeles",phone="3234671777",comment="",name="Rose-Vine Exchange",)
	Place.create(category=tapvendors,lon=-118.407366,lat=34.068492,address="471 S. Roxbury Dr.",city="Beverly Hills",phone="3102856840",comment="No EZ Passes",name="Roxbury Community Center",)
	Place.create(category=tapvendors,lon=-118.253702,lat=34.047519,address="410-A W. 6th St.",city="Los Angeles",phone="2133275121",comment="",name="Royal Deli and Market",)
	Place.create(category=tapvendors,lon=-118.492236,lat=34.154005,address="16550 Ventura Blvd/Lobby",city="Encino",phone="8189905100",comment="",name="Rubio Drug",)
	Place.create(category=tapvendors,lon=-118.273732,lat=34.059268,address="2001 W. 6th Street",city="Los Angeles",phone="2134838753",comment="",name="Sams Corner Liquor",)
	Place.create(category=tapvendors,lon=-118.270810,lat=34.025823,address="201 W. Adams Blvd",city="Los Angeles",phone="2137468951",comment="",name="San Pedro Check Cashing",)
	Place.create(category=tapvendors,lon=-118.553087,lat=34.208028,address="7550 Tampa Ave. #D",city="Reseda",phone="8187741045",comment="",name="Sandhya Enterprises",)
	Place.create(category=tapvendors,lon=-118.510821,lat=34.443151,address="27641 Bouquet Canyon Road",city="Santa Clarita",phone="6612963980",comment="No EZ Passes",name="Sangus Drugs and Hallmark",)
	Place.create(category=tapvendors,lon=-118.251532,lat=34.041221,address="305 E. 8Th St",city="Los Angeles",phone="2136893199",comment="",name="Santee Market",)
	Place.create(category=tapvendors,lon=-118.309248,lat=34.071046,address="201 S. Western Ave.",city="Los Angeles",phone="2133861771",comment="No EZ Passes",name="Sav-On Variety Store",)
	Place.create(category=tapvendors,lon=-118.284053,lat=34.057818,address="2633 W. 8th St.",city="Los Angeles",phone="2133841433",comment="No EZ Passes",name="Sav-On Variety Store",)
	Place.create(category=tapvendors,lon=-118.087753,lat=33.990225,address="9200 Mines Ave.",city="Pico Rivera",phone="5629484844",comment="No EZ Passes",name="Senior Center Pico Rivera",)
	Place.create(category=tapvendors,lon=-117.889399,lat=34.087701,address="125 E. College St.",city="Covina",phone="",comment="",name="Senior Center Joslyn Covina",)
	Place.create(category=tapvendors,lon=-118.468143,lat=34.232270,address="8925 Sepulveda Boulevard-#3",city="North Hills",phone="8188300250",comment="",name="Sepulveda Check Cashing",)
	Place.create(category=tapvendors,lon=-118.517880,lat=34.200653,address="16048 1/2 Sherman Way",city="Van Nuys",phone="8183761211",comment="No EZ Passes",name="Sherman Way Check Cashing",)
	Place.create(category=tapvendors,lon=-118.451115,lat=34.243102,address="9501 Van Nuys Blvd",city="Panorama City",phone="8188301394",comment="",name="Short Stop",)
	Place.create(category=tapvendors,lon=-118.467493,lat=34.235512,address="15400 Nordhoff St.",city="North Hills",phone="8188920640",comment="Seniors Only",name="Short Stop",)
	Place.create(category=tapvendors,lon=-118.449060,lat=34.215047,address="7929 Van Nuys Blvd",city="Panorama City",phone="8189029729",comment="No EZ Passes",name="Short Stop",)
	Place.create(category=tapvendors,lon=-118.466842,lat=34.193936,address="15317 Vanowen St.",city="Van Nuys",phone="8189943631",comment="",name="Short Stop 21",)
	Place.create(category=tapvendors,lon=-118.449092,lat=34.180944,address="6073 Van Nuys Blvd.",city="Van Nuys",phone="8189040677",comment="",name="Short Stop 28",)
	Place.create(category=tapvendors,lon=-118.432186,lat=34.259189,address="10402 Laurel Canyon Blvd.",city="Pacoima",phone="8188903951",comment="",name="Short Stop 29",)
	Place.create(category=tapvendors,lon=-118.057840,lat=34.161598,address="232 W. Sierra Madre Blvd.",city="Sierra Madre",phone="6263557135",comment="No EZ Passes",name="Sierra Madre City Hall",)
	Place.create(category=tapvendors,lon=-118.291645,lat=34.052126,address="1003 S. Vermont Ave.",city="Los Angeles",phone="7147026857",comment="",name="Smoky Tango",)
	Place.create(category=tapvendors,lon=-118.249683,lat=34.042762,address="239 E. 7th Street",city="Los Angeles",phone="2136147918",comment="No EZ Passes",name="Speedy Check Cashing",)
	Place.create(category=tapvendors,lon=-118.349625,lat=34.184536,address="3510 W. Victory Boulevard",city="Burbank",phone="8188464010 ",comment="No EZ  Passes",name="Starlite Liquor",)
	Place.create(category=tapvendors,lon=-118.258942,lat=33.833153,address="1 Civic Plaza Dr. #625",city="Carson",phone="3237285800",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-118.158100,lat=34.020333,address="5166 E. Whittier Blvd.",city="Los Angeles",phone="3232662188",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-118.187246,lat=34.036182,address="3657 E. 1St St.",city="Los Angeles",phone="3239809886",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-118.126986,lat=34.014312,address="2400 W. Whittier Blvd.",city="Montebello",phone="3137266740",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-118.163610,lat=34.021589,address="4840 E. Whittier Blvd.",city="Los Angeles",phone="3108472990",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-118.131101,lat=34.011901,address="6571 E Olympic Blvd",city="Los Angeles",phone="3232789922",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-118.219542,lat=34.026923,address="1260 S. Soto #19",city="Los Angeles",phone="3239800511",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-118.069738,lat=33.964621,address="11522 Slauson Ave.",city="Whittier",phone="5624639213",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-117.974090,lat=34.034148,address="14632 E. Valley Blvd. #A",city="La Puente",phone="3108472990",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-118.225599,lat=33.983528,address="2576 clarendon Ave.",city="Huntington Park",phone="3235825467",comment="",name="Su Casa de Cambio",)
	Place.create(category=tapvendors,lon=-118.210687,lat=34.047937,address="2132 E. Cesar Chavez Ave",city="Los Angeles",phone="3232623240",comment="",name="Su Casa De Cambio",)
	Place.create(category=tapvendors,lon=-118.097493,lat=33.969055,address="9335 Slauson Ave.",city="Pico Rivera",phone="5628210215",comment="",name="Su Casa de Cambio",)
	Place.create(category=tapvendors,lon=-118.291096,lat=33.973849,address="7224 S. Vermont Ave.",city="Los Angeles",phone="3237525633",comment="",name="Super Buy",)
	Place.create(category=tapvendors,lon=-118.442609,lat=34.283453,address="1126 San Fernando Rd.",city="San Fernando",phone="8183653146",comment="",name="Super Dollar",)
	Place.create(category=tapvendors,lon=-118.162456,lat=34.044024,address="625 N. Mednik Ave.",city="Los Angeles",phone="3232687934",comment="No EZ Passes",name="Super Salud Liquor & Market",)
	Place.create(category=tapvendors,lon=-118.289608,lat=33.881533,address="814 W. Gardena Blvd.",city="Gardena",phone="3103234708",comment="No EZ Passes",name="TDT Community Market",)
	Place.create(category=tapvendors,lon=-118.254600,lat=34.043342,address="806 S Broadway",city="Los Angeles",phone="2136276270",comment="No EZ Passes",name="Top Town",)
	Place.create(category=tapvendors,lon=-118.353289,lat=33.937533,address="10819 S. Hawthorne Blvd..",city="Inglewood",phone="3106717988",comment="",name="Top Valu Market",)
	Place.create(category=tapvendors,lon=-118.606299,lat=34.202238,address="7239 Topanga Canyon blvd.",city="Canoga Park",phone="8185940057",comment="",name="Topanga Check Cashing",)
	Place.create(category=tapvendors,lon=-118.341254,lat=33.837087,address="3031 Torrance Blvd.",city="Torrance",phone="3106182536",comment="",name="Torrance Transit System",)
	Place.create(category=tapvendors,lon=-118.273900,lat=33.964348,address="59465948 S. Main St.",city="Los Angeles",phone="3232325035",comment="No EZ Passes",name="Town Deli & Liquor",)
	Place.create(category=tapvendors,lon=-118.261200,lat=34.039057,address="1139 S. Hill St.",city="Los Angeles",phone="2137426774",comment="",name="Trimana",)
	Place.create(category=tapvendors,lon=-118.445210,lat=34.073634,address="325 Westwood Plaza",city="Los Angeles",phone="3108252101",comment="",name="UCLA Central Ticket Office",)
	Place.create(category=tapvendors,lon=-118.134861,lat=34.683786,address="44055 Sierra Highway",city="Lancaster",phone="6617261911",comment="No EZ Passes",name="University of Antelope Valley",)
	Place.create(category=tapvendors,lon=-118.115592,lat=34.579762,address="803 E. Palmdale Blvd.",city="Palmdale",phone="6612740762",comment="No EZ Passes",name="US Postal Exchange",)
	Place.create(category=tapvendors,lon=-118.549801,lat=34.416137,address="23743 Valencia Blvd",city="Santa Clarita",phone="6612598942",comment="No EZ Passes",name="Valencia Library",)
	Place.create(category=tapvendors,lon=-118.431277,lat=34.194107,address="6803 Woodman Ave",city="Van Nuys",phone="8183741371",comment="",name="Vanowen Check Cashing",)
	Place.create(category=tapvendors,lon=-118.167833,lat=33.782380,address="1942 E Anaheim St.",city="Long Beach",phone="5625910549",comment="",name="Vermillion's Drug #3",)
	Place.create(category=tapvendors,lon=-118.219788,lat=34.007066,address="3843 S. Soto St.",city="Vernon",phone="3235887776",comment="",name="Vernon & Soto",)
	Place.create(category=tapvendors,lon=-118.230441,lat=33.989675,address="5825 S. Santa Fe Ave.",city="Vernon",phone="3235889991",comment="",name="Vernon Quick Check",)
	Place.create(category=tapvendors,lon=-118.369987,lat=34.179912,address="6012 Vineland Avenue",city="North Hollywood",phone="8187632234",comment="No EZ Passes",name="Vineland Wine Cellar",)
	Place.create(category=tapvendors,lon=-118.288074,lat=34.097097,address="4520 Sunset Blvd.",city="Los Angeles",phone="3236628107",comment="",name="Vons",)
	Place.create(category=tapvendors,lon=-118.396122,lat=34.144572,address="4033 Laurel Canyon Blvd.",city="Studio City",phone="8189855401",comment="",name="Vons",)
	Place.create(category=tapvendors,lon=-118.456663,lat=34.153324,address="14845 Ventura Blvd.",city="Sherman Oaks",phone="8189867213",comment="",name="Vons",)
	Place.create(category=tapvendors,lon=-118.489853,lat=34.026444,address="1311 Wilshire Blvd.",city="Santa Monica",phone="3103941414",comment="",name="Vons",)
	Place.create(category=tapvendors,lon=-118.399889,lat=34.059688,address="9476 W Olympic Blvd.",city="Beverly Hills",phone="3105535734 ",comment="",name="Vons",)
	Place.create(category=tapvendors,lon=-118.386897,lat=34.083292,address="8969 Santa Monica Blvd.",city="West Hollywood",phone="3105951730",comment="",name="Vons",)
	Place.create(category=tapvendors,lon=-118.327077,lat=34.084427,address="727 N Vine St",city="Los Angeles",phone="3234614167",comment="",name="Vons",)
	Place.create(category=tapvendors,lon=-118.202392,lat=34.661499,address="4033 West Ave L",city="Lancaster",phone="6617227291",comment="",name="Vons",)
	Place.create(category=tapvendors,lon=-118.184244,lat=34.603411,address="3027 Rancho Vista Blvd",city="Palmdale",phone="6612659285",comment="",name="Vons",)
	Place.create(category=tapvendors,lon=-118.557054,lat=34.377497,address="24160 Lyons Ave",city="Santa Clarita",phone="6612599214",comment="No Stored Value",name="Vons",)
	Place.create(category=tapvendors,lon=-118.258562,lat=34.026295,address="1955 S. San Pedro St.",city="Los Angeles",phone="2137465666",comment="No EZ Passes",name="Wally's Liquor Market",)
	Place.create(category=tapvendors,lon=-118.111837,lat=34.579930,address="38416 10th St. E. ",city="Palmdale ",phone="6612659900",comment="No EZ Passes",name="Ware Networking",)
	Place.create(category=tapvendors,lon=-118.369536,lat=34.090464,address="8272 Santa Monica Blvd.",city="West Hollywood",phone="3236502688",comment="No EZ Passes",name="West Hollywood Chamber of Commerce ",)
	Place.create(category=tapvendors,lon=-118.147979,lat=34.687749,address="44248 10th Street West",city="Lancaster",phone="6614180153",comment="No EZ Passes",name="Westside Biz & Mail Stop",)
	Place.create(category=tapvendors,lon=-118.184652,lat=34.024124,address="4045 Whittier Blvd.",city="Los Angeles",phone="3232684869",comment="No EZ Passes",name="Whittier Market",)
	Place.create(category=tapvendors,lon=-85.893207,lat=37.474611,address="13225 Walnut St.",city="Whittier",phone="5626982131",comment="",name="Whittier Senior Center",)
	Place.create(category=tapvendors,lon=-118.588183,lat=34.201358,address="20851 Sherman Way",city="Canoga Park",phone="8185920516",comment="",name="Winnetka Check Cashing",)



@manager.command
def add_admin(email, password):
	"""Add an admin user to your database_string"""

	# set up the admin role if necessary
	try:
		admin_role = Role.create(name="admin",description="Admin role")
	except:
		admin_role = Role.get(name="admin")

	user = user_datastore.create_user(email=email,
		password=encrypt_password(password),)

	# admin_role = user_datastore.find_or_create_role("admin")
	user_datastore.add_role_to_user(user, admin_role)
	user.confirmed_at = datetime.datetime.now()
	user.save()

	print "Created admin user: %s" % (user, )


# @manager.command
# def init(name, test=False, indent=""):
# 	"""Initialize and rename a flask-metroplaces project"""
#
# 	print "{0}Initializing flask-metroplaces project with name '{1}'".format(
# 		indent, name)
#
# 	module_name = "_".join(name.split()).lower()
# 	print "{0}Python main module will be: {1}".format(indent, module_name)
#
# 	module_files = ["manage.py", "dev.py", "shell.py", "metroplaces/config.py"]
#
# 	for filename in module_files:
# 		print "{0}Updating module name in '{1}'".format(indent, filename)
#
# 		if not test:
# 			with open(filename) as f:
# 				lines = [l.replace("metroplaces", module_name) for l in f.readlines()]
#
# 			with open(filename, 'w') as f:
# 				f.writelines(lines)
#
# 	print '{0}Generating salts and secret keys'.format(indent)
# 	with open("metroplaces/config.py") as f:
# 		lines = f.readlines()
#
# 	if not test:
# 		with open("metroplaces/config.py", "w") as f:
# 			for line in lines:
# 				if "REPLACE_WITH_RANDOM" in line:
# 					line = line.replace("REPLACE_WITH_RANDOM", bcrypt.gensalt())
#
# 				f.write(line)
#
# 	print "{0}Renaming 'metroplaces' module to '{1}'".format(indent, module_name)
# 	if not test:
# 		os.rename("metroplaces", module_name)
#
# 	print "{0}Finished initializing project".format(indent)


# @manager.command
# def wizard(test=False):
# 	"""New project wizard to go through all required startup steps"""
# 	print 'Starting the flask-metroplaces wizard'
#
# 	indent = ' ' * 4
#
# 	default_name = "metroplaces"
# 	print '\n\nProject name:'
# 	name = raw_input("> Please enter a name for your project [{0}]: ".format(
# 		default_name))
#
# 	name = name or default_name
# 	init(name, test=test, indent=indent)
#
# 	if test:
# 		name = default_name
#
# 	config_file = "{0}/config.py".format(name)
#
# 	lines = []
# 	database_string = ""
#
# 	with open(config_file) as f:
# 		for line in f:
# 			if line.strip().startswith("SQLALCHEMY_DATABASE_URI"):
# 				parts = line.split("=", 1)
# 				uri = parts[1].strip()
#
# 				print '\n\nDatabase configuration:'
# 				print '*** NB Please ensure your database has been created'
# 				print ('Database string must be a valid python expression that'
# 					' will be understood by SQLAlchemy. Please include '
# 					'surrounding quotes if this is just a static string')
#
# 				database_string = raw_input("> Please enter your database "
# 					"connection string [{0}]: ".format(uri))
#
# 				database_string = database_string or uri
#
# 				parts[1] = " {0}\n".format(database_string)
# 				parts.insert(1, "=")
# 				lines.append("".join(parts))
# 			else:
# 				lines.append(line)
#
# 	print "{0}Writing database connection string: {1}".format(indent,
# 		database_string)
#
# 	if not test:
# 		with open(config_file, "w") as f:
# 			f.writelines(lines)
#
# 	print "\n\nCreate admin user"
# 	email = raw_input("> Please enter an admin email address: ")
# 	password = raw_input("> Please enter an admin password: ")
# 	add_admin(email, password)


class UserAdmin(ModelView):
	# Visible columns in the list view
	column_exclude_list = ['password']

class PlaceAdmin(ModelView):
	# Visible columns in the list view
	foreign_key_lookups = {
		'feature': 'name',
		'category': 'name',
	}
	column_searchable_list = ( Place.name, Place.city )
	# place_category = relationship("w_accounts", backref=db.backref('categories', lazy='dynamic'))
	# column_select_related_list = ('place_category',)


admin = Admin(app, name='Metro Places')
admin.add_view(UserAdmin(User))
admin.add_view(ModelView(Role))
admin.add_view(ModelView(UserRoles))
admin.add_view(PlaceAdmin(Place))
admin.add_view(ModelView(Feature))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(PlaceFeatures))
# admin.add_view(ModelView(Tag))
# admin.add_view(ModelView(TagRelationship))


if __name__ == "__main__":
	import logging
	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)

	User.create_table(fail_silently=True)
	Role.create_table(fail_silently=True)
	UserRoles.create_table(fail_silently=True)
	Place.create_table(fail_silently=True)
	Category.create_table(fail_silently=True)
	Feature.create_table(fail_silently=True)
	PlaceFeatures.create_table(fail_silently=True)
	# Tag.create_table(fail_silently=True)
	# TagRelationship.create_table(fail_silently=True)

	# install some data
	# why does this fail?
	# load_data()

	# app.run()
	manager.run()



