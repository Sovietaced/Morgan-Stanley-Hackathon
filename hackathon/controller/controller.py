import socket, sys

def main(port=sys.argv[1]):
    connection = connect(port)
    if connection:
        costs = connection.recv(4096)
        costs = costs.strip('COSTS ').split(' ')
        revenue_transaction_cents = costs[0]
        cost_web = costs[1]
        cost_java = costs[2]
        cost_database = costs[3]
        print costs
        
        # Generate costs table for region
        
        # Begin the game
        connection.send('START')
        
        #while True:
        config = connection.recv(4096)
            #if not 'END' in config:
        config = config.strip('CONFIG ').split(' ')
        print config
        connection.send('RECD')
        demand = connection.recv(4096)
        demand = demand.strip('DEMAND ').split(' ')
        print demand
        connection.send('RECD')
        distribution = connection.recv(4096)
        distribution = distribution.strip('DIST ').split(' ')
        print distribution
        connection.send('RECD')
        profit = connection.recv(4096)
        profit = profit.strip('PROFIT ').split(' ')
        profit 
        print profit
            #else:
                #break;
        connection.send('CONTROL 1 1 1 1 1 1 1 1 1')
        
        connection.send('STOP') 
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