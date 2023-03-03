Simulations
***********

Debates and Positions are static objects: they describe arguments and an agent's
belief system at one point in time. Dynamical aspects of debates and belief
systems can be studied in Simulations.

In agent-based models built on the theory of dialectical structures, the 
simulated world consists of a sentence pool and arguments made from these 
sentences. Agents have a multi-dimensional belief system in terms of Positions. 
The Simulations progress by introducing arguments, possibly according to an 
argumentation strategy assigned to agents. Arguments can be introduced in a 
random fashion to debates. Those have minimal requirements and can be used even
in Simulations that do not contain any agents. Purposeful argumentation
strategies select premises and conclusions in light of agents' belief systems.
For these arguments, at least two agents are drawn from the population. 
After argument introduction, the entire population responds by checking their 
belief system in light of the new argument and revise their beliefs if 
necessary. This process continues until a termination condition is reached. If 
requested by the user, the sentence pool is also occassionaly extended.
The simulation terminates when the desired inferential density is reached or the desired number of arguments has been introduced.

.. toctree::

   populations
   simulations
   update
   experiments
   evaluation
