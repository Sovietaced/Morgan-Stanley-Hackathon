import socket, sys
from ..models import Tier, Turn, Device, Region
from django.conf import settings

def run(port=sys.argv[1]):
    connection = connect(port)
    if connection:
        costs = connection.recv(4096)
        costs = costs.strip('COSTS ').split(' ')
        generate_cost_models(costs)
        generate_region_models()
        
        # Begin the game
        connection.send('START')
        
        #while True:
        # Generate the turn model
        turn = Turn()
        turn.save()
        
        config = connection.recv(4096)
            #if not 'END' in config:
        config = config.strip('CONFIG ').split(' ')
        
        turn.config,add(generate_config_model(config))
        turn.save()
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
    
def generate_region_models():
    Region.objects.all().delete()
    
    na_region = Region()
    na_region.region = 'n'
    na_region.save()
    
    e_region = Region()
    e_region.region = 'e'
    e_region.save()
    
    a_region = Region()
    a_region.region = 'a'
    a_region.save()
    
    
def generate_config_model(config):
    
    devices = []
    
    for region in Region.objects.all():
        web_device = Device()
        web_device.tier = Tier.objects.get(tier='w')
        web_device.region = region
        web_device.count = config[list(Region.objects.all()).index(region)/3]
        web_device.save()
        devices.append(web_device)
        
    return devices
    

def connect(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('67.202.15.69', int(port)))
    s.send('INIT brogrammers')
    s.recv(4096)
    s.send('RECD')
    return s

if __name__ == "__main__":
    main()