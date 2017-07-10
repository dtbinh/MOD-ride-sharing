//! Attributions: Javier Alonso-Mora

import numpy as np
import matplotlib.image as mpimg
import re
import os
import matplotlib.pyplot as plt
import mpld3
import subprocess

myDir = "/Users/dhecht/Desktop/CSAIL/Ride-Sharing /visualize"
numeric_const_pattern = r"""
    [-+]? # optional sign
    (?:
        (?: \d* \. \d+ ) # .1 .12 .123 etc 9.1 etc 98.1 etc
        |
         (?: \d+ \.? ) # 1. 12. 123. etc 1 12 123 etc
    )
    # followed by optional exponent part if desired
    (?: [Ee] [+-]? \d+ ) ?
    """
rx = re.compile(numeric_const_pattern, re.VERBOSE)

class Parameters(object):
    def __init__(self):           
        self.NUMBER_VEHICLES = 0
        self.N_HIGHCAP_VEHICLES = 0
        self.maxTripSize = 0
        self.maxPassengersVehicle = 0
        self.MAX_PASS_HIGHCAP_VEHICLE = 0
        self.maxWaitTime = 0
        self.maxDelay = 0
        self.USE_PREDICTION = 0
        self.USE_REBALANCING = 0
        self.SAMPLED_DEMANDS_MAX_NUMBER = 0
        self.DEMAND_DAY = 0
        self.DEMAND_WEEK = 0
        self.DEMAND_YEAR = 0

class Vehicle(object):
    def __init__(self):                                       
        self.position = []                          
        self.passengers_id = []
        self.requests_scheduled = []
        self.travel_schedule_order = []
        self.travel_schedule_time = []
        self.travelled_distance = 0.0
        self.is_rebalancing = 0

class Person(object):
    def __init__(self):
        self.id = -1                                      
        self.origin = []                     
        self.destination = []
        self.station_origin = -1
        self.station_origin_pos = []
        self.station_dest = -1
        self.station_dest_pos = [] 
        self.time_request = -1
        self.time_pickup = -1
        self.time_dropoff = -1
        self.travel_time_optim = -1
        self.time_wait = -1
        self.time_delay = -1
        self.assigned = -1
        self.vehicle = -1
        self.prediction = -1

class Path(object):
    def __init__(self):                                       
        self.planned = []                          
        self.executed = []

class Performance(object):
    def __init__(self):                                       
        self.wait_mean = 0.0  
        self.wait_max = 0   
        self.delay_mean = 0.0  
        self.incar_delay_mean = 0.0  
        self.delay_max = 0 
        self.incar_delay_max = 0 
        self.n_pickup = 0
        self.n_delivered = 0
        self.occupancy_mean = 0.0  
        self.occupancy_max = 0

# TODO: THERE IS A PROBLEM WHEN IMPORTING CLOSE TO ZERO VALUES IN NOTATION 1.154E-15!!!

LAUNCH_IN_FOLDER = True

if LAUNCH_IN_FOLDER :
    save_folder = ''
else:
    save_folder_number = 1457970658
    save_folder = '../data-sim/data-' + str(save_folder_number) + '/'

if os.path.isdir(save_folder) is not True:
    save_folder = ''
    print( "The script is launched within the data folder")


# Get parameters
param = Parameters()
filename = save_folder + '../parameters.txt'
with open(filename,'r') as f:
    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.NUMBER_VEHICLES = int(elementList[0])
    
    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.maxTripSize = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.maxPassengersVehicle = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.maxWaitTime = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.maxDelay = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.USE_PREDICTION = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.USE_REBALANCING = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.SAMPLED_DEMANDS_MAX_NUMBER = int(elementList[0])
 
    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.N_MEMORY_DAYTIMES = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.DEMAND_DAY = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.DEMAND_WEEK = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.DEMAND_YEAR = int(elementList[0])

    for i in range(6):
        strLine = f.readline()

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.N_HIGHCAP_VEHICLES = int(elementList[0])

    strLine = f.readline()
    elementList = rx.findall(strLine)
    param.MAX_PASS_HIGHCAP_VEHICLE = int(elementList[0])

# import data trips
    n_capacity = param.maxPassengersVehicle
#if param.N_HIGHCAP_VEHICLES>0:
    #n_capacity = param.MAX_PASS_HIGHCAP_VEHICLE

