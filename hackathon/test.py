import socket, thread
from datetime import datetime


def run():
    connection = connect(57012)

    if connection:
        print 'swag'
        costs = connection.recv(4096)
        connection.send('START')
            
        # Run this shit on a new thread!
        start(connection)
        
def connect(port):
    print 'we startin'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'sconnecting'
    print s.connect(('67.202.15.69', port))
    print 'sending'
    print s.send('INIT StorganManley')
    print 'receiving'
    print s.recv(4096)
    print 'sending recd'
    print s.send('RECD')
    return s

def start(connection):
    print 'started connection'
    while True:
        # Generate the turn model
        config = connection.recv(9999)
        if not 'END' in config:
        
            print connection.send('RECD')
            print connection.recv(9999)
            print connection.send('RECD')
            print connection.recv(9999)
            print connection.send('RECD')
            profit = connection.recv(9999)
            print profit
            print connection.send('CONTROL 1 1 1 1 1 1 1 1 1')
            print '\n'
        else:
            break
    print 'sending stop'
    print connection.send('STOP')
    
if __name__ == "__main__":
    run()