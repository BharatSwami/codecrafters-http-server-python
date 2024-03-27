# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client

    with conn:
        #print(f"connected by {addr}")
        while True:
            data = conn.recv(1024).decode()
            #print(data)
            if not data:
                break
            #startline, host, UserAgent = data.split("\n")
            data_list = data.split("\n")
            print(data_list)
            #request_verb, request_target, http_version = startline.split(" ")
            startline_list = data_list[0].split(" ")
            #if request_verb == "GET":
            response_massage = ""
            print(startline_list)
            #print(request_verb, request_target, http_version)
            if "echo/" in startline_list[1]:    #request_target:
                #random_string = request_target.split("echo/")[-1]
                random_string = startline_list[1].split("echo/")[-1]
                #print(request_target)
                response_massage = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}"
                #print(response_massage)
            elif startline_list[1] == "/user-agent":   #request_target == "/user-agent":
                #user_agent = UserAgent.split(" ")[-1]
                user_agent = data_list[2].split("/r")[0].split(" ")[-1]
                response_massage = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
            elif startline_list[1] == "/":   #request_target == "/":
                response_massage = "HTTP/1.1 200 OK\r\n\r\n"
            else:
                response_massage = "HTTP/1.1 404 Not Found\r\n\r\n"
            #
            conn.sendall(response_massage.encode())
    
        server_socket.close()

if __name__ == "__main__":
    main()
