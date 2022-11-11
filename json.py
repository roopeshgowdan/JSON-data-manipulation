import json 
import datetime as dt

#function to extract the required Visits data.
def getVisits(data):
    visitsOutput = {}

    visitsOutput['full_visitor_id'] = data['fullVisitorId']
    visitsOutput['visit_id'] = data['visitId']
    visitsOutput['visit_number'] = int(data['visitNumber'])
    visitsOutput['visit_start_time'] = getISOTimeStamp(float(data['visitStartTime']))
    visitsOutput['browser'] = data['device']['browser']
    visitsOutput['country'] = data['geoNetwork']['country']

    return visitsOutput

#function to extract the required hits data.
def getHits(data):
    hitsOutput = []
    hits = {}
    hitsSize = int(data['totals']['hits'])
    hitsData = data['hits']
    # Generating a Unique Key field which can be used relate visits and hits
    visits_identifier = int(data['fullVisitorId']) // int(data['visitId']) 

    for i in range(hitsSize):
        hits['hit_number'] = int(hitsData[i]['hitNumber'])
        hits['hit_type'] = hitsData[i]['type']
        hits['hit_timestamp'] = getISOTimeStamp(float(data['visitStartTime']) + (float(hitsData[i]['time']) // 1000))
        hits['page_path'] = hitsData[i]['page']['pagePath']
        hits['page_title'] = hitsData[i]['page']['pageTitle']
        hits['hostname'] = hitsData[i]['page']['hostname']
        hits['visits_identifier'] = visits_identifier

        hitsOutput.append(hits)
        hits = {}
        
    return hitsOutput

#function to create .json file with specified filename.
def jsonGenerator(fileName, jsonData): #function to create a .json file.
    with open(fileName + ".json", "w") as jsonFile:
        jsonFile.write(jsonData)

    print(fileName + ".json Created" )

#function to get ISO8601-format timestamp from epoch time.
def getISOTimeStamp(epochTime):
    return dt.datetime.utcfromtimestamp(epochTime).isoformat(sep = " ")

#function to create visits.json
def createVisitsJSON(data):
    visitsJSONout = []
    for i in range(len(data)):
        visitsJSONout.append(getVisits(data[i]))
    
    jsonObject = json.dumps(visitsJSONout, indent=4)
    jsonGenerator("visits", jsonObject)

#function to create hits.json 
def createHitsJSON(data):
    hitsJSONout = []
    for i in range(len(data)):
        hitsJSONout.extend(getHits(data[i]))
    
    jsonObject = json.dumps(hitsJSONout, indent=4)
    jsonGenerator("hits", jsonObject)
    
def main():
    gaData = []

    # Reading the input JSON file line by line
    with open("ga_sessions_20160801.json") as inputData:
        for line in inputData:
            try:
                gaData.append(json.loads(line.rstrip(';\n')))
            except ValueError:
                print ("Skipping invalid line {0}".format(repr(line)))

    createVisitsJSON(gaData)
    createHitsJSON(gaData)

if __name__ == "__main__":
    main()
