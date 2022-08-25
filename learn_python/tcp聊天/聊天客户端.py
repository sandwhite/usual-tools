import socket

def main():
    # 1.创建套接字
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2.链接服务器
    #tcp_socket.connect_ex("ip", 7890)
    sever_ip = input("请输入需要链接的服务器ip:")
    sever_port = int(input("请输入需要链接的服务器的port："))
    sever_addr = (sever_ip, sever_port)
    tcp_socket.connect(sever_addr)

    # 3.发送数据/接收数据
    send_data = input("请输入需要发送的数据：")
    tcp_socket.send(send_data.encode("utf-8"))

    # 4.关闭套接字
    tcp_socket.close()


if __name__ == "__main__":
    main()