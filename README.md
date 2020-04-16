# Project-Diamond
Project Diamond Technical Requirements
I. Introduction
A. Project Diamond is a project that uses all of the skills learned throughout
the semester and incorporates them into a singular project. It is essentially
a loop that never ends in which each component sends data or a message
to another component. The component receives the data, converts it to
another format, then sends it to the next component. And it repeats this
process over and over again. This documents provides the technical
requirements for the Project Diamond.
II. Technical Requirements
A. I will be using Python and program via Linux and using the Vim text editor
to create, test and run the code. I will provide example code via links.
B. RabbitMQ Message Queue
1. It will listen to receive the JSON file from Pyro4
2. Create an SSL connection from RabbitMQ to a the socket
3. Send the JSON to the socket
4. Sends the activity log to the Mongo Database
5. Example:https://www.rabbitmq.com/tutorials/tutorial-one-python.ht
ml
C. Networking Sockets
1. Establishes a SSL connection from the RabbitMQ Message Queue
2. Listens to receive the JSON file from RabbitMQ Message Queue
3. Checks the hash payload value
4. Sends the JSON file to the Secure File Transfer Protocol
5. Sends the activity log to the Mongo Database
6. Example:https://www.tutorialspoint.com/python/python_networking.
html
D. SFTP Secure File Transfer Protocol - is used for securely exchanging
files via the Internet. Can be used with pysftp which is an easy to use sftp
module that utilizes paramiko and pycrypto.
1. Establishes a connection with the socket
2. Downloads the JSON file from the socket
3. Sends the JSON file to Pyro4 ORB
4. Sends the activity log to the Mongo Database
5. Example:http://www.pythonforbeginners.com/modules-in-python/pyt
hon-secure-ftp-module
E. Pyro4 ORB - is a library that allows the user to make applications in which
objects can talk to each other over the network
1. Establishes a connection with SFTP
2. Receives the JSON file from SFTP
3. Converts the JSON file via AES Encryption
4. Sends the JSON file to RabbitMQ Messaging Queue
5. Sends the activity log to the Mongo Database
6. Example: https://pythonhosted.org/Pyro4/intro.html
F. MongoDB - we are going to use Mongo to store all the logs of the program
such as error messages, time stamps, EventID etc for future references.
1. Example:https://docs.mongodb.com/getting-started/shell/import-dat
a/
G. Use Curl to grab an external JSON payload that will be passed around
1. Exampe: http://conqueringthecommandline.com/book/curl
