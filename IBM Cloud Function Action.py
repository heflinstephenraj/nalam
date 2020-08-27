def main(args):
    import requests
    import hmac, hashlib
    import base64
    import json
    from enum import Enum

    Gender = Enum('Gender', 'Male Female')

    SelectorStatus = Enum('SelectorStatus', 'Man Woman Boy Girl')

    class DiagnosisClient:
        'Client class for priaid diagnosis health service'       

    # <summary>
    # DiagnosisClient constructor
    # </summary>
    # <param name="username">api user username</param>
    # <param name="password">api user password</param>
    # <param name="authServiceUrl">priaid login url (https://authservice.priaid.ch/login)</param>
    # <param name="language">language</param>
    # <param name="healthServiceUrl">priaid healthservice url(https://healthservice.priaid.ch)</param>
        def __init__(self, username, password, authServiceUrl, language, healthServiceUrl):
            self._handleRequiredArguments(username, password, authServiceUrl, healthServiceUrl, language)

            self._language = language
            self._healthServiceUrl = healthServiceUrl
            self._token = self._loadToken(username, password, authServiceUrl)


        def _loadToken(self, username, password, url):
            rawHashString = hmac.new(bytes(password, encoding='utf-8'), url.encode('utf-8')).digest()
            computedHashString = base64.b64encode(rawHashString).decode()

            bearer_credentials = username + ':' + computedHashString
            postHeaders = {
                'Authorization': 'Bearer {}'.format(bearer_credentials)
        }
            responsePost = requests.post(url, headers=postHeaders)

            data = json.loads(responsePost.text)
            return data


        def _handleRequiredArguments(self, username, password, authUrl, healthUrl, language):
            if not username:
                raise ValueError("Argument missing: username")

            if not password:
                raise ValueError("Argument missing: password")

            if not authUrl:
                raise ValueError("Argument missing: authServiceUrl")

            if not healthUrl:
                raise ValueError("Argument missing: healthServiceUrl")

            if not language:
                raise ValueError("Argument missing: language")


        def _loadFromWebService(self, action):
            extraArgs = "token=" + self._token["Token"] + "&format=json&language=" + self._language
            if "?" not in action:
                action += "?" + extraArgs
            else:
                action += "&" + extraArgs

            url = self._healthServiceUrl + "/" + action
            response = requests.get(url)

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print ("----------------------------------")
                print ("HTTPError: " + e.response.text )
                print ("----------------------------------")
                raise

            try:
                dataJson = response.json()
            except ValueError:
                raise requests.exceptions.RequestException(response=response)

            data = json.loads(response.text)
            return data       

    
    # <summary>
    # Load all issues
    # </summary>
    # <returns>Returns list of all issues</returns>
        def loadIssues(self):
            return self._loadFromWebService("issues")

    # <summary>
    # Load detail informations about selected issue
    # </summary>
    # <param name="issueId"></param>
    # <returns>Returns detail informations about selected issue</returns>
        def loadIssueInfo(self, issueId):
            if isinstance( issueId, int ):
                issueId = str(issueId)
            action = "issues/{0}/info".format(issueId)
            return self._loadFromWebService(action)

    
    # <summary>
    # Load all symptoms
    # </summary>
    # <returns>Returns list of all symptoms</returns>
        def loadSymptoms(self):
            return self._loadFromWebService("symptoms")

    # <summary>
    # Load calculated list of potential issues for selected parameters
    # </summary>
    # <param name="selectedSymptoms">List of selected symptom ids</param>
    # <param name="gender">Selected person gender (Male, Female)</param>
    # <param name="yearOfBirth">Selected person year of born</param>
    # <returns>Returns calculated list of potential issues for selected parameters</returns>
        def loadDiagnosis(self, selectedSymptoms, gender, yearOfBirth):
            if not selectedSymptoms:
                raise ValueError("selectedSymptoms can not be empty")
        
            serializedSymptoms = json.dumps(selectedSymptoms)
            action = f"diagnosis?symptoms={serializedSymptoms}&gender={gender}&year_of_birth={yearOfBirth}"
            return self._loadFromWebService(action)    
    option = args.get("option", 0)
    issue = args.get("issue", "")
    symptoms1 = args.get("symptoms1", "")
    symptoms2 = args.get("symptoms2", "")
    symptoms3 = args.get("symptoms3", "")
    symptoms4 = args.get("symptoms4", "")
    symptoms5 = args.get("symptoms5", "")
    symptoms6 = args.get("symptoms6", "")
    d=DiagnosisClient(username=" ",password=" ",authServiceUrl=" ",language="en-gb",healthServiceUrl=" ") # Enter your api key 
    if int(option) == 0:
        issues_1 = d.loadIssues()
        if issue:
            for ism in issues_1:
                if issue.lower() == ism["Name"].lower():
                    issues = d.loadIssueInfo(
                        int(ism["ID"])
                    )
        else:
            issues ={"No":""}
    if int(option) == 2:
        symptoms = d.loadSymptoms()
        sym_id = []
        gen = args.get("gen","")
        yob = args.get("yob","")
        if symptoms1:
            for i in symptoms:
                if i["Name"].lower() == symptoms1.lower():
                    sym_id.append(i["ID"])
        if symptoms2:
            for i in symptoms:
                if i["Name"].lower() == symptoms2.lower():
                    sym_id.append(i["ID"])
        if symptoms3:
            for i in symptoms:
                if i["Name"].lower() == symptoms3.lower():
                    sym_id.append(i["ID"])
        if symptoms4:
            for i in symptoms:
                if i["Name"].lower() == symptoms4.lower():
                    sym_id.append(i["ID"])
        if symptoms5:
            for i in symptoms:
                if i["Name"].lower() == symptoms5.lower():
                    sym_id.append(i["ID"])
        if symptoms6:
            for i in symptoms:
                if i["Name"].lower() == symptoms6.lower():
                    sym_id.append(i["ID"])
                  
        do = d.loadDiagnosis(gender=gen,yearOfBirth=int(yob),selectedSymptoms=sym_id)
        if do:
            issues = {"Name":""}
            for i in range(len(do)):
                if len(do)-1 == i:
                    issues["Name"] = issues["Name"]+ do[i]["Issue"]["Name"] + " (Accuracy: " + str(do[i]["Issue"]["Accuracy"])[:4] +"% ) "
                elif len(do)-2==  i:
                    issues["Name"] = issues["Name"]+ do[i]["Issue"]["Name"] + " (Accuracy: " + str(do[i]["Issue"]["Accuracy"])[:4] +"% ) "+" and "
                else:
                    issues["Name"] = issues["Name"]+ do[i]["Issue"]["Name"] + " (Accuracy: " + str(do[i]["Issue"]["Accuracy"])[:4] +"% ) "+" , "
        else:
            issues = {"No":"" }
            
    return issues
