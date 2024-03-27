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
            startline, host, UserAgent = data.split("\n")
            request_verb, request_target, http_version = startline.split(" ")
            if request_verb == "GET":
                response_massage = ""
                if "echo/" in request_target:
                    random_string = request_target.split("echo/")[-1]
                    #print(request_target)
                    response_massage = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(random_string)}\r\n\r\n{random_string}"
                    #print(response_massage)
                elif request_target == "/user-agent":
                    user_agent = UserAgent.split(" ")[-1]
                    response_massage = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}"
                elif request_target == "/":
                    response_massage = "HTTP/1.1 200 OK\r\n\r\n"
                else:
                    response_massage = "HTTP/1.1 404 Not Found\r\n\r\n"
            #
            conn.sendall(response_massage.encode())
    
    server_socket.close()

if __name__ == "__main__":
    main()
