from scraper import fetch_survey_numbers

if __name__ == "__main__":
    # Sample input
    district = "Adilabad|ఆదిలాబాద్"
    mandal = "Bela|బేల"
    village = "Bhedoda|బెదోడ"
    
    survey_numbers = fetch_survey_numbers(district, mandal, village)
    
    with open('sample_output.txt', 'w') as f:
        for survey_number in survey_numbers:
            f.write(survey_number + '\n')
