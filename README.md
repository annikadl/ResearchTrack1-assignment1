# ResearchTrack1-assignment1
This is the first assignment for the Research Track 1 exam for the Robotics Engineering Master's degree at the University of Genoa.


## Simulator
To know all about the simulator, who developed it, how to download it and all the base primitives you're invited to look at ReadMe.md in the `assignment23` branch. 
Given that, to **run** this code:
* clone the repository
* move into the `assignment23` branch with the line command `git checkout assignment23` 
* run the program with the line command `python2 run.py assignment.py`
At this point the simulator has started, the program is running and the robot is moving.

## The assignment
The assignment requires writing a Python node that controls the robot to **put all the golden boxes together**. 

### Description of the initial condition

### Assumptions



No obstacle avoidance function was implemented

### How to accomplish the task



To accomplish it, the idea is to implement the following pseudo-code.
```
{
  look for the nearest token

  make the robot reach and grab it

  calculate where to release it as:
    look for the farthest token
    compute the mean distance between the farthest and the nearest token
    go forward in the direction of the farthest token and release the grabbed halfway

  use the just-released token as the target to group them all

  for all the other tokens:
    look for the remaining tokens
    chose one, preferably the nearest but the target one
    reach it and grab it
    move to the target token
    release the token

  when all the tokens are grouped, exit the program    

}
```
As the willing was to make the

### Functions

#### Already implemented functions
Given functions implemented:
* `drive`: is a function that allows the robot to move in the arena. It takes two parameters _speed_ and _seconds_ that indicate how fast the robot must go and for how long.
* `turn`: is a function to set the angular velocity of the robot. As the _drive_ function takes _speed_ and _seconds_ as parameters.
`find_token`:

#### Brand-new implemented functions
Brand-new functions implemented to accomplish the assignment:
* `center_group`
* `go_take_token`
* `place_first_token`
* `bring_token_to_target`


Function list:
##### TODO: 
* provide a brief explanation of what it does
* provide a list of the parameters it takes
* provide a list of the eventual return values
* talk about global functions
* explain how to run the code
* explain how the program is expected to behaviour
* maybe insert some code blocks
* provide pseudo code or diagrams
* add comments in the code





