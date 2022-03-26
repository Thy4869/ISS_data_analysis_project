from flask import Flask
import xmltodict, logging, flask

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def appInfo():
    return 'Download the data to file with code curl localhost:<your port number>/download -X POST\n Then interact the function with code curl localhost:<your port number>/<option of the data user want to get>\nThe options of the datas are:\nposition/Epochs -- all Epochs in the position data\nposition/<Epoch name> -- all information about a specific Epoch in the positional data\nCountry/Countries -- all countries from the sighting data\nCountry/<Country name> -- all information about a specific Country in the sighting data\nCountry/<country_name>/Region/Regions -- all regions associated with a given Country in the sighting data\nCountry/<country_name>/Region/<region_name> -- all information about a specific Region in the sighting data\nCountry/<country_name>/Region/<region_name>/City/Cities -- all cities associated with a given Country and Region in the sighting data\nCountry/<country_name>/Region/<region_name>/City/<city_name> -- all information about a specific City in the sighting data\n'

@app.route('/download', methods = ['POST'])
def get_data():
    '''
    This function reads in and load the position data and sightings data from ISS.OEM_J2K_EPH.xml file and XMLsightingData_citiesUSA02.xml file and store the datas into two different variables for both files 
    '''
    global pos_data, sig_data
    try:
        with open('ISS.OEM_J2K_EPH.xml','r') as f:
            data =  xmltodict.parse(f.read())
        pos_data = data['ndm']['oem']['body']['segment']['data']['stateV\
ector']
    except FileNotFoundError as g:
        logging.error(g)
        return 'Error message: The ISS Positional data XML file is not found\n'

    try:
        with open('XMLsightingData_citiesINT02.xml','r') as f:
            data =  xmltodict.parse(f.read())
        sig_data = data['visible_passes']['visible_pass']
    except FileNotFoundError as g:
        logging.error(g)
        return 'Error message: The ISS Sighting data XML file is not found\n'
    return 'Download Completed\n'

@app.route('/position/<name>', methods = ['GET'])
def get_position(name):
    """
    This function reads in and load the position data from the download function from the ISS.OEM_J2K_EPH XML file. This function specificlly looks into Epoch data in the file and return all epochs or specific epoch data with user inputted  
    """
    position_data = {}
    j = 0;
    if (f'{name}' == 'Epochs'):
        for i in pos_data:
            position_data['EPOCH: ' + str(j)] = i.get('EPOCH')
            j = j + 1

    else:
        for i in pos_data:
            if i.get('EPOCH') == f'{name}':
                position_data = {'EPOCH': i.get('EPOCH'), 'X units(km)': i.get('X').get('#text'), 'Y units(km)': i.get('Y').get('#text'), 'Z units(km)': i.get('Z').get('#text'), 'X_DOT units(km/s)': i.get('X_DOT').get('#text'), 'Y_DOT units(km/s)': i.get('Y_DOT').get('#text'), 'Z_DOT units(km/s)': i.get('Z_DOT').get('#text')}

    return position_data


@app.route('/Country/<name>', methods = ['GET'])
def get_country(name):
    """
    This function reads in and load the sighting data from the download function from the XMLsightingData_citiesINT02 XML file. This function specificlly looks into countries data in the file and return all countries in the file or detail data in the specific country with return type of class dict
    """
    country_data = {}
    countries = []
    if (f'{name}' == 'Countries'):
        for i in sig_data:
            country = i.get('country')
            if len(countries) == 0:
                countries.append(country)
            else:
                counter = 0
                for j in countries:
                    different = (country == j)
                    if different == True:
                        counter = 1
                        break
                if counter == 0:
                    countries.append(country)
    else:
         for j in sig_data:
             if j.get('country') == f'{name}':
                 country = {"Region":(j.get('region')),"City":(j.get('city')),"Spacecraft":(j.get('spacecraft')),"Sighting Date":(j.get('sighting_date')),"Duration minutes":(j.get('duration_minutes')),"Maximum Elevation":(j.get('max_elevation')),"Enters":(j.get('enters')),"Exits":(j.get('exits')),"UTC Offset":(j.get('utc_offset')),"UTC Time":(j.get('utc_time')),"UTC Date":(j.get('utc_date'))}
                 countries.append(country)

    country_data = {'Countries': countries}

    return country_data

@app.route('/Country/<country_name>/Region/<region_name>', methods = ['GET'])
def get_region(country_name, region_name):
    """
    This function reads in and load the data of sighting data from the download function from the XMLsightingData_citiesINT02 XML file. This function accept inputs of country name and the region name to return all regions in a specific country or detail of a specific region in specific country
    """
    region_data = {}
    regions = []
    if (f'{region_name}' == 'Regions'):
        for i in sig_data:
            if i.get('country') == f'{country_name}':
                region = i.get('region')
                if len(regions) == 0:
                    regions.append(region)
                else:
                    counter = 0
                    for j in regions:
                        different = (region == j)
                        if different == True:
                            counter = 1
                            break
                    if counter == 0:
                        regions.append(region)
    else:
        for j in sig_data:
            if j.get('country') == f'{country_name}':
                if j.get('region') == f'{region_name}':
                    region = {"City":(j.get('city')),"Spacecraft":(j.get('spacecraft')),"Sighting Date":(j.get('sighting_date')),"Duration minutes":(j.get('duration_minutes')),"Maximum Elevation":(j.get('max_elevation')),"Enters":(j.get('enters')),"Exits":(j.get('exits')),"UTC Offset":(j.get('utc_offset')),"UTC Time":(j.get('utc_time')),"UTC Date":(j.get('utc_date'))}
                    regions.append(region)

    region_data = {'Regions': regions}

    return region_data

@app.route('/Country/<country_name>/Region/<region_name>/City/<city_name>', methods = ['GET'])
def get_city(country_name, region_name, city_name):
    """
    This function reads in and load the data of sighting data from the download function from the XMLsightingData_citiesINT02 XML file. This function accept inputs of country name, \ region name, and city name to return all citiess in a specific country of specific region or detail of a specific city in specific region in the country
    """
    city_data = {}
    cities = []
    if (f'{city_name}' == 'Cities'):
        for i in sig_data:
            if (i.get('country') == f'{country_name}') and (i.get('region') == f'{region_name}'):
                city = i.get('city')
                if len(cities) == 0:
                    cities.append(city)
                else:
                    counter = 0
                    for j in cities:
                        different = (city == j)
                        if different == True:
                            counter = 1
                            break
                    if counter == 0:
                        cities.append(city)
    else:
        for j in sig_data:
            if (j.get('country') == f'{country_name}') and (j.get('region') == f'{region_name}'):
                if j.get('city') == f'{city_name}':
                    city = {"Spacecraft":(j.get('spacecraft')),"Sighting Date":(j.get('sighting_date')),"Duration minutes":(j.get('duration_minutes')),"Maximum Ele\
vation":(j.get('max_elevation')),"Enters":(j.get('enters')),"Exits":(j.get('exits')),"UTC Offset":(j.get('utc_offset')),"UTC Time":(j.get('utc_time')),"UTC Date":(j.get('utc_date'))}
                    cities.append(city)

    city_data = {'Cities': cities}

    return city_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
