import pika
from twilio.rest import Client


account_sid = 'sua_account_sid'
auth_token = 'seu_auth_token'
twilio_number = 'seu_numero_twilio'
receiver_number = 'numero_destinatario'

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='weather')

def callback(ch, method, properties, body):
    print("Recebido:", body)
    send_sms(body)

def send_sms(message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_number,
        to=receiver_number
    )
    print(f"Mensagem SMS enviada com SID: {message.sid}")

channel.basic_consume(queue='weather', on_message_callback=callback, auto_ack=True)

print("Aguardando mensagens...")
channel.start_consuming()
