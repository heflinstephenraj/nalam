# Nalam
Nalam is a Healthcare Chatbot. It is developed to make a diagnosis and to get detailed information about the health problems.

Nalam is developed on IBM Watson Assistant, IBM Cloud Functions and ApiMedic.

Step 1: Provision your IBM Watson Assistant service and Upload the "Nalam-Skills.json" to your IBM Watson Assistant service's dialogue skill.

Step 2: Create your apimedic api from https://apimedic.com/

Step 3: Enter your api in "IBM Cloud Function Action.py" and upload the python file to your IBM Cloud Functions Actions.

Step 4: Enable web action for your IBM Cloud Function Action and copy the web action URL.

Step 5: Enter the web action URL in the webbooks of your IBM Watson Assistant.
