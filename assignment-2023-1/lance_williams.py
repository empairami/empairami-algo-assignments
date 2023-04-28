from sys import argv

with open(argv[2]) as f:
    file_content = f.readline().strip('\n')
    numbers = [int(num) for num in file_content.split(' ')]
    clusters = [[num] for num in sorted(numbers)]

cluster_distance = [
    [abs(clusters[i][0]-clusters[j][0]) for j in range(len(clusters))] for i in range(len(clusters))
]

for _ in range(len(clusters)-1):
    # We find the two clusters that are most similar to each other
    s = -1
    t = -1
    min_distance = -1
    for i in range(len(cluster_distance)):
        for j in range(len(cluster_distance)):
            if cluster_distance[i][j] != 0:
                if min_distance == -1 or cluster_distance[i][j] < min_distance:
                    s = i
                    t = j
                    min_distance = cluster_distance[i][j]

    # We merge these two clusters and create a new cluster
    merge = clusters[s] + clusters[t]

    # The distance of a new cluster 𝑢 that we create by merging two of the other clusters 𝑠, 𝑡 from every other cluster 𝑣 results from the formula
    for v in range(len(clusters)):
        if not len(clusters[v]) == 0 and not s == v and not t == v:
            d_s_v = cluster_distance[s][v]
            d_t_v = cluster_distance[t][v]
            d_s_t = cluster_distance[s][t]

            # calculate coefficients
            if argv[1] == "single":
                ai = 0.5
                aj = 0.5
                beta = 0
                gamma = -0.5
            elif argv[1] == "complete":
                ai = 0.5
                aj = 0.5
                beta = 0
                gamma = 0.5
            elif argv[1] == "average":
                ai = len(clusters[s]) / (len(clusters[s]) + len(clusters[t]))
                aj = len(clusters[t]) / (len(clusters[s]) + len(clusters[t]))
                beta = 0
                gamma = 0
            else:
                ai = (len(clusters[s]) + len(clusters[v])) / (len(clusters[s]) + len(clusters[t]) + len(clusters[v]))
                aj = (len(clusters[t]) + len(clusters[v])) / (len(clusters[s]) + len(clusters[t]) + len(clusters[v]))
                beta = -len(clusters[v]) / (len(clusters[s]) + len(clusters[t]) + len(clusters[v]))
                gamma = 0

            d_u_v = ai*d_s_v + aj*d_t_v + beta*d_s_t + gamma * abs(d_s_v - d_t_v)

            cluster_distance[v][s] = d_u_v
            cluster_distance[s][v] = d_u_v

    print("(" + " ".join(map(str, clusters[s])) + ")", "(" + " ".join(map(str, clusters[t])) + ")", "{:.2f}".format(min_distance), len(merge))

    # one of the merged clusters does now no longer exist
    for i in range(len(cluster_distance)):
        cluster_distance[i][t] = 0
        cluster_distance[t][i] = 0
    # put merged cluster in position of cluster s
    clusters[s] = sorted(merge)
    clusters[t] = []