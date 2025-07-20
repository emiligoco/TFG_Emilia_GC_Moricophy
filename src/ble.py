import asyncio
import json
from bleak import BleakClient, BleakScanner

#Adreces BLE
SERVICE_UUID = "6c8dfa24-87a0-41b4-a47c-f1674f1974c7"
CHAR_UUID_TX = "8053f0ba-2459-4622-9838-a4f5d2b55e61"
OUTPUT_FILE = "dades.json"

async def notification_handler(sender, data):
    try:
        payload = json.loads(data.decode())
        with open(OUTPUT_FILE, "w") as f:
            json.dump(payload, f)
        print("Dades rebudes i desades")
    except Exception as e:
        print("Error rebent dades BLE:", e)

async def main():
    print("Escanejant dispositius BLE...")
    devices = await BleakScanner.discover()
    addr = next(
        (d.address for d in devices if d.name and "ESP32-SensorsEmili" in d.name),
        None
    )
    if not addr:
        print("No s'ha trobat l'ESP32-SensorsEmili")
        return

    print(f"Connectant amb {addr}...")
    async with BleakClient(addr) as client:
        await client.start_notify(CHAR_UUID_TX, notification_handler)
        print("Connectat! Esperant dades...")
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
      asyncio.run(main())