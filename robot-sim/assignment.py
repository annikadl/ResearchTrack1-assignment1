from __future__ import print_function

import time
from sr.robot import *

R = Robot()
""" instance of the class Robot"""

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""
d_target_token = 0.6

target_id = 0	


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
	return -1, -1,0
    else:
   	return dist, rot_y, token_id
   			   	

		
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
			
	if id_min_dist_token != id_max_dist_token:	
		# target_distance from the min_dist_token
		target_distance = (min_dist+max_dist)/2
	# if the robot sees just a token, the min distance token corresponds to the target
	elif id_min_dist_token == id_max_dist_token:
		target_distance = min_dist
	
	return target_distance, id_max_dist_token, id_min_dist_token
	
	
	
''' 
	first token -> kind_of_token = 1
    	generic token -> kind_of_token = 3 '''

def go_take_token(token_id,kind_of_token):
	# go take first token: 1
	notgrabbed = 0
	# go take token i: 3
	counter_left_rotation = 0
	counter_right_rotation = 0
	found = 0
	found_id = 0
	found_3 = 0
	
	
	while found == 0:
		for m in R.see():
			if m.info.offset == token_id:
				dist = m.dist
				rot_y = m.rot_y
				found = 1
				found_id = token_id
				print('found_id: ', found_id)
				print('dist dal prossimo token: ',dist)
		if found_id != token_id:
			turn(-25,0.5)
	
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
		elif -a_th<= rot_y <= a_th and dist >d_th: # if the robot is well aligned ith the token, we go forward
			# print("Ah, here we are!.")
			drive(15, 0.5)   	   
		elif dist <d_th:
			drive(0,1)
			# print("Found it!")
			R.grab() # if we are close to the token, we grab it.
			print("Gotcha!") 
			drive(-15, 0.5)
			notgrabbed = 1
		while found_3 == 0:	
			dist, rot_y, token_id2 = find_token()
			if token_id2 == token_id:
				token_id = token_id2
				found_3 = 1
			else: 
				# print('i dont see the token ', token_id, ' anymore')
				# print('now i see token ', token_id2)
				drive(-15, 0.5)
		found_3 = 0
		
	if kind_of_token == 1:
	# perform a rotation that brings e back to the inizial rotation
		while counter_left_rotation != 0:
			# for each left rot,i do a right rot
			# print("Right a bit...")
			turn(+10, 0.1)	
			counter_left_rotation = counter_left_rotation-1
		
		while counter_right_rotation != 0:
			# for each right rot,i do a left rot
			# print("Left a bit...")
			turn(-10, 0.1)	
			counter_right_rotation = counter_right_rotation -1
			
	if kind_of_token == 3:
		# perform a rotation that brings e back to the inizial rotation
		# assunption: the robot takes the token turning its back from the center
		drive(-20,1)
		turn(-20,2.5)
		

def place_first_token(id_max_dist_token,target_distance):
	first_token_placed = 0;
	markers = R.see()

	while first_token_placed == 0:
		markers = R.see()
		for m in markers:
			if m.info.offset != id_max_dist_token:
				markers.remove(m)
		
		# list of one element
		for m in markers:
    			dist = m.dist
    			rot_y = m.rot_y
    			token_id = m.info.offset
		
		if dist < (target_distance/2): # if the robot is well aligned with the token, we go forward
			#print("Ah, here we are!.")
			drive(15, 0.5)		
		elif dist > (target_distance/2):
			R.release()
			first_token_placed = 1 
			print("First token released.")
			drive(-10,1)
			#print(target_distance/2)   	
			#print(dist)		

	
def bring_token_to_target(token_id):
	''' 
	cerco in R.see() il token target
	mi calcolo la distanza dal token target
	finche non sono abbastanza vicino vado avanti
	quando lo rilascio rimuovo l'elemento da tutti e tre i vettori (nel main?)
	faccio retro e poi viene richiamata go_take_token_i nel ciclo nel main	
	'''
	token_placed = 0
	found = 0
	found_id = 0
	
	while found == 0:
			for m in R.see():
				if m.info.offset == target_id:
					dist = m.dist
					rot_y = m.rot_y
					found_id = target_id
					# print('found id: ', found_id)
					print('dist from target token: ',dist)
					found = 1
			if found_id != target_id:
				turn(-25,0.5)
				drive(0,1)
				# print('i dont see target token')
				
	
	while token_placed == 0:
		for m in R.see():
			if m.info.offset == target_id:
				dist = m.dist
				rot_y = m.rot_y
				# print('update dist: ',dist)
		if rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			# print("Left a bit...")
			turn(-10, 0.1)
			drive(15,0.5)
		elif rot_y > a_th:
			# print("Right a bit...")
			turn(+10, 0.1)	
			drive(15,0.5) 
		elif -a_th<= rot_y <= a_th and dist > d_target_token: # if the robot is well aligned with the token, we go forward
			# print("Ah, here we are!.")
			drive(15, 0.5)   	   
		elif -a_th<= rot_y <= a_th and dist < d_target_token: # and token_id in id_token_list:
			drive(0,1)
			R.release() # if we are close to the target token, we release it.
			print("Token released") 
			drive(-10,1)
			token_placed = 1	
	
	drive(-10,2)
	turn(20,2)	
	
	
	

def main():

	markers = R.see()
	dist, rot_y, token_id = find_token()
	while dist == -1:  # we look for markers
	     print("I don't see any token!!")
	     drive(10,0.5)
	     turn(10,0.5)
	     dist, rot_y, token_id = find_token()

	target_distance, id_max_dist_token, id_min_dist_token = center_group(markers)
	
	global target_id
	target_id = id_min_dist_token

	print('offset of min_dist_token is: ',id_min_dist_token )
	
	# go take the first token
	kind_of_token = 1
	go_take_token(token_id,kind_of_token)
	
	# go towards the max dist token and stop half way to place the target token
	place_first_token(id_max_dist_token, target_distance)
	
	
	turn(-20,3)
	drive(0,1)
	
	# perfom a full rotation to see each token
	i = 0
	counter = 0
	
	# initialise a list containing the id of each token in the playground. This is going to be useful when the robot look for a token to move to the target one. 	
	id_token_list = []
	
	# 12 partial rotation almost correspond to a 360 rotation with this speed and time. It may be better to compute it not empirically
	while i  < 12:
		for m in R.see():
			if m.info.offset not in id_token_list:
				id_token_list.append(m.info.offset) 
				counter = counter +1			
		i = i+1
		turn(-20,0.5)
	
	
	# remove from the list of tokens to move the id_min_dist token that was placed in the middle of the playground
	d = 0
	while d < counter:
		if id_token_list[d] == target_id:
			id_token_list.pop(d)
			counter -= 1
		d += 1
		
	
	d = 0
	# now the robot moves the other tokens to the target one
	kind_of_token = 3
	while len(id_token_list) > 0:
		print('token to move: ', id_token_list)
		token_id = id_token_list[d]
		print('next token to take: ', token_id)
		go_take_token(token_id,kind_of_token)
		print('here')
		bring_token_to_target(token_id)

		''' remove placed token '''
		id_token_list.pop(d)
		
		# d is always zero and takes always the first element
		# since token are removed, no need to change cell
		print('number of remaining token: ', len(id_token_list))
		
	print('TASK ACCOMPLISHED!.')
	exit()
   
	    
main()	    