time_step = 30
index_iter = 0
time_now = index_iter * time_step
while time_now>-1: # breaks when files end

    print("loading {:d} - {:d}".format(time_now, index_iter))
    figurename = save_folder + "../data/sim/sim-{0:05d}.jpg".format(index_iter)
    if os.path.exists(figurename) is not True:

        performance = Performance()

        # Import data
        vehicles = []
        requests = []
        passengers = []
        if os.path.exists(save_folder + '../data/graphs/data-graphs-{:d}.txt'.format(time_now)):
          filename = save_folder + '../data/graphs/data-graphs-{:d}.txt'.format(time_now)
        else:
          while os.path.exists(save_folder + '../data/graphs/data-graphs-{:d}.txt'.format(time_now)) is not True:
            time_now += time_step
            index_iter += 1
        filename = save_folder + '../data/graphs/data-graphs-{:d}.txt'.format(time_now)
        
        with open(filename,'r') as f:
            strLine = f.readline()

            # requests
            strLine = f.readline()
            elementList = rx.findall(strLine)
            for w in elementList:
                n_req = int(w)
            requests = []
            for i in range(0, n_req):
                strLine = f.readline()
                elementList = rx.findall(strLine)
                elementList = [float(x) for x in elementList]
                
                person = Person()

                person.id = i                                    
                person.origin = [elementList[0], elementList[1]]   
                person.destination = [elementList[2], elementList[3]]      
                person.station_origin = elementList[4]
                person.station_origin_pos = [elementList[5], elementList[6]] 
                person.station_dest = elementList[7]
                person.station_dest_pos = [elementList[8], elementList[9]] 
                person.time_request = elementList[10]
                person.assigned = elementList[11]
                person.vehicle = elementList[12]
                person.prediction = elementList[13]

                requests.append(person)

            # vehicles
            strLine = f.readline()
            strLine = f.readline()
            elementList = rx.findall(strLine)
            for w in elementList:
                n_veh = int(w)
            mean_travel_distance = 0
            for i in range(0, n_veh):

                strLine = f.readline()
                data_veh_aux = strLine.split('%')

                vehicle = Vehicle()
                data_aux = rx.findall(data_veh_aux[0])
                vehicle.position = [float(x) for x in data_aux] 
                data_aux = rx.findall(data_veh_aux[1])                       
                vehicle.passengers_id = [int(x) for x in data_aux] 
                data_aux = rx.findall(data_veh_aux[2]) 
                vehicle.requests_scheduled = [int(x) for x in data_aux] 
                data_aux = rx.findall(data_veh_aux[3]) 
                vehicle.travel_schedule_order = [int(x) for x in data_aux] 
                data_aux = rx.findall(data_veh_aux[4]) 
                vehicle.travel_schedule_time = [float(x) for x in data_aux]
                vehicle.travelled_distance = float(data_veh_aux[5])
                vehicle.is_rebalancing = int(data_veh_aux[6])
                mean_travel_distance += vehicle.travelled_distance

                vehicles.append(vehicle)
            mean_travel_distance /= n_veh

            # passengers
            strLine = f.readline()
            strLine = f.readline()
            elementList = rx.findall(strLine)
            for w in elementList:
                n_pass_total = int(w)
            passengers = []
            for i in range(0, n_pass_total):
                strLine = f.readline()
                elementList = rx.findall(strLine)
                elementList = [float(x) for x in elementList]

                person = Person()

                person.id = elementList[0]                                  
                person.origin = [elementList[1], elementList[2]]  
                person.destination = [elementList[3], elementList[4]]    
                person.station_origin = elementList[5]
                person.station_origin_pos = [elementList[6], elementList[7]] 
                person.station_dest = elementList[8]
                person.station_dest_pos = [elementList[9], elementList[10]] 
                person.time_request = elementList[11]
                person.time_pickup = elementList[12]
                person.time_dropoff = elementList[13]
                person.travel_time_optim = elementList[14]
                person.assigned = 1
                person.vehicle = elementList[15]

                person.time_wait = person.time_pickup - person.time_request
                # if person.time_wait < 0:
                #    print "Negative waiting time!!"
                performance.wait_mean += person.time_wait
                performance.n_pickup += 1
                if person.time_wait > performance.wait_max :
                    performance.wait_max = person.time_wait
                if person.time_dropoff > person.time_pickup :
                    person.time_delay = person.time_dropoff - person.time_request - person.travel_time_optim
                    performance.delay_mean += person.time_delay
                    performance.incar_delay_mean += person.time_delay - person.time_wait
                    performance.n_delivered += 1
                    # if person.time_delay < person.time_wait:
                    #    print "Delay %f lower than wating %f!!"  \
                    #        % (person.time_delay, person.time_wait)
                    if person.time_delay > performance.delay_max :
                        performance.delay_max = person.time_delay        
                    if (person.time_delay - person.time_wait) > performance.incar_delay_max :
                        performance.incar_delay_max = (person.time_delay - person.time_wait)    
                # elif person.time_dropoff > 0 :
                #    print "Drop-off before Pick-up!!!"
                passengers.append(person)

                if person.id == n_pass_total - 1:
                    break

            if performance.n_pickup > 0 :
                performance.wait_mean /= performance.n_pickup
            if performance.n_delivered > 0 :
                performance.delay_mean /= performance.n_delivered
                performance.incar_delay_mean /= performance.n_delivered
                # Remove rounding error
                performance.incar_delay_mean = max(performance.incar_delay_mean, 0)

            print("waiting = %d (%d ), delay = %d (%d ), incar_delay = %d (%d )" % \
                   (performance.wait_mean, performance.wait_max,
                   performance.delay_mean, performance.delay_max,
                   performance.incar_delay_mean, performance.incar_delay_max))

            print 

            # performance
            strLine = f.readline()
            strLine = f.readline()
            strLine = f.readline()
            l = rx.findall(strLine)
            n_pickups = int(l[0])
            n_total_pickups = int(l[1])
            n_dropoffs = int(l[2])
            n_total_dropoffs = int(l[3])
            n_ignored = int(l[4])
            n_total_ignored = int(l[5])
            n_rebalancing = int(l[6])

            # R-V graph
            strLine = f.readline()
            strLine = f.readline()
            strLine = f.readline()    
            RVgraph_RRedges = []
            strLine = f.readline()
            while len(re.findall("#", strLine)) == 0:
                elementList = rx.findall(strLine)
                elementList = [int(x) for x in elementList]
                size = len(elementList)
                for i in range(0,int(size/2)):
                    RVgraph_RRedges.append([elementList[2*i], elementList[2*i+1]])
                strLine = f.readline()
            RVgraph_VRedges = []
            strLine = f.readline()
            while len(re.findall("#", strLine)) == 0:
                elementList = rx.findall(strLine)
                elementList = [int(x) for x in elementList]
                size = len(elementList)
                for i in range(0, int(size/2)):
                    RVgraph_VRedges.append([elementList[2*i], elementList[2*i+1]])
                strLine = f.readline()

            # Trips
            elementList = rx.findall(strLine)
            for w in elementList:
                n_trips = int(w)
            trips = []
            for i in range(0, n_trips):
                strLine = f.readline()
                w_trip = strLine.split('%')
                aux_strLine = [];
                for j in range(0, len(w_trip)):
                    aux = rx.findall(w_trip[j])
                    aux = [int(x) for x in aux]
                    aux_strLine.append(aux)
                trips.append(aux_strLine)

        print("n_pickups = %d (%d), n_dropoffs = %d(%d), n_ignored = %d (%d), n_rebalancing = %d" \
                % (n_pickups, n_total_pickups, n_dropoffs, n_total_dropoffs,
                   n_ignored, n_total_ignored, n_rebalancing))

        # import data assignment
        if os.path.exists(save_folder + '../data/assignment/data-assignment-{:d}.txt'.format(time_now)):
          filename = save_folder + '../data/assignment/data-assignment-{:d}.txt'.format(time_now)
        else:
          while os.path.exists(save_folder + '../data/assignment/data-assignment-{:d}.txt'.format(time_now)) is not True:
            time_now += time_step
            index_iter += 1
        filename = save_folder + '../data/assignment/data-assignment-%d.txt' % (time_now)
          
        with open(filename,'r') as f:
            strLine = f.readline()
            strLine = f.readline()
            elementList = rx.findall(strLine)
            n_links = int(elementList[0])
            links_assignment = []

            n_assign_float = 0;
            n_assign_all = 0;
            
            for l in range(0,n_links):
                strLine = f.readline()
                elementList = rx.findall(strLine)
                id_trip = int(elementList[0])
                id_veh = int(elementList[1])
                cost_link = float(elementList[2])

                assign_link = 0
                if float(elementList[3])>0.999:
                    assign_link = 1
                    n_assign_all += 1
                elif float(elementList[3]) > 0.001:
                    n_assign_float +=1
                
                links_assignment.append([id_trip,id_veh,cost_link,assign_link])

        n_assign_all += n_assign_float
        print("Number of links {:d}".format(len(links_assignment)))
        if n_assign_float>0:
            print("Non binary assignments = {:d} / {:d}!".format(n_assign_float, n_assign_all))

        # # Store the travel for each trip
        # travels_order = [];
        # travels = [];
        # travels_pickup = [];
        # link_id = 0
        # for t in range(0, n_trips):
        #     for i in range(2, len(trips[t])):
        #         travel_order = trips[t][i]
        #         travels_order.append(travel_order);

        #         link = links_assignment[link_id]
        #         if link[3] == 1:
        #             travel = []
        #             travel_pick = []
        #             vehicle = vehicles[link[1]]
        #             pos = [vehicle.position[0], vehicle.position[1], link[1]]
        #             n_passengers = len(vehicle.passengers_id)
        #             travel.append(pos)
        #             travel_pick.append(pos)
        #             for i_travel in travel_order:
        #                 if i_travel < 0: # passenger/request drop-off
        #                     i_travel = abs(i_travel) - 1
        #                     if i_travel < n_passengers: # it was a passenger
        #                         id_pas = int(vehicle.passengers_id[i_travel])
        #                         pos = [passengers[id_pas][2], passengers[id_pas][3], id_pas]
        #                     else: # it was a request
        #                         id_req = trips[t][0][i_travel - n_passengers]
        #                         pos = [requests[id_req][2], requests[id_req][3], id_req]
        #                 else: # request pick-up
        #                     i_travel = i_travel - 1
        #                     id_req = trips[t][0][i_travel - n_passengers]
        #                     pos = [requests[id_req][0], requests[id_req][1], id_req]
        #                     travel_pick.append(pos)
        #                 travel.append(pos)
        #             travels.append(travel)
        #             travels_pickup.append(travel_pick)
        #         link_id += 1

        # # Store the travel for each vehicle
        # car_travels = [];
        # for i_veh in range(0, n_veh):
        #     vehicle = vehicles[i_veh]
        #     car_travel = []
        #     pos = [vehicle.position[0], vehicle.position[1], i_veh]
        #     n_passengers = len(vehicle.passengers_id)
        #     car_travel.append(pos)

        #     for i_travel in vehicle.travel_schedule_order:

        #         if i_travel < 0: # passenger/request drop-off
        #             i_travel = abs(i_travel) - 1
        #             if i_travel < n_passengers: # it was a passenger
        #                 id_pas = vehicle.passengers_id[i_travel]
        #                 pos = [passengers[id_pas][2], passengers[id_pas][3], id_pas]
        #             else: # it was a request
        #                 id_req = vehicle.requests_scheduled[i_travel - n_passengers]
        #                 pos = [requests[id_req][2], requests[id_req][3], id_req]
        #         else: # request pick-up
        #             i_travel = i_travel - 1
        #             id_req = vehicle.requests_scheduled[i_travel - n_passengers]
        #             pos = [requests[id_req][0], requests[id_req][1], id_req]
        #             travel_pick.append(pos)

        #         car_travel.append(pos)

        #     car_travels.append(car_travel)

        # import data paths
        if os.path.exists(save_folder + '../data/paths/data-paths-{:d}.txt'.format(time_now)):
          filename = save_folder + '../data/paths/data-paths-{:d}.txt'.format(time_now)
        else:
          while os.path.exists(save_folder + '../data/paths/data-paths-{:d}.txt'.format(time_now)) is not True:
            time_now += time_step
            index_iter += 1
        filename = save_folder + '../data/paths/data-paths-{:d}.txt'.format(time_now)
        
        vehicle_paths = []
        with open(filename,'r') as f:
            strLine = f.readline()
            elementList = rx.findall(strLine)
            for w in elementList:
                n_veh = int(w)
            for i in range(0, n_veh):

                strLine = f.readline()
                data_paths_aux = strLine.split('%')

                path = Path()
                data_aux = rx.findall(data_paths_aux[0])
                data_aux = [float(x) for x in data_aux]
                for j in range(0, int(len(data_aux)/2)):
                    path.executed.append([data_aux[2*j], data_aux[2*j + 1]])

                data_aux = rx.findall(data_paths_aux[1])
                data_aux = [float(x) for x in data_aux]
                for j in range(0, int(len(data_aux)/2)):
                    path.planned.append([data_aux[2*j], data_aux[2*j + 1]])

                vehicle_paths.append(path)

        #-------------------------------------------------------
        # Plot figures
        #-------------------------------------------------------

        print ("Data imported - plotting {:d} -  {:d} ".format(time_now, index_iter))

        if n_capacity == 1:
            veh_colors = ['cyan','darkred','blue']
        elif n_capacity == 2:
            veh_colors = ['cyan','darkorange','darkred', 'blue']
        elif n_capacity <= 4:
            veh_colors = ['cyan','greenyellow','darkorange','magenta','darkred', 'blue']
            #veh_colors = ['cyan','yellowgreen','gold','orangered','darkred', 'blue']
            # veh_colors = ['green','greenyellow','yellow','orange','red', 'blue']
        else:
            veh_colors = ['cyan', 'lightgreen', 'greenyellow', 'gold','darkorange','salmon','red','magenta','darkviolet','darkmagenta', 'darkred', 'blue']
            #veh_colors = ['cyan', 'lightgreen', 'greenyellow', 'yellow','gold','orange','salmon','red','magenta','darkmagenta', 'darkred', 'blue']
            #veh_colors = ['cyan', 'lightgreen', 'greenyellow', 'yellowgreen','yellow','salmon','coral','orangered','magenta','darkmagenta', 'darkred', 'blue']
            #veh_colors = ['cyan', 'lightgreen', 'greenyellow', 'yellowgreen','yellow','salmon','coral','orangered','magenta','red', 'darkred', 'blue']
            #veh_colors = ['green', 'lightgreen', 'greenyellow', 'yellowgreen','yellow','orange','salmon','pink','coral','magenta','red', 'blue']
        trip_colors = ['green','dodgerblue','deepskyblue','saddlebrown','green'];
        trip_line_format = ['k-','k:','k--','k.-']

        # plot requests-vehicles at their start/current position

        fig1 = plt.figure(time_now)
        high_res = False
        if high_res:
            plt.figure(figsize = (20,20))
            size_markers = [6,6,9,6,6,21,18,18,15]
            alpha_markers = [0.7,0.7,1]
            edgewidth_markers = [1,1]
        else:
            size_markers = [2,2,3,2,2,7,6,6,5]
            alpha_markers = [0.4,0.4,0.9]
            edgewidth_markers = [0.2,0.2]

        # Display assignment links vehicles - requests
        # for travel in travels_pickup:
        #     for i in range(1,len(travel)):
        #         p1 = travel[i - 1]
        #         p2 = travel[i]
        #         plt.plot([p1[1], p2[1]], [p1[0], p2[0]], 'k', linewidth = 1, alpha = 0.1)

        # Travel trip
        # for t in range(0, n_veh):        
        #     for i in range(1,len(vehicle_paths[t].executed)):
        #          p1 = vehicle_paths[t].executed[i-1]
        #          p2 = vehicle_paths[t].executed[i]
        #          plt.plot([p1[1], p2[1]], [p1[0], p2[0]], c = "yellow", linewidth = 1, alpha = 0.05)

        #     for i in range(1,len(vehicle_paths[t].planned)):
        #          p1 = vehicle_paths[t].planned[i-1]
        #          p2 = vehicle_paths[t].planned[i]
        #          plt.plot([p1[1], p2[1]], [p1[0], p2[0]], c = "grey", linewidth = 1, alpha = 0.05)

        if len(RVgraph_RRedges) < 1:
            for w in RVgraph_RRedges:
                p1 = requests[w[0]].origin
                p2 = requests[w[1]].origin
                plt.plot([p1[1], p2[1]], [p1[0], p2[0]], 'r:')
            for w in RVgraph_VRedges:
                p1 = vehicles[w[0]].position
                p2 = requests[w[1]].origin
                plt.plot([p1[1], p2[1]], [p1[0], p2[0]], 'g--')

        for w in requests:
            if w.assigned == 1 :
                plt.plot(w.origin[1], w.origin[0], 'k*', markersize = size_markers[0], alpha = alpha_markers[0])
            else:
                plt.plot(w.origin[1], w.origin[0], 'r*', markersize = size_markers[1], alpha = alpha_markers[1]) # 3 and 0.3

        for w in vehicles:
            num_pass = len(w.passengers_id)
            performance.occupancy_mean += num_pass
            if num_pass > performance.occupancy_max :
                performance.occupancy_max = num_pass            
            if w.is_rebalancing == 1:
                num_pass = n_capacity + 1

            plt.plot(w.position[1], w.position[0], 'o', c = veh_colors[num_pass],
                    markersize = size_markers[2], alpha = alpha_markers[2], markeredgewidth=edgewidth_markers[0]) # 4 and 0.5
        
        performance.occupancy_mean /= n_veh

        # Display N vehicles on top
        n_vehicles_highlight = 2

        for t in range(0, min(n_vehicles_highlight, n_veh)):        
            # # Travel trip
            # for i in range(1,len(car_travels[t])):
            #     p1 = car_travels[t][i - 1]
            #     p2 = car_travels[t][i]
            #     plt.plot([p1[1], p2[1]], [p1[0], p2[0]], c = trip_colors[t], linewidth = 2, alpha = 1)

            for i in range(1,len(vehicle_paths[t].executed)):
                 p1 = vehicle_paths[t].executed[i-1]
                 p2 = vehicle_paths[t].executed[i]
                 plt.plot([p1[1], p2[1]], [p1[0], p2[0]], c = "yellow", linewidth = size_markers[3], alpha = 1)

            for i in range(1,len(vehicle_paths[t].planned)):
                 p1 = vehicle_paths[t].planned[i-1]
                 p2 = vehicle_paths[t].planned[i]
                 plt.plot([p1[1], p2[1]], [p1[0], p2[0]], trip_colors[t], linewidth = size_markers[4], alpha = 1)

            # Requests
            for i in range(0,len(vehicles[t].requests_scheduled)):
                id_req = vehicles[t].requests_scheduled[i]
                p1 = requests[id_req].station_origin_pos
                plt.plot(p1[1], p1[0], 'k*', markersize = size_markers[5], alpha = 1)
                p2 = requests[id_req].station_dest_pos
                plt.plot(p2[1], p2[0], 'kv', markersize = size_markers[6], alpha = 1)

            # Passengers
            for id_pass in vehicles[t].passengers_id:
                for id_aux in range(0,len(passengers)):
                    if passengers[id_aux].id == id_pass:
                        p2 = passengers[id_aux].station_dest_pos
                        plt.plot(p2[1], p2[0], 'kv', markersize = size_markers[7], alpha = 1)

            # Position car
            num_pass = len(vehicles[t].passengers_id)
            if vehicles[t].is_rebalancing == 1:
                num_pass = n_capacity + 1

            plt.plot(vehicles[t].position[1], vehicles[t].position[0], 'o',
                 c = veh_colors[num_pass], markersize = size_markers[8], alpha = 1, markeredgewidth=edgewidth_markers[1])

        # Make figure pretty
        m, s = divmod(time_now, 60)
        h, m = divmod(m, 60)

        if not high_res:
            plt.title('%4d Req, Time %d-%d-%d %02d:%02d:%02d' \
                        % (n_req, param.DEMAND_DAY, param.DEMAND_WEEK, param.DEMAND_YEAR, h, m, s))

            super_title = 'Vehicles: %d, Capacity: %d, Max_wait: %d, Max_delay: %d, Samples: %d, Rebalance: %d' \
                        % (n_veh, n_capacity, param.maxWaitTime, param.maxDelay, \
                        (param.SAMPLED_DEMANDS_MAX_NUMBER * param.USE_PREDICTION), param.USE_REBALANCING)
            plt.annotate(super_title, (0,0), (-120, 385), xycoords='axes fraction',
                textcoords='offset points', va='top')

        # image = mpimg.imread("../map/map-manhattan-1.png")
        # axis = [-73.993498, -73.957058, 40.752273, 40.766382] # manhattan
        # image = mpimg.imread(save_folder + "../../map/soho.png")
        # axis = [-74.01002602762065, -73.96044289997499, 40.7354687066417, 40.77202074228057] # soho
        # image = mpimg.imread(save_folder + "../../map/manhattan-downtown.png")
        # axis = [-74.01824376474143, -73.94812921425887, 40.73320343981938, 40.77082617894838] # downtown
        # image = mpimg.imread(save_folder + "../../map/map-manhattan.png")
        # axis = [-74.0216305923443, -73.92825168720965, 40.70003931056439, 40.81495971924326] # manhattan
        image = mpimg.imread(save_folder + "../map/manhattan-full.png")
        axis = [-74.0190, -73.9064, 40.6994, 40.8782] # manhattan full
        # image = mpimg.imread(save_folder + "../../map/close-up-manhattan-bw.png")
        # axis = [-74.0089, -73.9581, 40.7103, 40.7690] # manhattan close up
        # image = mpimg.imread(save_folder + "../../map/mid-manhattan.png")
        # axis = [-74.0124, -73.9646, 40.7308, 40.7673] # manhattan center
        # image = mpimg.imread(save_folder + "../../map/mid-manhattan-2.png")
        # axis = [-74.0184, -73.9492, 40.7217, 40.7802] # manhattan center
        
        plt.imshow(image, zorder=0, extent=axis, alpha = 0.8)

        # plt.axis([103.6, 104.1, 1.2, 1.5])
        # plt.axis([-74.02, -73.91, 40.7, 40.875])
        plt.axis(axis)
        plt.axes().set_aspect('equal')
        if high_res:
            plt.axes().set_aspect(1.3)
        plt.axes().get_xaxis().set_visible(False)
        plt.axes().get_yaxis().set_visible(False)

        color_legend = "Vehicle color for passengers from 0 to {:d}, rebalancing:  ".format(len(veh_colors)-2)
        all_colors = ''
        for w in veh_colors:
            all_colors += w + ", "

        serviced = n_pickups * 100.0 / max(1.0,(n_ignored + n_pickups))
        serviced_total = n_total_pickups * 100.0 / max(1.0,(n_total_ignored + n_total_pickups))

        # Outside legends
        if not high_res:
            performance_data = "Picked up = %d  %d " % \
                            (n_pickups, n_total_pickups)
            plt.annotate(performance_data, (0,0), (230, 300), xycoords='axes fraction',
                textcoords='offset points', va='top')
            performance_data = "Dropped off = %d  (%d )" % \
                            (n_dropoffs, n_total_dropoffs)
            plt.annotate(performance_data, (0,0), (230, 280), xycoords='axes fraction',
                textcoords='offset points', va='top')
            performance_data = "Ignored = %d  (%d )" % \
                            (n_ignored, n_total_ignored)
            plt.annotate(performance_data, (0,0), (230, 260), xycoords='axes fraction',
                textcoords='offset points', va='top')
            performance_data = "Rebalancing = %d " % \
                             (n_rebalancing)
            plt.annotate(performance_data, (0,0), (230, 240), xycoords='axes fraction',
                textcoords='offset points', va='top')

            performance_data = "Serviced = %d%% (%d%%)" \
                            % (serviced, serviced_total)
            plt.annotate(performance_data, (0,0), (230, 200), xycoords='axes fraction',
                textcoords='offset points', va='top')

            performance_data = "Waiting time [s]"
            plt.annotate(performance_data, (0,0), (230, 160), xycoords='axes fraction',
                textcoords='offset points', va='top')
            performance_data = "Mean = %d , max = %d "  \
                           % (performance.wait_mean, performance.wait_max)
            plt.annotate(performance_data, (0,0), (230, 140), xycoords='axes fraction',
                textcoords='offset points', va='top')
            performance_data = "Delay [s]"
            plt.annotate(performance_data, (0,0), (230, 120), xycoords='axes fraction',
                textcoords='offset points', va='top')
            performance_data = "Mean = %d , max = %d "  \
                           % (performance.delay_mean, performance.delay_max)
            plt.annotate(performance_data, (0,0), (230, 100), xycoords='axes fraction',
                textcoords='offset points', va='top')
            performance_data = "Occupancy"
            plt.annotate(performance_data, (0,0), (230, 80), xycoords='axes fraction',
                textcoords='offset points', va='top')
            performance_data = "Mean = %.1f, max = %d " \
                           % (performance.occupancy_mean, performance.occupancy_max)
            plt.annotate(performance_data, (0,0), (230, 60), xycoords='axes fraction',
                textcoords='offset points', va='top')

            plt.annotate(color_legend, (0,0), (-150, -1), xycoords='axes fraction',
                textcoords='offset points', va='top')
            plt.annotate(all_colors, (0,0), (-150, -13), xycoords='axes fraction',
                textcoords='offset points', va='top')
            plt.annotate('Path of some vehicles. Star = pick-up; Triangle = drop-off',
                (0,0), (-150, -25), xycoords='axes fraction', textcoords='offset points', va='top')

            # Colors legend
            for index in range(0, n_capacity+1):
                plt.annotate("..", xy=(0, 0), xycoords='axes fraction',
                    xytext=(-10, 35 + 20*index), textcoords='offset points',
                    bbox=dict(boxstyle="round", fc = veh_colors[index]),
                    arrowprops=dict(arrowstyle="-",
                                    connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                    )
                plt.annotate(index, (0,0), (-25, 45 + 20 * index), xycoords='axes fraction',
                    textcoords='offset points', va='top',size=10)
            index = n_capacity + 1
            plt.annotate("..", xy=(0, 0), xycoords='axes fraction',
                    xytext=(-10, 10), textcoords='offset points',
                    bbox=dict(boxstyle="round", fc = veh_colors[index]),
                    arrowprops=dict(arrowstyle="-",
                                    connectionstyle="angle,angleA=0,angleB=90,rad=10"),
                    )
            plt.annotate("R", (0,0), (-25, 20), xycoords='axes fraction',
                    textcoords='offset points', va='top',size=10)

            # Inside legend - performance
            perform_data = []

            perform_data.append("Service rate, c. [total]:")
            perform_data.append("  %d%%   [%d%%]" \
                            % (serviced, serviced_total))

            perform_data.append("Waiting time, c.m.:")
            aux_val = performance.wait_mean % 60
            perform_data.append("  %d min %d  s" \
                           % (int((performance.wait_mean - aux_val) / 60), aux_val))

            perform_data.append("In-car delay, c.m.:")
            aux_val = (performance.incar_delay_mean) % 60
            perform_data.append("  %d  min %d  s"  \
                           % ((performance.incar_delay_mean - aux_val) / 60, aux_val))

            perform_data.append("Occupancy, c.m.:")
            perform_data.append("  %.1f pass/vehicle" \
                           % (performance.occupancy_mean))

            perform_data.append("Travel distance, c.m.:")
            perform_data.append("  %d  km/vehicle" \
                           % (mean_travel_distance))

            index = 0
            for text in perform_data:
                plt.annotate(text, (0,0), (5, 345 - 14*index), xycoords='axes fraction',
                    textcoords='offset points', va='top',size=9)
                index += 1

            # Inside legend - parameters
            param_data = []

            m, s = divmod(time_now, 60)
            h, m = divmod(m, 60)        

            day_of_week = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]

            param_data.append("n: {:d} vehicles".format((n_veh)))
            param_data.append("c: {:d} passengers".format((n_capacity)))
            param_data.append("W: {} min".format((param.maxWaitTime / 60)))
            param_data.append("D: {} min".format(param.maxDelay / 60))
            param_data.append("Day: %s %d -%d -%d " \
                   % (day_of_week[param.DEMAND_DAY - 1], param.DEMAND_DAY, param.DEMAND_WEEK, param.DEMAND_YEAR))
            param_data.append("Time: %02d:%02d:%02d" % (h, m, s))

            index = 0
            for text in param_data:
                plt.annotate(text, (0,0), (120, 90 - 14*index), xycoords='axes fraction',
                    textcoords='offset points', va='top',size=9)
                index += 1

        fig, ax = plt.subplots()        
        plt.draw()
        
        #fig.savefig(figurename, format = 'png', dpi = 200)
       
        plt.show(fig)
        
        

        plt.close()

    time_now += time_step
    index_iter += 1
    
    


    

# generate movie
subprocess.run("ffmpeg -f image2 -r 25 -i sim/sim-%05d.jpg -vcodec mpeg4 -y movie.mp4".split())
subprocess.call("avconv -f image2 -r 25 -i sim/sim-%05d.jpg -vcodec mpeg4 -y movie.mp4".split())
