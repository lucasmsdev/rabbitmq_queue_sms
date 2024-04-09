import pika
import requests
from datetime import datetime


api_key = 'sua_chave_de_api'
cidade = 'Taubaté'
url = f'http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='weather')

def traduzir_condicao(condicao):
    traducoes = {
        'Thunderstorm': 'Tempestade',
        'Drizzle': 'Chuvisco',
        'Rain': 'Chuva',
        'Snow': 'Neve',
        'Mist': 'Nevoeiro',
        'Smoke': 'Fumaça',
        'Haze': 'Neblina',
        'Dust': 'Poeira',
        'Fog': 'Nevoeiro',
        'Sand': 'Areia',
        'Dust': 'Poeira',
        'Ash': 'Cinzas',
        'Squall': 'Borrasca',
        'Tornado': 'Tornado',
        'Clear': 'Céu limpo',
        'Clouds': 'Nuvens',
        'Few clouds': 'Poucas nuvens',
        'Scattered clouds': 'Nuvens dispersas',
        'Broken clouds': 'Nuvens quebradas',
        'Overcast clouds': 'Nublado',
    }
    return traducoes.get(condicao, condicao)

def send_weather_to_rabbitmq():
    response = requests.get(url)
    data = response.json()
    if 'weather' in data:
        descricao = data['weather'][0]['main']
        descricao_traduzida = traduzir_condicao(descricao)
        temperatura_kelvin = data['main']['temp']
        temperatura_celsius = temperatura_kelvin - 273.15  
        umidade = data['main']['humidity']
        chance_chuva = data.get('rain', {}).get('1h', 0)  
        message = f"Previsão do Tempo:\n\n" \
                  f"Dia: {datetime.now().strftime('%d/%m/%Y')}\n" \
                  f"Condição: {descricao_traduzida}\n" \
                  f"Temperatura: {temperatura_celsius:.2f} °C\n" \
                  f"Umidade: {umidade}%\n" \
                  f"Chance de Chuva: {chance_chuva}%"
        channel.basic_publish(exchange='', routing_key='weather', body=message)
        print("Previsão do tempo enviada para o RabbitMQ")

send_weather_to_rabbitmq()
