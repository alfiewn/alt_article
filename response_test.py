from statistics import mean, stdev

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


# Plot bar chart of local and remote response times
def plot_bar(indexes, local):
    x = np.arange(len(input_indexes)) 
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, local_average_time, width, label='Local')

    ax.set_ylabel('Response Time (s)')
    ax.set_xlabel('Input Index')
    ax.set_title('Successful Response Time')
    ax.set_xticks(x)
    ax.set_xticklabels(input_indexes)
    ax.legend()

    fig.tight_layout()

    plt.show()

input_indexes = []
local_average_time = []
remote_average_time = []

# Initial requests to ensure endpoints are up
requests.get("http://127.0.0.1:5000/by_index/1")

# Test parameters
inputs_to_test = 10
step_size = 1000
repeats = 3
expected_code = 200

# Initialise counters
succeses = 0
index = 0

while succeses < inputs_to_test:

    # Build request URL
    local_url = "http://127.0.0.1:5000/by_index/" + str(index*step_size)

    # Make request repeatedly
    local_response_time = []
    for repeat in range(repeats):
        
        local_response = requests.get(local_url)
        local_response_time.append(local_response.elapsed.total_seconds())

    # Record results for expected http status code
    if local_response.status_code == expected_code:
        input_indexes.append(index*step_size)
        local_average_time.append(round(mean(local_response_time), 4))
        succeses += 1

    index += 1


# Create dataframe for table output
df = pd.DataFrame({
    'Input Index': input_indexes,
    'Local Response Time': local_average_time,
})

# Print latex output
print(df.to_latex(index=False))

# Print averages and standard deviations
print("Local mean:", round(mean(local_average_time), 4))
print("Local stdev:", round(stdev(local_average_time), 4))

# Call plot function
plot_bar(input_indexes, local_average_time)



    














