import requests
import time
import pymongo

def fetch_data():
        client = pymongo.MongoClient(
            "mongodb+srv://tejas:tejas@pythonfinalprojectclust.jcjtq.azure.mongodb.net")
        db = client['covid']

        while True:
            r = requests.get(
                'https://disease.sh/v3/covid-19/countries?yesterday=true&sort=cases&allowNull=false')
            if(r.status_code == 200):
                data = r.json()
                for c in data:
                    db['countries'].insert_one(c)
                print('Data Uploaded')
                # uncomment below line in production to run the loop every 24 hours
                # for debugging purposes it's kept commented out
                time.sleep(24*60*60)
                exit()
            else:
                exit()
