import socket, sys

def main(port=sys.argv[1]):
    connection = connect(port)
    if connection:
        costs = connection.recv(4096)
        
        print costs
        connection.send('START')
        print connection.recv(4096)
        
    else:
        print 'Connection Failed'
    
    
def connect(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('67.202.15.69', int(port)))
    s.send('INIT brogrammers')
    s.recv(4096)
    s.send('RECD')
    return s
    

if __name__ == "__main__":
    main()