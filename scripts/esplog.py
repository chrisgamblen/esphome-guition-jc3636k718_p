import asyncio, sys, time
from aioesphomeapi import APIClient, LogLevel

HOST = "voice-knob.local"   # your device hostname or IP
PORT = 6053
DURATION = int(sys.argv[1]) if len(sys.argv) > 1 else 15
FILTER = sys.argv[2] if len(sys.argv) > 2 else ""  # optional substring filter

async def main():
    cli = APIClient(HOST, PORT, None)  # no password, no encryption
    await cli.connect(login=True)
    info = await cli.device_info()
    print(f"# connected: {info.name}  esphome={info.esphome_version}  uptime-ok", flush=True)

    def on_log(msg):
        line = msg.message.decode("utf-8", "replace")
        if FILTER and FILTER.lower() not in line.lower():
            return
        print(line, flush=True)

    cli.subscribe_logs(on_log, log_level=LogLevel.LOG_LEVEL_DEBUG)
    await asyncio.sleep(DURATION)
    print(f"# done ({DURATION}s)", flush=True)

asyncio.run(main())
