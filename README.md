# taupy

## Dependencies
 - [https://github.com/sympy/sympy](sympy), for its Boolean algebra
 - [https://github.com/tulip-control/dd](dd), to create BDDs to check satisfiability as well as listing and counting their number
 - [https://git.skewed.de/count0/graph-tool](graph_tool), for graph analysis and plotting

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
