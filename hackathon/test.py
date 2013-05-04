import socket
from datetime import datetime

def connect(port):
    print 'we startin'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('67.202.15.69', int(port)))
    s.send('INIT brogrammers')
    s.recv(4096)
    s.send('RECD')
    return s

def test():
    
    date = datetime.today()
    print date
    connection = connect(57013)
    if connection:
        print connection.recv(4096)
        print connection.send('START')
        print connection.recv(4096)
        print connection.send('RECD')
        print connection.recv(4096)
        print connection.send('RECD')
        print connection.recv(4096)
        print connection.send('RECD')
        print connection.recv(4096)
            #else:
                #break;
        connection.send('CONTROL 1 1 1 1 1 1 1 1 1')
        
        connection.send('STOP') 
    else:
        print 'Connection Failed'
if __name__ == "__main__":
    test()