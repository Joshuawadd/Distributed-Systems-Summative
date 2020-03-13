# Distributed-Systems-Summative

## Set Up
To set up this project two pagages need to be installed. The first is the pyro4 package, and the second is the requests package. Both can be installed with "pip installl (package name)".

## Running the system
6 terminal windows are needed to run the system. In the first, the command "python -m Pyro4.naming" should be run in order to start the name server. Then in another winder, run "python client.py" to open the client, "python frontend.py" to open the front-end, and then in the other 3 run "python backend.py" to open the main back-end server and the 2 backup ones. 

Instructions should be shown on the command line for the client program for use of the system. If the main server is to be ended via the use of "CTRL-C", then one of the reserves will convert into the new main back-end server and continue the system. However if the main server is closed by exiting the terminal, this will not work.