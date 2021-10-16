from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative
from img_pro import detect_circle
import time
import math

ptime = time.time()

class Iha():

    def __init__(self, connection_string) -> None:
        self.connection_string = connection_string
        self.vehicle = connect(self.connection_string, wait_ready=True)
        if self.vehicle:
            print("Succesfully connected to the MP!")
        
            self.vehicle.mode = VehicleMode("AUTO")


    def download_commands(self):
        cmds = self.vehicle.commands
        cmds.download()
        cmds.wait_ready()

        if cmds:
            print("Commands are successfully downloaded from MP!")

        return cmds
    

    def arming_plane(self):

        self.vehicle.arm(wait=True)

        if self.vehicle.armed == True:
            print("Vehicle is armed!")


    def waypoint(self):
        nextwaypoint = self.vehicle.commands.next
        return nextwaypoint


    def battery_info(self):

        if self.vehicle.battery.level % 5 == 0:
            print("---------------------------------")
            print("Battery: {}".format(self.vehicle.battery.level))
            print("----------------------------------")

    def coordinates(self):
        global_location = self.vehicle.location.global_frame
        return global_location
    

    def altimeter(self):
        return self.vehicle.location.global_relative_frame.alt

    def get_meter(self, aLocation1, aLocation2):
            dlat = aLocation2.lat - aLocation1.lat
            dlong = aLocation2.lon - aLocation1.lon
            return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5


    def distance_to_current_waypoint(self, nextwaypoint):
        if nextwaypoint==0:
            return None
        missionitem = iha.download_commands()[nextwaypoint]
        lat = missionitem.x
        lon = missionitem.y
        alt = missionitem.z
        targetWaypointLocation = LocationGlobalRelative(lat,lon,alt)
        distancetopoint = iha.get_meter(self.vehicle.location.global_frame, targetWaypointLocation)
        return distancetopoint

    def time2rtl(self):
        self.vehicle.mode = VehicleMode("RTL")


iha = Iha('tcp:127.0.0.1:5760')

iha.download_commands()
iha.arming_plane()

while True:
    iha.battery_info()

    if iha.waypoint() == 1:
        print("-------------------------------------------")
        print("Taking off!")
        print("Alt: ", iha.altimeter())
        time.sleep(1)
    
    if iha.waypoint() == 2:
        print("-------------------------------------------")
        print("Going to waypoint 2!")
        print("Alt: ", iha.altimeter())
        print("Distance to current waypoint is: ", iha.distance_to_current_waypoint(1))
        time.sleep(1)

    if iha.waypoint() == 3:
        print("-------------------------------------------")
        print("Going to waypoint 3!")
        print("Alt: ", iha.altimeter())
        print("Distance to current waypoint is: ", iha.distance_to_current_waypoint(2))
        print("Turning on the camera!")
        detect_circle(5)

    if iha.waypoint() == 4:
        print("-------------------------------------------")
        print("Going to waypoint 3!")
        print("Alt: ", iha.altimeter())
        print("Distance to current waypoint is: ", iha.distance_to_current_waypoint(3))
        time.sleep(1)

    if iha.waypoint() == 5:
        print("-------------------------------------------")
        print("Going to waypoint 3!")
        print("Alt: ", iha.altimeter())
        print("Distance to current waypoint is: ", iha.distance_to_current_waypoint(4))
        print("Turning on the camera!")
        detect_circle(5)
        break

iha.time2rtl()

