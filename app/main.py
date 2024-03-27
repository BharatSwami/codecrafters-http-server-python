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
            data_list = data.split("\n")[0].split(" ")
            print(data_list)
            if "echo/" in data_list[1]:
                random_string = data_list[1].split("echo")[-1]
                print(random_string)
                response_massage = f"HTTP/1.1 200 OK\r\n\r\nContent-Type: text/plain\r\n\r\nContent-Length: {len(random_string)-1}r\n\r\n{random_string[1:]}r\n\r\n"
                print(response_massage)
                conn.sendall(response_massage.encode())
            elif data_list[1] == "/":
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            else:
                conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    
    
    server_socket.close()

if __name__ == "__main__":
    main()
