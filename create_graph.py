# Create lists of inner and outer nodes
outer = list(range(12))
inner = list(range(12,24,1))

# Create list of outer edges
outer_edges = []
for i in range(len(outer)):
    if i < max(outer):
        outer_edges.append((i, i+1))
    else:
        outer_edges.append((0, max(outer)))

# Create list of inner edges
inner_temp = inner + inner + inner
inner_edges = []
for i in inner:
    inner_edges.append((i, inner_temp[i+4]))
    inner_edges.append((i, inner_temp[i+8]))

# Create list of inner edges
cross_edges = []
for i in range(len(outer)):
    cross_edges.append((outer[i], inner[i]))

edges = inner_edges + outer_edges + cross_edges