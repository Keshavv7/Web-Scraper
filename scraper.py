import requests
from bs4 import BeautifulSoup

def fetch_survey_numbers(district, mandal, village):
    url = "https://dharani.telangana.gov.in/knowLandStatus"
    mandal_api_url = "https://dharani.telangana.gov.in/getMandalFromDivisionCitizenPortal"
    village_api_url = "https://dharani.telangana.gov.in/getVillageFromMandalCitizenPortal"
    survey_api_url = "https://dharani.telangana.gov.in/getSurveyCitizen"
    
    # Create a session object
    with requests.Session() as session:
        # Fetch the webpage content
        response = session.get(url)
        if response.status_code != 200:
            print("Failed to retrieve the webpage")
            return
        
        # Parse the webpage content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract required data from the webpage based on the provided details
        district_select = soup.find('select', {'id': 'districtID'})
        
        # Extract survey numbers for the given district
        survey_numbers = []
        for option in district_select.find_all('option'):
            district_option = option.text.strip()
            if district_option == district:
                district_id = option['value']
                #print("Found district! ", district_option)
                #print("DistrictID: ", district_id)
                break
        
        # Fetch mandal options based on the selected district using GET request
        params_for_mandal = {
            'district': district_id
        }
        
        response_for_mandal = session.get(mandal_api_url, params=params_for_mandal)
        if response_for_mandal.status_code != 200:
            print("Failed to fetch mandal options")
            return
        
        mandal_select = BeautifulSoup(response_for_mandal.content, 'html.parser')
        
        # Extract village options based on the selected mandal
        for option in mandal_select.find_all('option'):
            mandal_option = option.text.strip()
            if mandal_option == mandal:
                mandal_id = option['value']
                #print("Found mandal! ", mandal_option)
                #print("MandalID: ", mandal_id)
                break
        
    # Create a new session object for fetching village options
    with requests.Session() as session:
        params_for_village = {
            'mandalId': mandal_id
        }
        
        response_for_village = session.get(village_api_url, params=params_for_village)
        
        if response_for_village.status_code != 200:
            print("Failed to fetch village options")
            return
        
        village_select = BeautifulSoup(response_for_village.content, 'html.parser')
        
        # Extract survey numbers for the given district, mandal, and village
        for option in village_select.find_all('option'):
            village_option = option.text.strip()
            if village_option == village:
                village_id = option['value']
                #print("Found village! ", village_option)
                #print("VillageID: ", village_id)
                break
        
    # Create a new session object for fetching survey numbers
    with requests.Session() as session:
        params_for_survey = {
            'villId': village_id,
            'flag': 'survey'
        }
        
        response_for_survey = session.get(survey_api_url, params=params_for_survey)
        if response_for_survey.status_code != 200:
            print("Failed to fetch survey numbers")
            return
        
        survey_select = BeautifulSoup(response_for_survey.content, 'html.parser')
        
        for option in survey_select.find_all('option'):
            survey_numbers.append(option.text)
        
        return survey_numbers[1:]  # As the first element is 'Please select'


