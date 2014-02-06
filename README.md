#Python Chat program#

A GUI chat program written in python 3. It is designed to not need a central server and so work very well on LANs that are not connected to the internet. One user starts the program in server mode, listening on a port of their choosing, and then other users connect to their machine. Each new user then acts as a host, allowing other people to connect to them. Encryption is done using Diffie-Hellman xor encrypting. Eventually some sort of real encryption will happen, but it is atleast semi-secured. It allows users to set nicknames, save chat history, and stores recent connections in addition to regular chatting.

