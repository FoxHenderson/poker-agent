# poker-agent
Utilising reinforcement learning to create a heads up, no limit, Texas Hold 'em poker agent. 

Vector/png graphics for the cards were sourced from https://code.google.com/archive/p/vector-playing-cards/source/default/source

# Plan

Here are the issues that come to mind:
  - Even with heads up there is a tonne of game states (due to the nature of incomplete information), although there are ways to reduce the number of states (hand grouping, considering pre/post flop seperately. etc.)
  - It's no limit, due to the nature of raising this means that their is a large number of bet sizing options. Obviosuly we could group hands based on our P of winning / size bets based on this P, but again this would give the opponent information about the strength of our hand, so more research/ideas for this is required.
  - Training needs to be done on a large number of hands, if I were to leverage the university super computer it would need to be optimised/adapted for that? (apparently it hates python + it runs on linux so aspects may need to changed)
  - There is no objectively correct move/decision in a position like there is in chess/tic tac toe (games of perfect information), only decisions that are EV+. This can make it hard to train the AI, as the program could make a mistake and be successful as well as the opposite. So how will the reward mechanism function for the RL program? IDFK! (large sample size may be the best way of dealing with this, but then again this will make training a pain)
  - How adaptable should the program be to an opponent? If an opponent is playing exceedingly tight/loose, how quickly should our program adapt? How does it even adapt? 

Order of implementation
  - Implement game logic, this MUST be efficient (so training is not as arduous) and carefully planned, so could take time!!
  - Get the GUI working (probably using a tkinter wrapper because tkinter is annoying)
  - Basic RL bot (maybe some sort of minmanx + alpha-beta pruning basic implementation)
  - Look at counterfactual regret minimisation / research papers on the topic


  - Game logic
  - GUI
  - AI that does random moves