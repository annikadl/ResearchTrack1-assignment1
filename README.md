# ResearchTrack1-assignment1
This is the first assignment for the Research Track 1 exam for the Robotics Engineering Master's degree at the University of Genoa.


## Simulator
The used environment is a 2D simulator of a moving robot. The robot can move in a fixed playground among stationary tokens (golden or silver), which can be detected, grabbed, moved and released by the robot.
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!(used during the course and to carry out this assignment)

To know more about the simulator, who developed it and how to download it, you are invited to take a look at the `ReadMe.md` file in the `assignment23` branch: this is the professor ReadMe file that provides a fully detailed description of the environment.

Given that, to **run this code**:
* clone the repository.
* move into the `assignment23` branch with the command `git checkout assignment23`.
* run the program by entering the `robot-sim` folder and using `run.py` with the command `python2 run.py assignment.py`.
At this point the simulator has started, the program is running and the robot is moving.

## The assignment
The assignment requires writing a Python node that controls the robot to **put all the boxes together**. 

### Description of the initial condition and assumptions
The initial condition of the simulation, before bringing the boxes together, can be described as follows:
* the robot appears on the top-left part of the playground and is directed to the centre.
* the tokens are:
  * six.
  * all gold (there could have been silver tokens, however only gold ones are present).
  * positioned forming a circle of a certain radius around the centre of the playground.

In order to make the code as general as possible, the only assumption made is about the number of partial rotations the robot needs to perform a full rotation.
Also, no obstacle-avoidance function was implemented.

### How to accomplish the task
To accomplish the task, the implemented workflow is:
1. check if the robot sees at least two tokens in the whole playground; otherwise, the task would be already accomplished.
2. choose the target token and where to place it, this is the area around which the other tokens will be placed.
3. take the target token and place it properly.
4. look at all the other tokens and save their identification offset in a list.
5. one by one take each token and bring it to the targeted one (see disclaimer). Once the token is correctly placed near the target, its offset is removed from the list of still-to-be-placed tokens.
6. when the list which contains the remaining boxes to move is empty, the tokens are grouped and the task is fulfilled.

##### DISCLAIMER
To improve the robot's performance, an operational choice was made, placing the target token as near as possible to all the others. Since the simulation starts with a circular disposition of boxes, the best path to make the robot move less is to bring the nearest token and place it at the centre of this disposition. Nonetheless, for the sake of generality, this position was not computed in an absolute manner (namely, if the disposition of tokens changes, the target's position does not). The location of the target coincides with the halfway between the position of both the nearest and the farthest tokens the robot can see; according to this reasoning, the target token will always be placed somewhere minimizing the displacement of the robot, excluding some specific cases ( e.g. all the tokens are already near but one). 

### Global variables
Some global variables, mostly constant and common to several functions were introduced.
* `a_th = 2.0`: used to check how many turns the robot must do to be aligned with its target.
* `d_th = 0.4`: used to check when the robot is sufficiently close to a token to grab it.
* `d_target_token = 0.6`: used to check when the robot is sufficiently close to the target token to release the one which it's holding.
* `target_id = 0`: once the target token is identified, this variable is updated and keeps the target's offset.

### Functions
To write a program capable of performing as explained in the "How to accomplish the task" section, some functions were implemented. Three of them have been already used in previous exercises with the same simulator, but with different initial configurations; the others were implemented ad hoc to fulfil the assignment.

#### Already implemented functions

| Function             | Description                                            | Taken Parameters                | Return Values         |
|----------------------|--------------------------------------------------------|---------------------------------|-----------------------|
| `drive(speed, seconds)` | Sets the linear velocity of the robot.             | `speed` (int), `seconds` (int) | None                  |
| `turn(speed, seconds)`  | Sets the angular velocity of the robot.            | `speed` (int), `seconds` (int) | None                  |
| `find_token()`        | Finds the closest token and its information.        | None                            | `dist` (float), `rot_y` (float), `token_id` (int) |


#### Ad hoc implemented functions

| Function             | Description                                            | Taken Parameters                | Return Values         |
|----------------------|--------------------------------------------------------|---------------------------------|-----------------------|
| `center_group(markers)` | Computes the placement area for tokens.           | `markers` (list of tokens)    | `target_distance` (float), `id_max_dist_token` (int), `id_min_dist_token` (int) |
| `go_take_token(token_id, kind_of_token)` | Moves to a specific token and grabs it. | `token_id` (int), `kind_of_token` (int) | None |
| `place_first_token(id_max_dist_token, target_distance)` | Places the first token in its position. | `id_max_dist_token` (int), `target_distance` (float) | None |
| `bring_token_to_target(token_id)` | Moves a token to the target token's position. | `token_id` (int) | None |
| `main()`             | Main function that controls the entire program.  | None                            | None |

