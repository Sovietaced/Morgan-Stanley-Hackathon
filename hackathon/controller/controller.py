import socket, sys
from datetime import datetime
from ..models import Tier, Turn, Device, Region, Profit, Demand
from django.conf import settings

def run(port=sys.argv[1]):
    connection = connect(port)
    if connection:
        costs = connection.recv(4096)
        costs = costs.strip('COSTS ').split(' ')
        generate_cost_models(costs)
        generate_region_models()
        
        Turn.objects.all().delete()
        # Begin the game
        connection.send('START')
        
        #while True:
        # Generate the turn model
        turn = Turn()
        turn.save()
        config = connection.recv(4096)
            #if not 'END' in config:
        config = config.strip('CONFIG ').split(' ')
        profit = Profit()
        turn.config = generate_server_map_model(config)
        turn.profit = profit.id
        connection.send('RECD')
        demand = connection.recv(4096)
        demand = demand.strip('DEMAND ').split(' ')
        turn.demands = generate_demand_models(demand)
        connection.send('RECD')
        distribution = connection.recv(4096)
        distribution = distribution.strip('DIST ').split(' ')
        turn.distribution = generate_server_map_model(distribution)
        print distribution
        connection.send('RECD')
        profit = connection.recv(4096)
        profit = profit.strip('PROFIT ').split(' ')
        profit = [p for p in profit if p != '']
        profit 
        print profit
        turn.save()
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
    
    
def generate_server_map_model(server_map):
    
    devices = []
    
    for region in Region.objects.all():
        web_device = Device()
        web_device.tier = Tier.objects.get(tier='w')
        web_device.region = region
        web_device.count = server_map[list(Region.objects.all()).index(region)]
        web_device.save()
        devices.append(web_device)
        
    for region in Region.objects.all():
        java_device = Device()
        java_device.tier = Tier.objects.get(tier='j')
        java_device.region = region
        java_device.count = server_map[3 + list(Region.objects.all()).index(region)]
        java_device.save()
        devices.append(java_device)
        
    for region in Region.objects.all():
        db_device = Device()
        db_device.tier = Tier.objects.get(tier='d')
        db_device.region = region
        db_device.count = server_map[6 + list(Region.objects.all()).index(region)]
        db_device.save()
        devices.append(db_device)
        
    return devices
    
def generate_demand_models(demand_list):
    day = demand_list[0]
    hours = demand_list[1]
    minutes = demand_list[2]
    seconds = demand_list[3]
    
    date = datetime.today()
    
    
    
    demands = [] 
    for region in Region.objects.all():
        demand = Demand()
        demand.region = region
        demand.count = demand_list[4 + list(Region.objects.all()).index(region)]
        demand.save()
        demands.append(demand)
        
    return demands

def connect(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('67.202.15.69', int(port)))
    s.send('INIT brogrammers')
    s.recv(4096)
    s.send('RECD')
    return s

if __name__ == "__main__":
    run()