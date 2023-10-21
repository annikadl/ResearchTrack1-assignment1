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
	
def go_take_first_token(dist, rot_y, token_id1):
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
			drive(-15, 0.5)	
		dist, rot_y, token_id2 = find_token()
		if token_id2 == token_id2:
			token_id1 = token_id2
		else: 
			print('i dont see the token ', token_id1, ' anymore')
			print('now i see token ', token_id2)
		
	#TODO: actually count rotation instead of performing rotations without check	
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
		
	
	
def go_take_token_i(dist, rot_y, token_id,id_token_list):
	notgrabbed = 0
	found = 0
	found_id = 0
	counter_left_rotation = 0
	counter_right_rotation = 0
	counter = 0
		
	# print(first_token_placed)
	while found == 0:
			for m in R.see():
				# counter = counter +1
				if m.info.offset == token_id:
					dist = m.dist
					rot_y = m.rot_y
					found = 1
					print('dist dal prossimo token: ',dist)
					found_id = token_id
			if found_id != token_id:
				turn(-25,0.5)
				# counter = 0 
	
	#if counter > 1:
	#	turn(20,2)
	#	drive(30,3)
	#	turn(-20,3) 
	
	while notgrabbed == 0: # and first_token_placed == 1:
		# when found once, is always in R.see()
		for m in R.see():
				if m.info.offset == token_id:
					dist = m.dist
					rot_y = m.rot_y
					print('dist dal prossimo token: ',dist)
			
		if rot_y < -a_th and dist >d_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-10, 0.1)
			drive(15,0.5)
			counter_left_rotation = counter_left_rotation +1
		elif rot_y > a_th and dist >d_th:
			print("Right a bit...")
			turn(+10, 0.1)	
			drive(15,0.5) 
			counter_right_rotation = counter_right_rotation +1
		elif -a_th<= rot_y <= a_th and dist >d_th: # if the robot is well aligned with the token, we go forward
			print("Ah, here we are!.")
			drive(15, 0.5)   	   
		elif dist <d_th: # and token_id in id_token_list:
			drive(0,1)
			print("Found it!")
			R.grab() # if we are close to the token, we grab it.
			print("Gotcha!") 
			notgrabbed = 1;	
			
	# perform a rotation that brings e back to the inizial rotation
	# assunption: the robot takes the token turning its back from the center
	drive(-20,1)
	turn(-20,2.5)
	'''
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
		counter_right_rotation = counter_right_rotation -1 '''
	
	
def place_first_token(id_max_dist_token,target_distance):
	# token already grabbed
	first_token_placed = 0;
	markers = R.see()
	# a_th2 = 1.10e-14

	for m in markers:
			if m.info.offset != id_max_dist_token:
				markers.remove(m)
		
	# assumption: i have already grabbed the token	
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
    		
    		# print(rot_y)
    		# print(a_th2)
    		    			
    		'''
    		TRIED TO PLACE IT BETTER
    		if rot_y < -a_th2 and dist < (target_distance/2): # if the robot is not well aligned with the token, we move it on the left or on the right
			# print("Left a bit...")
			turn(-10, 0.1)
			drive(15, 0.5) 
		elif rot_y > a_th2 and dist < (target_distance/2):
			# print("Right a bit...")
			turn(+10, 0.1)
			drive(15, 0.5) 	
		#elif - a_th2<= rot_y <= a_th2 and dist < (target_distance/2):
		'''
		
		if dist < (target_distance/2): # if the robot is well aligned with the token, we go forward
			#print("Ah, here we are!.")
			drive(15, 0.5)		
		elif dist > (target_distance/2):
			R.release()
			first_token_placed = 1 
			print("First token released.")
			drive(-10,1)
			print(target_distance/2)   	
			print(dist)	
	return first_token_placed	
	
