import os
import time
import logging
import argparse
import json
import statistics
import matplotlib.pyplot as plt
import cProfile
import psutil

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

def xor_encrypt(data, key):
    logging.debug("Starting encryption")
    encrypted = bytearray()
    key_len = len(key)
    for i in range(len(data)):
        encrypted.append(data[i] ^ key[i % key_len])
    logging.debug("Encryption complete")
    return encrypted

def test_encryption(data, key, iterations=1000):
    logging.info("Testing encryption performance")
    times = []
    for _ in range(iterations):
        start_time = time.time()
        xor_encrypt(data, key)
        times.append(time.time() - start_time)
    logging.info("Testing complete")
    return times

def security_analysis(data):
    logging.info("Starting security analysis")
    patterns = {}
    for i in range(len(data) - 1):
        pattern = (data[i], data[i + 1])
        if pattern in patterns:
            patterns[pattern] += 1
        else:
            patterns[pattern] = 1
    repeated_patterns = {k: v for k, v in patterns.items() if v > 1}
    logging.info("Security analysis complete")
    return repeated_patterns

def analyze_performance(times):
    avg_time = sum(times) / len(times)
    logging.info(f"Average encryption time: {avg_time:.6f} seconds")
    print(f"Average encryption time: {avg_time:.6f} seconds")

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(times, bins=30, edgecolor='k', alpha=0.7)
    plt.title("Encryption Time Distribution")
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency")

    plt.subplot(1, 2, 2)
    plt.boxplot(times, vert=False)
    plt.title("Encryption Time Box Plot")
    plt.xlabel("Time (s)")

    plt.tight_layout()
    plt.show()

    logging.info(f"Median encryption time: {statistics.median(times):.6f} seconds")
    logging.info(f"Standard deviation of encryption times: {statistics.stdev(times):.6f} seconds")

def profile_code(func):
    profiler = cProfile.Profile()
    profiler.enable()
    func()
    profiler.disable()
    profiler.print_stats(sort="time")

def estimate_power_consumption(iterations):
    cpu_usages = []
    for _ in range(iterations):
        cpu_usage = psutil.cpu_percent(interval=0.1)
        cpu_usages.append(cpu_usage)

    average_cpu_power = 65  # Assume an average power consumption for CPU (in Watts)
    power_consumptions = [(cpu_usage / 100) * average_cpu_power for cpu_usage in cpu_usages]

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(cpu_usages, label="CPU Usage (%)")
    plt.title("CPU Usage Over Time")
    plt.xlabel("Iteration")
    plt.ylabel("CPU Usage (%)")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(power_consumptions, label="Power Consumption (W)", color='r')
    plt.title("Estimated Power Consumption Over Time")
    plt.xlabel("Iteration")
    plt.ylabel("Power Consumption (W)")
    plt.legend()

    plt.tight_layout()
    plt.show()

    avg_power_consumption = sum(power_consumptions) / len(power_consumptions)
    logging.info(f"Average estimated power consumption: {avg_power_consumption:.2f} W")
    print(f"Average estimated power consumption: {avg_power_consumption:.2f} W")

def main(data_size, key_size, iterations):
    try:
        data = bytearray([i % 256 for i in range(data_size)])
        key = bytearray([i % 256 for i in range(key_size)])

        encryption_times = test_encryption(data, key, iterations)

        repeated_patterns = security_analysis(data)
        if repeated_patterns:
            logging.warning(f"Found repeated patterns: {repeated_patterns}")
            print(f"Found repeated patterns: {repeated_patterns}")
        else:
            logging.info("No repeated patterns found.")
            print("No repeated patterns found.")

        analyze_performance(encryption_times)

        estimate_power_consumption(iterations)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XOR Encryption Performance and Security Analysis")
    parser.add_argument("--data_size", type=int, default=10, help="Size of the data to be encrypted")
    parser.add_argument("--key_size", type=int, default=4, help="Size of the encryption key")
    parser.add_argument("--iterations", type=int, default=5, help="Number of iterations for testing")
    args = parser.parse_args()

    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            config = json.load(file)
            args.data_size = config.get("data_size", args.data_size)
            args.key_size = config.get("key_size", args.key_size)
            args.iterations = config.get("iterations", args.iterations)

    profile_code(lambda: main(args.data_size, args.key_size, args.iterations))
