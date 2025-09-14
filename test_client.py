import enet
import random
import sys

# Seed
try:
    random.seed(sys.argv[1])
except IndexError:
    pass

SHUTDOWN_MSG = b"SHUTDOWN"
MSG_NUMBER = 10

# Create host (client)
host = enet.Host(None, 1, 0, 0, 0)
host.checksum = enet.ENET_CRC32

peer = host.connect(enet.Address(b"localhost", 17091), 1)

counter = 0
run = True

try:
    while run:
        event = host.service(1000)
        if event.type == enet.EVENT_TYPE_CONNECT:
            print(f"{event.peer.address}: CONNECT")
        elif event.type == enet.EVENT_TYPE_DISCONNECT:
            print(f"{event.peer.address}: DISCONNECT")
            run = False
            continue
        elif event.type == enet.EVENT_TYPE_RECEIVE:
            print(f"{event.peer.address}: IN: {event.packet.data!r}")
            continue

        msg = bytes([random.randint(0, 255) for _ in range(40)])
        peer.send(0, enet.Packet(msg))
        print(f"{peer.address}: OUT: {msg!r}")

        counter += 1
        if counter >= MSG_NUMBER:
            peer.send(0, enet.Packet(SHUTDOWN_MSG))
            host.service(100)
            peer.disconnect()
except KeyboardInterrupt:
    print("\nClient manually stopped.")

# --- Intercept ---
peer = host.connect(enet.Address(b"localhost", 17091), 1)
shutdown_scheduled = False
run = True

def receive_callback(address, data):
    global shutdown_scheduled
    if shutdown_scheduled:
        return
    if data == b"\xff\xff\xff\xffstatusResponse\n":
        shutdown_scheduled = True
    else:
        print(f"Unexpected data: {data!r}")
        assert False

host.intercept = receive_callback

try:
    while run:
        event = host.service(1000)
        if event.type == enet.EVENT_TYPE_CONNECT:
            print(f"{event.peer.address}: CONNECT")
            msg = bytes([random.randint(0, 255) for _ in range(40)])
            peer.send(0, enet.Packet(msg))

        elif event.type == enet.EVENT_TYPE_DISCONNECT:
            print(f"{event.peer.address}: DISCONNECT")
            run = False
            continue

        elif event.type == enet.EVENT_TYPE_RECEIVE:
            print(f"{event.peer.address}: IN: {event.packet.data!r}")
            continue

        if shutdown_scheduled:
            peer.send(0, enet.Packet(SHUTDOWN_MSG))
            host.service(100)
            peer.disconnect()
            continue

        host.socket.send(peer.address, b"\xff\xff\xff\xffgetstatus\x00")
except KeyboardInterrupt:
    print("\nClient manually stopped.")
