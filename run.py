import os
import aio_pika
from dotenv import load_dotenv
import uvicorn
import asyncio
from fastapi import FastAPI

# Carregar as variáveis do arquivo .env
load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

app = FastAPI()

# Função de callback para processar a mensagem de forma assíncrona
async def process_message(message: aio_pika.IncomingMessage):
    async with message.process():  # Confirmação de processamento (ACK automático)
        print(f" [x] Processing message: {message.body.decode()}")
        # Simular um processamento demorado
        await asyncio.sleep(1)
        print(f" [x] Finished processing message: {message.body.decode()}")
        
# Função que consome mensagens do RabbitMQ
async def consume_rabbitmq():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)

    async with connection:
        channel = await connection.channel()
        
        # Declaração das exchanges.
        ex_novos_locatarios = await channel.declare_exchange(name="fanout-novos-locatarios", type="fanout")
        ex_upgrades_plano = await channel.declare_exchange(name="fanout-upgrades-plano", type="fanout")
        ex_cancelamentos_assinatura = await channel.declare_exchange(name="fanout-cancelamentos-assinatura", type="fanout")
        
        # Declaração das queues.
        q_novos_locatarios = await channel.declare_queue(name="novos-locatarios",
                                                         durable=True,
                                                         exclusive=False,
                                                         auto_delete=False)
        q_upgrades_plano = await channel.declare_queue(name="upgrades-pano",
                                                       durable=True,
                                                       exclusive=False,
                                                       auto_delete=False)
        q_cancelamentos_assinatura = await channel.declare_queue(name="cancelamentos-assinatura",
                                                                 durable=True,
                                                                 exclusive=False,
                                                                 auto_delete=False)
        
        # Vincular filas as exchanges.
        await q_novos_locatarios.bind(ex_novos_locatarios, routing_key="")
        await q_upgrades_plano.bind(ex_upgrades_plano, routing_key="")
        await q_cancelamentos_assinatura.bind(ex_cancelamentos_assinatura, routing_key="")
        
        # Inicia consumo e processamento de mensagens.
        await q_novos_locatarios.consume(process_message)
        await q_upgrades_plano.consume(process_message)
        await q_cancelamentos_assinatura.consume(process_message)

        print(" [*] Waiting for messages. To exit press CTRL+C")

        # Bloqueio indefinido.
        await asyncio.Future()
        

async def start_fastapi():
    config = uvicorn.Config("app.main:app", host="0.0.0.0", port=8009, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    fastapi_task = asyncio.create_task(start_fastapi())
    rabbitmq_task = asyncio.create_task(consume_rabbitmq())
    await asyncio.gather(fastapi_task, rabbitmq_task)

if __name__ == "__main__":
    asyncio.run(main())
