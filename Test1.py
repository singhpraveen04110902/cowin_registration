import requests
from pygame import mixer 
from datetime import datetime, timedelta
import time


age = 18
pincodes = ["273008","273001","273013","273012","273014","273016","273005","273002","273003","273004","273005","273006"]
num_days = 1

print_flag = 'Y'

print("Starting search for Covid vaccine slots!")

actual = datetime.today().strftime("%d-%m-%Y")
valid_date = datetime.strptime("29-05-2021","%d-%m-%Y")
found = 0
while found==0: 

    for pincode in pincodes:   
            actual = datetime.today().strftime("%d-%m-%Y")
            try:
                URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, actual)
                header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 
                time.sleep(3)
                print (f"Query at {datetime.today()} for {actual} with pincode={pincode}")
                result = requests.get(URL, headers=header)
                if result.ok:
                    response_json = result.json()
                    if response_json["centers"]:
                        if(print_flag.lower() =='y'):
                            for center in response_json["centers"]:
                                for session in center["sessions"]:
                                    if (session["min_age_limit"] == age and datetime.strptime(session["date"],"%d-%m-%Y") >= valid_date ):
                                        print ("\t\t",session["min_age_limit"],session["vaccine"],session["available_capacity_dose2"],session["date"])
                                        if (session["available_capacity_dose2"] > 2 and session["vaccine"] == "COVAXIN" ) :
                                            found = 1;
                                            exec(open("covid-vaccine-slot-booking.py").read())
                else:
                    print("No Response!")
            except requests.exceptions.ConnectionError:
               print ("Caught ConnectionError .. will try again")
