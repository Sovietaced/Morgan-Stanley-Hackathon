import socket, sys
from ..models import Tier
from django.conf import settings

def run(port=sys.argv[1]):
    connection = connect(port)
    if connection:
        costs = connection.recv(4096)
        costs = costs.strip('COSTS ').split(' ')
        generate_cost_models(costs)
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
        profit = [p for p in profit if p != '']
        profit 
        print profit
            #else:
                #break;
        connection.send('CONTROL 1 1 1 1 1 1 1 1 1')
        
        connection.send('STOP') 
    else:
        print 'Connection Failed'
    
def generate_cost_models(costs):
    
    # CLean the DB before we start a new game
    Tier.objects.all().delete()
    revenue_transaction_cents = costs[0]
    # Web Tier
    cost_web = costs[1]
    tier_web = Tier()
    tier_web.tier = 'w';
    tier_web.cost = int(cost_web)
    tier_web.save()
    
    # Java Tier
    cost_java = costs[2]
    tier_java = Tier()
    tier_java.tier = 'j'
    tier_java.cost = int(cost_java)
    tier_java.save()
    
    cost_db = costs[3]
    tier_db = Tier()
    tier_db.tier = 'd'
    tier_db.cost = int(cost_db)
    tier_db.save()

def connect(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('67.202.15.69', int(port)))
    s.send('INIT brogrammers')
    s.recv(4096)
    s.send('RECD')
    return s

if __name__ == "__main__":
    main()