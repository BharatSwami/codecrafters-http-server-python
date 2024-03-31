# Uncomment this to pass the first stage
import socket
import threading
import sys
import os
import argparse
from pathlib import Path
import pathlib


def handle_response(conn,addr,directory = " "):
    

    with conn:
        #print(f"connected by {addr}")
        while True:
            data = conn.recv(1024).decode()
            #print(data)
            if not data:
                break
            #startline, host, UserAgent = data.split("\n")
            data_list = data.split("\n")
            #print(data_list)
            #request_verb, request_target, http_version = startline.split(" ")
            startline_list = data_list[0].split(" ")
            if startline_list[0] == "GET":
                response_massage = ""
                #print(startline_list)
                #print(request_verb, request_target, http_version)
                if "echo/" in startline_list[1]:    #request_target:
                    #random_string = request_target.split("echo/")[-1]
                    random_string = startline_list[1].split("echo/")[-1]
                    #print(request_target)
                    response_massage = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}"
                    #print(response_massage)
                elif "files/" in startline_list[1]:
                    filename = startline_list[1].split("/")[-1]
                    print(filename)
                    absolute_filepath = os.path.join(directory,filename)
                    print(absolute_filepath)
                    
                    if os.path.exists(absolute_filepath) and os.path.isfile(absolute_filepath):
                            with open(absolute_filepath, 'rb') as f:
                                contents = f.read().decode()
                                #print(type(contents))

                                response_massage = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(contents)}\r\n\r\n" + contents
                                f.close()
                    else:  
                        response_massage = "HTTP/1.1 404 Not Found\r\n\r\n"
                        #
                        ###
                    

                    print(response_massage)
                elif startline_list[1] == "/user-agent":   #request_target == "/user-agent":
                    #user_agent = UserAgent.split(" ")[-1]
                    user_agent = data_list[2].split("\r")[0].split(" ")[-1]
                    print(user_agent)
                    response_massage = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
                elif startline_list[1] == "/":   #request_target == "/":
                    response_massage = "HTTP/1.1 200 OK\r\n\r\n"
                else:
                    response_massage = "HTTP/1.1 404 Not Found\r\n\r\n"
                #
                conn.send(response_massage.encode())
            elif startline_list[0] == "POST":
                if "files/" in startline_list[1]:
                    filename = startline_list[1].split("/")[-1]
                    print(filename)
                    absolute_filepath = os.path.join(directory,filename)
                    print(absolute_filepath)
                    
                    if os.path.exists(absolute_filepath) and os.path.isfile(absolute_filepath):
                            with open(absolute_filepath, 'w') as f:
                                print(data_list[-1])
                                f.write(data_list[-1])
                                #print(type(contents))

                                response_massage = f"HTTP/1.1 201 Created\r\n\r\n"
                                f.close()
                    else:  
                        response_massage = "HTTP/1.1 404 Not Found\r\n\r\n"
                conn.send(response_massage.encode())
            conn.close()
        
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    directory = ""
    if(len(sys.argv) == 3 and sys.argv[1] == "--directory"):
        directory = sys.argv[2]
    print(directory)
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        conn, addr = server_socket.accept() # wait for client
        threading.Thread(
            target=handle_response, args = [conn,addr,directory]
        ).start()
    

if __name__ == "__main__":
    main()
