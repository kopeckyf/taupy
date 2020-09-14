# taupy

## Dependencies
 - https://github.com/sympy/sympy, for its Boolean algebra
 - https://github.com/tulip-control/dd, to create BDDs to check satisfiability as well as listing and counting their number
 - graph_tool, for graph analysis and plotting

Functional structure:

taupy
 - basic
   - core
     - Debate
     - Argument
   - positions
     - Position
 - analysis
   - agreement
   - centrality/distance
   - mutual coherence
   - doj
   - inferential density
 - simulation
   - agreement
   - polarisation
   - argument introduction methods
   - belief updating rules
 - visualisation
   - plot tau
   - plot sccp
