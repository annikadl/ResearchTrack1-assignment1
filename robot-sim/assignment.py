from __future__ import print_function

import time
from sr.robot import *

R = Robot()
""" instance of the class Robot"""

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""


def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_token():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is 	detected)
    """
    dist=100
    for token in R.see():
    	if token.dist < dist:
    		dist = token.dist
    		rot_y = token.rot_y
    		token_id = token.info.offset
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y, token_id
   	
  
# TODO: i dont think i need this func
'''	   	
def grab_token():
	while 1:
	    dist, rot_y = find_token()  # we look for markers
	    if dist==-1:
		print("I don't see any token!!")
		exit()  # if no markers are detected, the program ends
	    elif dist <d_th: 
		print("Found it!")
		R.grab() # if we are close to the token, we grab it.
		print("Gotcha!") 
		exit()
	    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, here we are!.")
		drive(10, 0.5)
	    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		print("Left a bit...")
		turn(-2, 0.5)
	    elif rot_y > a_th:
		print("Right a bit...")
		turn(+2, 0.5)	 '''
		   	
		
def center_group(markers):
	min_dist = 100
	for m in markers:
		if m.dist < min_dist:
			min_dist = m.dist
			id_min_dist_token = m.info.offset
			
	max_dist = 0
	for m in markers:
		if m.dist > max_dist:
			max_dist = m.dist
			id_max_dist_token = m.info.offset
			
	#print(min_dist, max_dist)
	
	# target_distance from the min_dist_token
	target_distance = (min_dist+max_dist)/2
	
	return target_distance, id_max_dist_token, id_min_dist_token
	
def go_take_token(dist, rot_y, token_id1):
	counter_left_rotation = 0
	counter_right_rotation = 0
	
	notgrabbed = 0;
	
	# non so se va bene while true
	while notgrabbed == 0: 
		if rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			# print("Left a bit...")
			turn(-10, 0.1)
			drive(15,0.5)
			counter_left_rotation = counter_left_rotation +1
		elif rot_y > a_th:
			# print("Right a bit...")
			turn(+10, 0.1)	
			drive(15,0.5)  
			counter_right_rotation = counter_right_rotation +1
		elif -a_th<= rot_y <= a_th and dist >d_th: # if the robot is well aligned with the token, we go forward
			# print("Ah, here we are!.")
			drive(15, 0.5)   	   
		elif dist <d_th: 
			drive(0,1)
			# print("Found it!")
			R.grab() # if we are close to the token, we grab it.
			print("Gotcha!") 
			notgrabbed = 1;
			#turn(20,2)
			#drive(20,2)
			#R.release()
			#drive(-20,2)
			#turn(-10,1.3)
		
		dist, rot_y, token_id2 = find_token()
		if token_id2 == token_id2:
			token_id1 = token_id2
		else: 
			print('i dont see the token ', token_id1, ' anymore')
			print('now i see token ', token_id2)
	return counter_left_rotation, counter_right_rotation

def main():

	dist, rot_y, token_id = find_token()
	while dist == -1:  # we look for markers
	     print("I don't see any token!!")
	     drive(10,0.5)
	     turn(10,0.5)
	     dist, rot_y, token_id = find_token()

	markers = R.see()
	print ("I can see", len(markers), "markers:")
	
	target_distance, id_max_dist_token, id_min_dist_token = center_group(markers)

	#for m in markers:	
	#	print (" - Token {0} is {1} metres away".format( m.info.offset, m.dist )

	print('the distance between nearset and farest token is: ', target_distance)
	print('offset of min_dist_ token is: ',id_min_dist_token )
	print('offset of max_dist_ token is: ',id_max_dist_token)
	
	
	# TODO: implement how to reach target distance here to call just a function iteratively on each token. by now it works, so i'll do it later
	# it's okay to use them as a return, so when i'll put the functionality inside the function itself i already have these values avaiable
	counter_left_rotation, counter_right_rotation = go_take_token(dist, rot_y, token_id) 
	
	#TODO: actually count rotation instead of performing rotations without check
	# perform a rotation that brings e back to the inizial rotation
	while counter_left_rotation != 0:
		# for each left rot,i do a right rot
		print("Right a bit...")
		turn(+10, 0.1)	
		counter_left_rotation = counter_left_rotation-1
		print(counter_left_rotation)
	
	while counter_right_rotation != 0:
		# for each right rot,i do a left rot
		print("Left a bit...")
		turn(-10, 0.1)	
		counter_right_rotation = counter_right_rotation -1
		print(counter_right_rotation)
	
	
	# update distance between target and actual distance
	
	''' while target_distance-dist > 0:
				print(target_distance-dist)
				dist, rot_y, token_id = find_token()
				drive(10,0.5)
			R.release() 	 '''
	
	 
	
	
	
	'''
	while 1:
		dist, rot_y, token_id = find_token()  # we look for markers
	    	if dist == -1:
	     		print("I don't see any token!!")
	     		drive(10,0.5)
	     		turn(10,0.5)
			# exit()  # if no markers are detected, the program ends
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-10, 0.1)
			drive(15,0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(+10, 0.1)	
			drive(15,0.5)  
		elif -a_th<= rot_y <= a_th and dist >d_th: # if the robot is well aligned with the token, we go forward
			print("Ah, here we are!.")
			drive(15, 0.5)   	   
		elif dist <d_th: 
			drive(0,1)
			print("Found it!")
			R.grab() # if we are close to the token, we grab it.
			print("Gotcha!") 
			
			#turn(20,2)
			#drive(20,2)
			#R.release()
			#drive(-20,2)
			turn(-10,1.3)
			while target_distance-dist > 0:
				print(target_distance-dist)
				dist, rot_y, token_id = find_token()
				drive(10,0.5)
			R.release()
			
			'''
			
	
	
		
	
	
	
	
	#while 1:
	#    pass
	    
	    
	    
main()	    
