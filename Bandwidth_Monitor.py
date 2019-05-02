# import matplotlib.animation as animation
# import matplotlib.pyplot as plt
# from matplotlib import style
import psutil
import socket
import time
# style.use("fivethirtyeight")
# fig = plt.figure()
# ax1 = fig.add_subplot(1, 1, 1)


# def animate(interval, total_network, time):
#   ax1.clear()
#   ax1.plot(total_network, time)
#   plt.ylabel("Network Activity")


def main():
    start = time.time()
    up_speed = psutil.net_io_counters().bytes_recv
    down_speed = psutil.net_io_counters().bytes_sent

    end = time.time()
    # ani = animation.FuncAnimation(fig, animate, fargs=(up_speed+down_speed, end - start), interval=1000)
    # plt.show()
    time_elapsed = end - start

    print("Connection Speed: {0:.2f} up {0:.2f} down".format(bytes_to_gb(up_speed)/60, bytes_to_gb(down_speed)/60))
    connections = psutil.net_connections()
    header = ["Process Name", "PID", "Local Address", "Foreign Address", "Status"]
    print("{:30} {:5} {:37} {:47} {:11}".format(*header))
    for connection in connections:
        ip_address = connection[4]
        status = connection[5]
        pid = connection[6]
        process = psutil.Process(pid)
        name = process.name()
        out_name = ""
        if any(map(len, ip_address)):
            try:
                ip_out = ip_address[0]
                outbound_conn = socket.gethostbyaddr(ip_out)
                out_name = outbound_conn[0]
            except socket.herror:
                out_name = "not found"

            port = ip_address[1]
            adrs = ip_address[0]

            print("{:30} {:>5} {:>23} {:>5} {:>25} {:>11}".format(name, pid, adrs, port, out_name, status))
            # print(name, pid, ip_address, outbound_conn, status)


def monitor_internet_speed(up_speed, down_speed, time_elapsed):
    print(bytes_to_gb(up_speed + down_speed), time_elapsed)


def bytes_to_gb(value):
    return value * 8e-6


main()