def bring_token_to_target(token_id, id_min_dist_token):
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
	# counter = 0
	
	while found == 0:
			for m in R.see():
				# counter = counter +1
				if m.info.offset == id_min_dist_token:
					dist = m.dist
					rot_y = m.rot_y
					found_id = token_id
					print('dist dal target token: ',dist)
					found = 1
			if found_id != id_min_dist_token:
				turn(-25,0.5)
				# counter = 0
	
	''' if counter > 1:
		turn(20,2)
		drive(30,3)
		turn(-20,3) '''
	
	while token_placed == 0:
		for m in R.see():
			if m.info.offset == id_min_dist_token:
				dist = m.dist
				rot_y = m.rot_y
				print('update dist')
				print(dist)
		
		if rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-10, 0.1)
			drive(15,0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(+10, 0.1)	
			drive(15,0.5) 
		elif -a_th<= rot_y <= a_th and dist > d_target_token: # if the robot is well aligned with the token, we go forward
			print("Ah, here we are!.")
			drive(15, 0.5)   	   
		elif -a_th<= rot_y <= a_th and dist < d_target_token: # and token_id in id_token_list:
			drive(0,1)
			R.release() # if we are close to the target token, we release it.
			print("Done") 
			drive(-10,1)
			token_placed = 1	
	
	drive(-10,2)
	turn(20,2)	
	
	
	

def main():

	# first_token_placed = 0
	markers = R.see()
	dist, rot_y, token_id = find_token()
	while dist == -1:  # we look for markers
	     print("I don't see any token!!")
	     drive(10,0.5)
	     turn(10,0.5)
	     dist, rot_y, token_id = find_token()

	
	print ("I can see", len(markers), "markers:")
	
	target_distance, id_max_dist_token, id_min_dist_token = center_group(markers)

	#for m in markers:	
	#	print (" - Token {0} is {1} metres away".format( m.info.offset, m.dist )

	print('the distance between nearest and farest token is: ', target_distance)
	print('offset of min_dist_token is: ',id_min_dist_token )
	print('offset of max_dist_token is: ',id_max_dist_token)
	
	# go take the first token
	go_take_first_token(dist, rot_y, token_id)
	
	# go towards the max dist token and stop half way
	first_token_placed = place_first_token(id_max_dist_token,target_distance)
	
	print('first token placed: ', first_token_placed)
	
	# perfom a full rotation to see each token
	i = 0
	counter = 0
	# remaining_token_dict = {}
	dist_token_list = []
	rot_token_list = []
	id_token_list = []
	# 12 partial rotation almost correspond to a 360 rotation
	while i  < 12:
		for m in R.see():
			if m.info.offset not in id_token_list:
				# index out of bound (idk)
				#dist_token_list[counter] = m.dist
				#rot_token_list[counter] = m.rot_y
				#id_token_list[counter] = m.info.offset
				#counter = counter + 1
				#print(counter)
				id_token_list.append(m.info.offset) 
				dist_token_list.append(m.dist) 
				rot_token_list.append(m.rot_y)
				counter = counter +1
							
		i = i+1
		turn(-20,0.5)
		# sometimes it misses token 10
		
	#print(dist_token_list)
	#print(rot_token_list)
	# print(id_token_list)
	
	
	#remaining_token = [dist_token_list, rot_token_list, id_token_list]
	#print(remaining_token)
	
	''' attempt with dictionary
	while i  < 6:
		for m in R.see():
			if m.info.offset not in remaining_token_dict:
				remaining_token_dict[counter] = {
					'dist': m.dist,
					'rot_y': m.rot_y,
					'token_id': m.info.offset
					}
			print(remaining_token_dict[counter])			
		i = 1+1
		counter = counter + 1
		turn(-20,1)
		# sometimes it misses token 10 '''
	
	
	# remove the id_min_dist token that was placed in the middle
	d = 0
	while d < counter:
		if id_token_list[d] == id_min_dist_token:
			dist_token_list.pop(d)
			rot_token_list.pop(d)
			id_token_list.pop(d)
			counter -= 1
		d += 1
		
			
	
	# print('the list of token to move is composed of: ', len(id_token_list))
	# print('elements that are: ', id_token_list)
	
	
	# TODO: find a smarter way
	# to not go into the first token
	drive(-10,3)
	turn(10,2)
	drive(15,3)
	turn(-10,1)
	
	d = 0
	while d < counter:
		print('token to move: ', id_token_list)
		dist = dist_token_list[d]
		rot_y = rot_token_list[d]
		token_id = id_token_list[d]
		print('next token to take: ', token_id)
		go_take_token_i(dist,rot_y,token_id,id_token_list)
		print('here')
		bring_token_to_target(token_id, id_min_dist_token)
		print('here2')
		dist_token_list.pop(d)
		rot_token_list.pop(d)
		id_token_list.pop(d)
		# remove element d? need to decrease d. yes because i pass id_token_list to go take token i
		counter = counter -1
		print('number of remaining token: ', counter)
		d = d -1
		
		
	
	'''
	for j in id_token_list:
	# TODO: i need to skip the first element because it is the target
		dist = dist_token_list[j]
		rot_y = rot_token_list[j]
		token_id = id_token_list[j]	
		go_take_token_i(dist, rot_y, token_id,first_token_placed,id_token_list)
		'''
		
	
	

	# TODO: implement how to reach target distance here to call just a function iteratively on each token. by now it works, so i'll do it later
	# modify go_take_token
	
	
	
	
	
	
	 
	
	
	
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
