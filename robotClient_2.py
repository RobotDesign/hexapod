





def receive():
    while True:
         data = self.sock.recv(1024)
         if not data: sys.exit(0)
         print(data)

Thread(target=receive()).start()