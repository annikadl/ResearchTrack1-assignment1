# ResearchTrack1-assignment1
This is the first assignment for the Research Track 1 exam for the Robotics Engineering Master's degree at the University of Genoa.


## Simulator
The Simulator used during the course is a 2D simulator of a moving Robot and stationary tokens on a playground. The robot can detect, grab and release the tokens.

To know all about the simulator, who developed it and how to download it, you're invited to look at `ReadMe.md` in the `assignment23` branch: this is the professor ReadMe file that provides a fully detailed description of the environment.

Given that, to **run this code**:
* clone the repository
* move into the `assignment23` branch with the line command `git checkout assignment23` 
* run the program going into `robot-sim` folder and using `run.py` with the line command `python2 run.py assignment.py`
At this point the simulator has started, the program is running and the robot is moving.

## The assignment
The assignment requires writing a Python node that controls the robot to **put all the golden boxes together**. 

### Description of the initial condition and assumptions
The initial condition of the simulation, not considering the code to group all tokens, can be described as follows:
* the robot occupies the top-left part of the playground and it is directed to its centre.
* the tokens are:
  * six.
  * all gold (there could have been silver tokens).
  * positioned forming a circle of a certain radius around the centre of the playground.

In order to make the code as general as possible, the only assumption made is about the number of singular rotations the robot needs to perform a full rotation. In particular, 12 rotations of intensity 20 for 0.5 seconds each are necessary.
Also, no obstacle-avoidance function was implemented.

### How to accomplish the task
To accomplish the task, the implemented workflow is:
1. check if the robot sees at least two tokens; otherwise the task would be already accomplished.
2. choose the target token and where to place it, this is the area around which the other tokens will be placed.
3. take the target token and place it properly.
4. look for all the other tokens to move and save their offset in a list.
5. one by one, choosing a token (from the first seen to the last), take it with and bring it to the target one. Once the token is correctly placed near the target one, its offset is removed from the list of still-to-be-placed tokens.
6. when the list which contains the remaining token to move is empty, the tokens are grouped and the task is accomplished.  

### Functions
To write a program performing as seen in the last section, some functions were implemented. Three of them have been already used in previous exercises with the same simulator, but with different initial configurations; the others were implemented ad hoc to fulfil the assignment.

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

To go more into details:
* `center_group`: the idea this function implements is to find a point in the playground that is near each token so that the robot must not cross the whole playground for each token. It is computed by looking for the nearest token and the farthest token, and placing the first one (chosen to be the target token) halfway through the second one. In order to reduce the number and the length of displacements, the target token is chosen to be the nearest one, that is brought to the target point.
* `go_take_token`: this function discriminates between two types of tokens:
  * the first token, the one that is placed according to function center_group and that, once placed, becomes the target token. In this case, the integer kind_of_token is equal to 1
  * the generic token that must be grabbed and brought to the target one. In this case, the integer kind_of_token is equal to 3.
* `place_first_token` complementary function to go_take_token in case of generic tokens. It is used to bring the token just grabbed to the target one, to place it there.

	

### Pseudocode
The written program obtained implementing the workflow idea already described works as the following pseudocode block shows.

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
        Decrement d

        Print the number of remaining tokens in id_token_list

    # Step 6: Task accomplished
    Print("TASK ACCOMPLISHED!")
    Exit the program
```






### Further improvements
* obtain full rotation automatically
* obstacle avoidance function


Function list:
##### TODO: 
* talk about global values
* maybe insert some code blocks
* provide pseudo code or diagrams
* IMPORTANT: explain why tokens where grouped in the middle of the playground and if the solution is sufficiently general


## TODO CODE:
* 




