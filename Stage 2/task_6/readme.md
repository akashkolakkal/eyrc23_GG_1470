# Team ID = 1470

model weights link: https://drive.google.com/file/d/1Dt_SLWlsqcoWF8Q6wuvrJSW94iJJKb2_/view?usp=sharing

videos:

Task 6 Original: https://youtu.be/LVYrfxTNusQ

Task 6 Bonus: https://youtu.be/7uLREmTS_Yw

Team Members: Parth Jain, Akash Kolakkal, Anikesh Kulal, Keshav Jha

----

The entry point of our code is task_6.py.
First, we are using multiprocessing to create a kill switch for the server and running the actual code as a new process. After that, we are running three threads; one for connecting with the ESP via socket; second one for handling any inputs from the ESP board; and the third to proceed towards the next task (Displaying live feed and mark bounding boxes from file task_4a.py) and live tracking.

The image classification is done using transfer learning, and fine tuning pre-trained EfficientNetB7 model using a dataset which has more than 2,500 images collected from public sources on the internet.

model weight link: https://drive.google.com/file/d/1Dt_SLWlsqcoWF8Q6wuvrJSW94iJJKb2_/view?usp=sharing

The model weights file is present in the model_weights subdirectory

On the third thread, when the events are displayed and marked, we are using a variant of Dijkstra's algorithm to find minimum path between any two nodes using adjacency list, which is a 5X5 list where each element contains weigths for it's four directions. So after calculating the order of events that needs to be visited according to the priotities, we are using our pathfinder algorithm to generate the most suitable path for the bot to traverse.
We check all possible permutations in case of multiple events, to find the path with minimum cost.
Once the path is calculated, we are processing it to morph it relative to the bot's perspective and sending the signal over.

Once all this is done, and the bot recieves it's first set of instructions (which look like: "SFFRR...E"). Once recieved, it starts following the black lines until it detects a node and perform the next instruction in the instructions that were sent over before from the server.

All the while, the server keeps checking if the bot has reached the events in the did_reach() function. And if so, sends a '1' indicating that event has arrived. The bot stops and beeps the buzzer for one second and carries on with the rest of the instructions.

Live tracking is acheived by first cheking the angle of the Bot's aruco marker, and calculating point that is ahead of the bot (referred to as forward in the code) and behind it(which is reffered to as backward in the code). For this, we have added the corresponding pixel coordinates from the frame to the lat_lon.csv. Once that is done, we are using the ratio obtained from the bot's current position with respect to these two markers(forward and backward) to calculate the latitude and longitude of the bot using section formula. The calculated values are written in task_4b.py and displayed on QGIS in real time.

After traversing the path, it returns back to its start point and beeps the buzzer for five seconds; which marks the end of the run.

----

The .ino file for ESP 32 is present in the esp_code folder.

nodes_example.png can be used to understand the virtual nodes, that is referred multiple times in the code.