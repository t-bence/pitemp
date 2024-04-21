import asyncio
from typing import Tuple

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

def load_secrets() -> Tuple[str, str]:
    import json
    with open("/home/pi/pitemp/pitemp/.env") as f:
        secrets = json.load(f)
    return secrets["CONNECTION_STRING"], secrets["EVENT_HUB_NAME"]


def get_cpu_temp() -> float:
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
            return float(file.read().strip()) / 1000
    except:
        return 0.0


async def run():
    import time
    # load config from JSON not in git
    conn_str, event_hub_name = load_secrets()

    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(
        conn_str=conn_str, eventhub_name=event_hub_name
    )
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        timestamp = time.time()

        data = f"{timestamp},{get_cpu_temp()}"

        # Add events to the batch.
        event_data_batch.add(EventData(data))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        print("Data was successfully sent.")

asyncio.run(run())
