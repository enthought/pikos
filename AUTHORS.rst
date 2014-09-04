Simon Jagoe and Ioannis Tziakos are the main developers and maintainers of pikos

Historical notes:
-----------------

Pikos started as a tool to help investigate *out of memory errors* on long running 
applications. At that time there where very few tools (even less working on windows) 
that could offer deterministic memory allocation/deallocation of a python process 
in a resonable amount of time. In fact still now most of the tools are aimed at 
finding memory leaks and work on memory snapshots or give memory usage at time 
intervals (average memory usage). These tools are not usefull when looking for 
temporary allocations/dealloations and distingusing (in alien code) code snipets 
that could easily lead into *out of memory errors*. After setting up the goals and 
we started working into formalizing our ideas and thus pikos was *born*.
