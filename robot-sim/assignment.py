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
""" float: Threshold for the control of the linear distance from the target token"""

target_id = 0	
""" int: id of target token initialised to 0, then it is updated"""


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
	- dist (float): distance of the closest token (-1 if no token is detected)
	- rot_y (float): angle between the robot and the token (-1 if no token is 	detected)
	- token_id (int): offset of the found token
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
	"""
	Function to compute where to place the first token, around which the others will be brought. The idea is to find a point in the playground that is near to each token, so that the robot must not cross the whole playground for each token.
	
	It is computed looking for the nearest token and the farthest token, and placing the first one (choosen to be the target token) half way through the second one. 
	
	In order to reduce the number and the lenght of displacements, the target token is choosen to be the nearest one, that is brought to the target point.
	
	returns:
	- target_distance (float): the distance from where to place the target token. It is computed from the nearest token 
	- id_max_dist_token (int): offset of the farthest token
	- id_min_dist_token (int): offset of the nearest token
	
	"""
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
				
	# target_distance from the min_dist_token
	target_distance = (min_dist+max_dist)/2

	
	return target_distance, id_max_dist_token, id_min_dist_token
	


def go_take_token(token_id,kind_of_token):
	"""
	Function to move in the direction of a specific token to reach and grab it.
	This function discriminates between two types of token:
	- the first token, the one that is placed according to function center_group and that, once placed, becomes the target token. In this case the integer kind_of_token is equal to 1
	- the generic token that must be grabbed and brought to the target one. In this case the integer kind_of_token is equal to 3.
	
	To resume:	
	first token -> kind_of_token = 1
    	generic token -> kind_of_token = 3 
    	
    	This function does not have return values
    	
    	
    	"""    	
	
	notgrabbed = 0
	
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
				print('dist from next token: ',dist)
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
	"""
	This function is used to place the first token after it has been grabbed. It is very similar to function go_take_token, but the distance check is made using target_distance parameter instead of the thershold d_th. 
	
	This function does not have return values.
	
	"""

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
			drive(15, 0.5)		
		elif dist > (target_distance/2):
			R.release()
			first_token_placed = 1 
			print("First token released.")
			drive(-10,1)		

	
def bring_token_to_target(token_id):
	"""
	This function is complementar to go_take_token in case of generic tokens. It is used to bring the token just grabbed to the target one, to place it there.
	
	This function does not have return values.
	
	"""
	
	token_placed = 0
	found = 0
	found_id = 0
	
	# looking for the token to move
	while found == 0:
			for m in R.see():
				if m.info.offset == target_id:
					dist = m.dist
					rot_y = m.rot_y
					found_id = target_id
					print('dist from target token: ',dist)
					found = 1
			if found_id != target_id:
				turn(-25,0.5)
				drive(0,1)
				
	
	# until the token is not correctly placed near the target one
	while token_placed == 0:
		for m in R.see():
			if m.info.offset == target_id:
				dist = m.dist
				rot_y = m.rot_y
		if rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			turn(-10, 0.1)
			drive(15,0.5)
		elif rot_y > a_th:
			turn(+10, 0.1)	
			drive(15,0.5) 
		elif -a_th<= rot_y <= a_th and dist > d_target_token: # if the robot is well aligned with the token, we go forward
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
	"""
	This is the main function in which all the other function are called and the idea of how to accomplish the task is implemented.
	
	The workflow is the following:
	1 - check if the robot sees at least two tokens
	2 - choose the target token and where to place it, it is the area around which the other tokens will be placed calling function center_group
	3 - take the target token and place it with functions go_take_token and place_first_token
	4 - look for all the other tokens to move and save their offset in a list called id_token_list
	5 - one by one, choosing a token (from the first seen to the last), go taking it with function go_take_token and bringing them to the target one with bring_token_to_target. Once the token is correctly placed near the target one, its offset is removed from id_token_list
	6 - when the id_token_list, which constains the remaining token to move, is empty, the task is accomplished.  
	
	"""
	### 1 - check if the robot sees at least two tokens
	markers = R.see()
	dist, rot_y, token_id = find_token()
	while dist == -1:  # we look for markers
	     print("I don't see any token!!")
	     drive(10,0.5)
	     turn(10,0.5)
	     dist, rot_y, token_id = find_token()
	     
	     
	# if the robot sees just one token there are two possibilities:
	# scenario 1 - it does not see the others, so it is useful to rotate to see them all
	
	# 12 partial rotation almost correspond to a 360 rotation with this speed and time. It may be better to compute it not empirically
	i = 0
	if len(markers) == 1:
		while i < 12 and len(markers) < 2:
			drive(10,0.5)
		     	turn(20,0.5)
		     	i = i + 1
		     	dist, rot_y, token_id = find_token()
		     	
	# scenario 2 - there is just one token
	if len(markers) == 1 and i == 12:
		# the last cycle never stopped with len(markers) > 1
		print("There is just a token so the task is already accomplished")
		exit();
		
	### 2 - choose the target token and where to place it, it is the area around which the other tokens will be placed calling function center_group

	target_distance, id_max_dist_token, id_min_dist_token = center_group(markers)
	
	global target_id
	target_id = id_min_dist_token

	print('offset of target token is: ',target_id)
	
	### 3 - take the target token and place it with functions go_take_token and place_first_token
	
	# go take the first token
	kind_of_token = 1
	go_take_token(token_id,kind_of_token)
	
	# go towards the max dist token and stop half way to place the target token
	place_first_token(id_max_dist_token, target_distance)
	
	# perform a rotation to get lookinf from the direction it came.
	turn(-20,3)
	drive(0,1)
	
	### 4 - look for all the other tokens to move and save their offset in a list called id_token_list
	
	# From this new position it is possible to start scanning the whole area to see all the tokens, perfoming a full rotation
	i = 0
	counter = 0
	
	# initialise a list containing the offset of each token in the playground. This is going to be useful when the robot looks for a token to move to the target one. 	
	id_token_list = []
	
	# 12 partial rotation almost correspond to a 360 rotation with this speed and time. It may be better to compute it not empirically
	while i  < 12:
		for m in R.see():
			if m.info.offset not in id_token_list:
				id_token_list.append(m.info.offset) 
				counter = counter +1			
		i = i+1
		turn(-20,0.5)
	
	
	# remove from the list of tokens to move the target token that was placed in the middle of the playground
	d = 0
	while d < counter:
		if id_token_list[d] == target_id:
			id_token_list.pop(d)
			counter -= 1
		d += 1
		
	
	### 5 - one by one, choosing a token (from the first seen to the last), go taking it with function go_take_token and bringing them to the target one with bring_token_to_target. Once the token is correctly placed near the target one, its offset is removed from id_token_list
	
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
	
	### 6 - when the id_token_list, which constains the remaining token to move, is empty, the task is accomplished. 
	# when id_token_list is empty the previous while condition is false
		
	print('TASK ACCOMPLISHED!.')
	exit()
   

# call to main function	    
main()	    
