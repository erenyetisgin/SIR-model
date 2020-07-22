import networkx as nx
import matplotlib.pyplot as plt
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep

# Variables
N = 100
m = 3
iter_count = 1000

# Initiate Graph
G = nx.barabasi_albert_graph(N, m)
pos = nx.spring_layout(G)

# SIR Model
model = ep.SIRModel(G)

# Model Config
cfg = mc.Configuration()
cfg.add_model_parameter('beta', 0.01)
cfg.add_model_parameter('gamma', 0.005)
cfg.add_model_parameter('fraction_infected', 0.05)  # Initial Fraction Infected
model.set_initial_status(cfg)

# Lists for simulation and plotting
t = []
S = []
I = []
R = []
color_map = []

# Simulation Execution
for iterations in model.iteration_bunch(iter_count):
    status_list = iterations.get('status')
    t.append(iterations.get('iteration'))
    node_count = iterations.get('node_count')
    S.append(node_count[0])
    I.append(node_count[1])
    R.append(node_count[2])

    # Initializing color_map
    if iterations.get('iteration') == 0:

        for status in status_list:
            if status_list[status] == 0:
                color_map.append('green')
            elif status_list[status] == 1:
                color_map.append('red')
            elif status_list[status] == 2:
                color_map.append('yellow')
    else:
        # Updating color_map according to node status
        if status_list:
            for status in status_list:
                if status_list[status] == 0:
                    color_map[status] = 'green'
                elif status_list[status] == 1:
                    color_map[status] = 'red'
                elif status_list[status] == 2:
                    color_map[status] = 'yellow'
    nx.draw(G, pos, node_color=color_map, with_labels=True)
    plt.pause(0.01)  # Time set between iterations in seconds
    plt.clf()

# Plot
plt.show()
plt.clf()
plt.suptitle('5% Infected')
plt.plot(t, S, label='S')
plt.plot(t, I, label='I')
plt.plot(t, R, label='R')
plt.xlabel('$t$')
plt.ylabel('Node Count')
plt.legend()
plt.show()
