import socket, sys
from datetime import datetime
from ..models import Tier, Turn, Device, Region, Profit, Demand, MovingAverage
from django.conf import settings
from multiprocessing.dummy import Pool
import django

def run(port):
    connection = connect(port)
    if connection:
        costs = connection.recv(4096)
        costs = costs.strip('COSTS ').split(' ')
        generate_cost_models(costs)
        generate_region_models()

        Turn.objects.all().delete()
        # Begin the game
        connection.send('START')

        # Run this shit on a new thread!
        pool = Pool(processes=4)
        pool.apply_async(start, [connection])

def start(connection):
    day_str = None
    day_num = 0
    while True:
        # Generate the turn model
        config = connection.recv(4096)
        if not 'END' in config:

            # Generate Turn model to dump stuff into
            turn = Turn()
            turn.save()

            # Config Parsing
            config = config.strip('CONFIG ').split(' ')
            turn.config = generate_server_map_model(config)

            # Demand and Time Parsing
            connection.send('RECD')
            demand = connection.recv(4096)
            demand = demand.strip('DEMAND ').split(' ')
            date, demands, day_str, day_num = generate_demand_models(demand,day_str, day_num)
            turn.time = date
            turn.demands = demands

            # Distribution Parsing
            connection.send('RECD')
            distribution = connection.recv(4096)
            distribution = distribution.strip('DIST ').split(' ')
            turn.distribution = generate_server_map_model(distribution)

            # Profit Parsing
            connection.send('RECD')
            profit = connection.recv(4096)
            profit = profit.strip('PROFIT ').split(' ')
            profit = [p for p in profit if p != '']
            turn.profit = generate_profit_model(profit)

            turn.save()
            # Determine Moving Averages
            turn = determine_moving_averages(turn)

            turn.save()
            connection.send('CONTROL 1 1 1 1 1 1 1 1 1')
        else:
            break

    connection.send('STOP')

def determine_moving_averages(turn):

    SMOOTH = 2 / (1+2)
    demands = turn.demands

    try:
        last_turn = Turn.objects.get(id=(turn.id-1))
    except Turn.DoesNotExist:
        last_turn = None

    mas = []
    for demand in demands.all():
        ma = MovingAverage()
        ma.region = demand.region
        ma.transactions = demand.count

        if last_turn:
            last_demand  = None
            last_ma = None
            for d in last_turn.demands.all():
                if d.region == demand.region:
                    last_demand = d

            for m in last_turn.moving_averages.all():
                if m.region == demand.region:
                    last_ma = m

            ma.short_term = last_demand.count
            ma.long_term = (ma.transactions * SMOOTH) + (last_ma.long_term * 1 - SMOOTH)
        else:
            ma.short_term = ma.transactions
            ma.long_term = ma.transactions

        ma.web_needed = ma.transactions / 180
        resources = None
        for d in turn.config.all():
            if d.region == ma.region and d.tier.tier == 'w':
                resources = d.count

        ma.web_rsource = resources

        ma.save()
        mas.append(ma)

    turn.moving_averages = mas
    turn.save()
    return turn

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

def generate_demand_models(demand_list, day_str, day_num):

    day = demand_list[0]

    if not day_str:
        day_str = day

    if day_str != day:
        day_num += 1

    hours = demand_list[1]
    minutes = demand_list[2]
    seconds = demand_list[3]

    today = datetime.today()
    day = today.day + day_num
    date = datetime(today.year, today.month, day, int(hours),int(minutes),int(seconds))

    demands = []
    for region in Region.objects.all():
        demand = Demand()
        demand.region = region
        demand.count = demand_list[4 + list(Region.objects.all()).index(region)]
        demand.save()
        demands.append(demand)

    return date, demands, day_str, day_num

def generate_profit_model(profit):

    p = Profit()
    p.last_profit = int(profit[0])
    p.last_potential = int(profit[1])
    p.total_profit = int(profit[2])
    p.total_potential = int(profit[3])
    p.save()
    return p

def connect(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('67.202.15.69', int(port)))
    s.send('INIT Brogrammers')
    s.recv(4096)
    s.send('RECD')
    return s

if __name__ == "__main__":
    run()
