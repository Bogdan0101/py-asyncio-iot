import time
import asyncio
from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def main() -> None:
    service = IOTService()
    devices = [HueLightDevice(), SmartSpeakerDevice(), SmartToiletDevice(), ]
    devices_id = await (asyncio.gather(
        *(service.register_device(device) for device in devices))
    )
    wake_up_program = [
        Message(devices_id[0], MessageType.SWITCH_ON),
        Message(devices_id[1], MessageType.SWITCH_ON),
        Message(devices_id[1],
                MessageType.PLAY_SONG,
                "Rick Astley - Never Gonna Give You Up"),
    ]
    sleep_program = [
        Message(devices_id[0], MessageType.SWITCH_OFF),
        Message(devices_id[1], MessageType.SWITCH_OFF),
        Message(devices_id[2], MessageType.FLUSH),
        Message(devices_id[2], MessageType.CLEAN),
    ]
    await service.run_program(wake_up_program)
    await service.run_program(sleep_program)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
