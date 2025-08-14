import json
import os
import boto3
import requests
from datetime import datetime, timezone

# --- Configuração Inicial ---
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
TABLE_NAME = os.environ.get('DYNAMO_TABLE_NAME', '')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_NAME)

# --- Constantes (Evita "Textos Mágicos") ---
PHOTO_GATO_IDIOTA = "https://bot-gatinho.s3.sa-east-1.amazonaws.com/gato+idiota.png"
PHOTO_FRIEND_CATS = "https://bot-gatinho.s3.sa-east-1.amazonaws.com/amizade.jpg"
PHOTO_FRIEND_USER = "https://bot-gatinho.s3.sa-east-1.amazonaws.com/amigos.jpg"

CALLBACK_FRIEND_CATS = 'friend_cats'
CALLBACK_FRIEND_USER = 'friend_user'


# --- Funções Auxiliares ---

def safe_post_request(url, payload):
    """Envia uma requisição POST de forma segura, tratando possíveis erros de conexão."""
    try:
        requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar requisição para o Telegram: {e}")

def send_message(chat_id, text, reply_markup=None):
    """Envia uma mensagem de texto com formatação MarkdownV2."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'MarkdownV2'}
    if reply_markup:
        payload['reply_markup'] = reply_markup
    safe_post_request(url, payload)

def send_photo(chat_id, photo_url):
    """Envia uma foto a partir de uma URL."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    payload = {'chat_id': chat_id, 'photo': photo_url}
    safe_post_request(url, payload)

def escape_markdown(text):
    """Escapa caracteres especiais para o MarkdownV2 do Telegram."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in text)

def get_insult_count(chat_id):
    """Busca e retorna a contagem de insultos para um usuário."""
    pk = f'USER#{chat_id}'
    response = table.query(
        KeyConditionExpression='PK = :pk AND begins_with(SK, :sk_prefix)',
        ExpressionAttributeValues={':pk': pk, ':sk_prefix': 'INSULT#'},
        Select='COUNT'
    )
    return response.get('Count', 0)


# --- Funções de Lógica de Negócio ---

def handle_insult(chat_id):
    """Salva um novo insulto e responde com a foto."""
    pk = f'USER#{chat_id}'
    sk = f'INSULT#{datetime.now(timezone.utc).isoformat()}'
    table.put_item(Item={'PK': pk, 'SK': sk})
    send_photo(chat_id, PHOTO_GATO_IDIOTA)

def handle_contagem(chat_id):
    """Verifica a contagem de insultos e envia a resposta correspondente."""
    count = get_insult_count(chat_id)
    if count == 0:
        reply_text = "Obrigado por não ter me chamado de idiota 😊"
    else:
        reply_text = f"Você me chamou de idiota *{count}* vezes 🙄"
    
    send_message(chat_id, escape_markdown(reply_text))

def handle_unknown_message(chat_id):
    """Responde a mensagens não reconhecidas com os botões de amizade."""
    keyboard = {
        'inline_keyboard': [[
            {'text': 'Friendship 🐈🐈', 'callback_data': CALLBACK_FRIEND_CATS},
            {'text': 'Friendship 🐈🐒', 'callback_data': CALLBACK_FRIEND_USER}
        ]]
    }
    send_message(chat_id, escape_markdown("Não te compreendo, mas podemos ser amigos."), reply_markup=keyboard)

def handle_callback_query(callback_query):
    """Trata os cliques nos botões."""
    callback_data = callback_query['data']
    chat_id = callback_query['message']['chat']['id']
    
    if callback_data == CALLBACK_FRIEND_CATS:
        send_photo(chat_id, PHOTO_FRIEND_CATS)
    elif callback_data == CALLBACK_FRIEND_USER:
        send_photo(chat_id, PHOTO_FRIEND_USER)


# --- Lógica Principal (Handler) ---

def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))
    
    if 'callback_query' in body:
        handle_callback_query(body['callback_query'])
    elif 'message' in body:
        message = body['message']
        chat_id = message['chat']['id']
        user_text = message.get('text', '').lower()

        if user_text == "gato idiota":
            handle_insult(chat_id)
        elif user_text == "/contagem":
            handle_contagem(chat_id)
        else:
            handle_unknown_message(chat_id)
            
    return {'statusCode': 200, 'body': 'Processed'}