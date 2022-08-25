import socket


def send_msg(udp_socket):
    send_data = input("请输入：")
    dest_ip = input("请输入对方ip：")
    dest_port = int(input("请输入对方端口："))
    udp_socket.sendto(send_data.encode("utf-8"), (dest_ip, dest_port))


def recv_msg(udp_socket):
    recv_data = udp_socket.recvfrom(1024)
    print("%s:%s" % (str(recv_data[1]), recv_data[0].decode("utf-8")))


def main():
    # 创建一个udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定信息
    udp_socket.bind(("", 7891))
    # 可以使用套接字收发数据
    while True:
        # 从键盘获取数据
        send_msg(udp_socket)
        # 接收并显示
        recv_msg(udp_socket)


if __name__ == "__main__":
    main()

