import requests
import csv

# Define the input and output CSV file paths
input_csv_file = 'input_data.csv'
output_csv_file = 'output_data.csv'

# Define the URL and headers
url = 'http://190.52.34.65/Notificaciones/Informacion/ConsultaPuco'
cookies = {
    'ASP.NET_SessionId': '2e4pwiujfnmvtxtaygfg31ep',
}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'es-419,es;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://190.52.34.65',
    'Referer': 'http://190.52.34.65/Notificaciones/Informacion/Puco',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# Create a function to make a request and return the response JSON
def make_request(dni):
    data = {
        'dni': dni,
    }
    response = requests.post(url, cookies=cookies, headers=headers, data=data, verify=False)
    return response.json()

# Create a list to store the responses
responses = []

# Read 'dni' values from the input CSV file and make requests
with open(input_csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dni = row['dni']
        response_json = make_request(dni)
        responses.append(response_json)

# Write the responses to the output CSV file
with open(output_csv_file, 'w', newline='') as csvfile:
    fieldnames = ['TipoDocumento', 'NroDocumento', 'ClaseDocumento', 'Nombre', 'FechaNacimiento', 'ObraSocial', 'Siglas']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for response_json in responses:
        if response_json['Estado'] == 'OK':
            items = response_json['Items'][0]
            writer.writerow({
                'TipoDocumento': items['TipoDocumento'],
                'NroDocumento': items['NroDocumento'],
                'ClaseDocumento': items['ClaseDocumento'],
                'Nombre': items['Nombre'],
                'FechaNacimiento': items['FechaNacimiento'],
                'ObraSocial': items['ObraSocial'],
                'Siglas': items['Siglas']
            })
        elif response_json['Estado'] == 'NotFound':
            writer.writerow({'TipoDocumento': 'No encontrado', 'NroDocumento': '', 'ClaseDocumento': '', 'Nombre': '', 'FechaNacimiento': '', 'ObraSocial': '', 'Siglas': ''})

print(f'Responses saved to {output_csv_file}')