To go more into detail:
* `center_group`: the idea this function implements is to find a point in the playground that is near each token so that the robot must not cross the whole playground. It is calculated by looking for the nearest and the furthest tokens and placing the first one (in order to reduce the number and the length of displacements, the target token is chosen to be the nearest one, that is brought to the target point) halfway through the second one.
* `go_take_token`: this function discriminates between two types of tokens:
  * the first token, the one that is placed according to function center_group and that, once placed, becomes the target token. In this case, the integer kind_of_token is equal to 1.
  * the generic token that must be grabbed and brought to the target one. In this case, the integer kind_of_token is equal to 3.
* `bring_token_to_target`: complementary function to go_take_token in case of generic tokens. It is used to bring the token just grabbed to the target one, to place it there.
* `place_first_token`: function used to place the first token at the distance previously calculated calling center_group function. It implements the same straight movement logic as the other functions. 


##### DISCLAIMER 2
Functions `go_take_token` and `bring_token_to_target` basically execute the same portion of code with few differences. This means that these two functions can easily be unified introducing one more value of `kind_of_token` to discriminate one more possible behaviour. However, this union will be performed despite clearness: having just a generic function, whose name can be changed into something such as `move`, does not make it easy to understand which kind of displacement the robot is performing (moving to take a token or bringing it to the targeted one). Furthermore, the clarity of the code decreases. In addition, the separation allows for writing a more intuitive main function.

To conclude, the choice of maintaining two separate functions is intentional for the aforementioned reasons.
	

### Pseudocode
The written program, obtained implementing the workflow idea already described, works as the following pseudocode block shows.

```
function main():
    Initialize robot and parameters
    Find the closest token (dist, rot_y, token_id)

    # Step 1: Look for tokens
    if dist == -1:
        # If no token is detected, perform initial scanning
        i = 0
        while i < 12 and no tokens are detected:
            Rotate the robot to scan the area
            Find the closest token (dist, rot_y, token_id)
            i = i + 1

        if still no tokens are detected:
            Print("No tokens found. Task cannot be accomplished.")
            Exit the program

    # Step 2: Choose the target token and where to place it
    Calculate target_distance, id_max_dist_token, and id_min_dist_token using center_group

    Set target_id to id_min_dist_token

    # Step 3: Take the target token and place it
    kind_of_token = 1
    Call go_take_token(token_id, kind_of_token)
    Call place_first_token(id_max_dist_token, target_distance)
    Perform a rotation to return to the initial orientation

    # Step 4: Find and list the offsets of all tokens
    Initialize id_token_list as an empty list
    Initialize counter as 0

    i = 0
    Perform a scan to find and list all tokens in id_token_list
    for each token found:
        Append the token's offset to id_token_list
        Increment counter

    # Remove the target token's offset from id_token_list
    d = 0
    while d < counter:
        if id_token_list[d] == target_id:
            Remove id_token_list[d]
            Decrement counter
        Increment d

    # Step 5: Move the other tokens to the target one
    kind_of_token = 3
    d = 0
    while id_token_list is not empty:
        token_id = id_token_list[d]
        Call go_take_token(token_id, kind_of_token)
        Call bring_token_to_target(token_id)

        # Remove the placed token from id_token_list
        Remove the first element from id_token_list

        Print the number of remaining tokens in id_token_list

    # Step 6: Task accomplished
    # When id_token_list is empty, tokens are correctly grouped
    Print("TASK ACCOMPLISHED!")
    Exit the program
```






### Further improvements
This simple code can be improved in different ways.

First of all, as is it possible to notice, the robot moves quite slowly: its speed can be incremented by paying attention to how fast it turns and stops in front of tokens, avoiding hurting them. In general, precision must be maintained.

Also, no obstacle avoidance function was implemented. To address the obstacle problem, the robot scans the tokens clockwise starting from its initial position; this behaviour allows it to collect all the tokens without crossing the playground's centre where the tokens lay. However, there is no guarantee that if the tokens were initially differently positioned, the program would work as efficiently as it does.

Furthermore, to make this program even more general, it is possible to compute automatically how much it takes to perform a full rotation. In this case, as said before, a full rotation was empirically obtained.

An additional feature, that can bring several improvements, regards where to place the target token. All the relative distances between tokens can be computed to choose and place the target more appropriately. This would help recognise lucky situations in which some tokens are already correctly placed. By now if the nearest token is the only one not well positioned, it still becomes the target and all the other tokens will be brought to it when it would be easier and cheaper to move it to the others.

To reduce the length of the program, functions `go_take_token` and `bring_token_to_target` can be unified, since they execute the same amount of code with just a few differences. The main reason why they are still separated, as said before, is to clarify better what the program does: using different functions, with different names, the overall behaviour should sound more clear. However, if upgraded the code may be required to be synthetic.


To conclude, even though clarity had the highest priority, several improvements are possible, both in terms of robot's behaviour and code efficiency.  However, the developed program fully accomplishes the assigned task. Furthermore, this Readme file provides a full description of program's behaviour, operational and structural choices. 
