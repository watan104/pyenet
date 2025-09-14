import enet

SHUTDOWN_MSG = b"SHUTDOWN"

def main():
    host = enet.Host(
        enet.Address(b"localhost", 17091),
        10,
        0,
        0,
        0
    )
    host.checksum = enet.ENET_CRC32

    connect_count = 0
    shutdown_received = False
    run = True

    def intercept_callback(address, data):
        if data == b"\xff\xff\xff\xffgetstatus\x00":
            host.socket.send(address, b"\xff\xff\xff\xffstatusResponse\n")

    host.intercept = intercept_callback

    print("Server started on 0.0.0.0:17091")

    while run:
        event = host.service(1000)
        if event.type == enet.EVENT_TYPE_CONNECT:
            print(f"{event.peer.address}: CONNECT")
            connect_count += 1

        elif event.type == enet.EVENT_TYPE_DISCONNECT:
            print(f"{event.peer.address}: DISCONNECT")
            connect_count -= 1
            if connect_count <= 0 and shutdown_received:
                run = False

        elif event.type == enet.EVENT_TYPE_RECEIVE:
            data = event.packet.data
            print(f"{event.peer.address}: IN: {data!r}")

            if event.peer.send(0, enet.Packet(data)) < 0:
                print(f"{event.peer.address}: Error sending echo packet!")
            else:
                print(f"{event.peer.address}: OUT: {data!r}")

            if data == SHUTDOWN_MSG:
                shutdown_received = True


if __name__ == "__main__":
    main()
