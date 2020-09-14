# taupy

## Dependencies
 - [sympy](https://github.com/sympy/sympy), for its Boolean algebra
 - [dd](https://github.com/tulip-control/dd), to create BDDs to check satisfiability as well as listing and counting their number
 - [graph_tool](https://git.skewed.de/count0/graph-tool), for graph analysis and plotting

## Functional structure:

taupy
 - basic
   - core
     - Debate
     - Argument
   - positions
     - Position
 - analysis
   - agreement
   - mutual coherence
   - doj
   - inferential density
 - simulation
   - agreement
   - polarisation
   - argument introduction methods
   - belief updating rules
 - graphs
   - centrality/distance measures
   - visualisation
     - plot tau
     - plot sccp
