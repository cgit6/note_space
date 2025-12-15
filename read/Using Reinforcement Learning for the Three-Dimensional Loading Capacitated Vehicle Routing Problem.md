# Using Reinforcement Learning for the Three-Dimensional Loading Capacitated Vehicle Routing Problem

#### Abstract

HGVs are important for the economy but contribute significantly to climate change with only $60 \%$ loading efficiency in the UK. Collaborative vehicle routing with coloading of delivery items is a promising solution to increase efficiency, but challenges remain to make this a possibility. One key challenge is the efficient computation of viable solutions. Current operations research methods suffer from non-linear scaling with increasing problem size and are therefore bound to limited geographic areas to compute results in time for day-to-day operations. This only allows for local optima in routing and leaves global optimization potential untouched. We develop a reinforcement learning model to solve the three-dimensional loading capacitated vehicle routing problem in linear time. While the three-dimensional loading capacitated vehicle routing problem has been studied extensively in operations research, no publications on solving the problem with reinforcement learning exist. We demonstrate the linear time scaling of our reinforcement learning model and benchmark our routing performance against state-of-the-art methods. The model performs within an average gap of $3.83 \%$ to $7.65 \%$ compared to the established methods. Our model, therefore, not only represents a promising first step towards large scale logistics optimization with reinforcement learning but also lays the foundation for this stream of research. GitHub: <https://github.com/if-loops/3L-CVRP>

## 1. Introduction

Heavy goods vehicles (HGVs) are a vital part of the supply chains that power our economy. At the same time, HGVs are also a major contributor to climate change, accounting for $4.75 \%$ of the total greenhouse gas emissions in the United Kingdom alone (Transport Statistics Great Britain 2020). Despite this significant impact on our environment, logistics operations in the UK are lacking efficiency with an average loading factor of only around $60 \%$ for HGVs (Freight Transport Association 2019).

One promising approach to increase the efficiency of HGV usage is collaborative vehicle routing with co-loading of delivery items, as shown in Figure 1. In this approach, carriers give away packages that are undesirable for their routes and accept packages from other carriers that fit within their routes. This exchange of items between carriers enables more efficient operations than a single carrier could achieve individually. The problem in practice lies within the sharing and assignment of the transportation requests (Gansterer and Hartl 2018). While there are different centralized and decentralized approaches to this challenge, they all rely on bin-packing and vehicle-routing

[^0]algorithms to determine viable package reassignment options. The combined problem of vehicle routing and 3D bin-packing is commonly referred to as the three-dimensional loading capacitated vehicle routing problem (3L-CVRP).
![](https://cdn.mathpix.com/cropped/2025_07_31_4ded066fdc202d6cd57cg-02.jpg?height=415&width=869&top_left_y=461&top_left_x=599)

Figure 1.: Collaborative packing and routing
The 3L-CVRP is a long-standing problem in the operations research literature (e.g., Gendreau et al. 2006). However, these existing approaches have two shortcomings. First, existing approaches are based on heuristics that are limited by the quality of the chosen rules and need to be adapted to new scenarios by domain experts. Second, existing approaches require convergence towards near-optimal solutions, which is computationally expensive. For example, a routing problem with 15 destinations requires around 10 seconds, while a routing problem with 100 destinations requires over 2000 seconds (Mahvash et al. 2017). In practice this leads to the decomposition into different regions (e.g., area codes) that get optimized individually to enable computation on a day-to-day basis. As illustrated in Figure 2 compared to Figure 1, this approach creates solutions that can be locally optimal but lack global optimality due to the sub-optimal decomposition.
![](https://cdn.mathpix.com/cropped/2025_07_31_4ded066fdc202d6cd57cg-02.jpg?height=512&width=1017&top_left_y=1560&top_left_x=525)

Figure 2.: Optimality gap caused by regional optimization
Solving the shortcomings of existing methods in the 3L-CVRP requires a method that relies less on heuristics and significantly improves compute times. For this, we propose the use of reinforcement learning (RL). Compared to existing approaches, reinforcement learning has several benefits. First, while training a reinforcement learning model is time-intensive, the learned policies can be executed in near real-time. Second, reinforcement learning models can learn policies based on a given cost function without human-designed heuristics. This not only allows us to potentially close the
global optimality gap shown in Figure 2 but also enables retraining for new problem settings without the need for new expert generated heuristics.

We benchmark the proposed reinforcement learning model on the original formulation of the 3L-CVRP (i.e., Gendreau et al. 2006) against state-of-the-art approaches (e.g., Mahvash et al. 2017; Zhang et al. 2015). Our benchmarking results show an average gap of $3.83 \%$ to Mahvash et al. (2017) and $7.65 \%$ to Zhang et al. (2015) combined with significantly better compute time scaling. Our model, therefore, represents a promising first step towards the large scale optimization of 3L-CVRP.

This work makes three main contributions to the literature. First, it merges the reinforcement learning research streams on bin-packing and vehicle routing by proposing the first reinforcement learning model to solve the 3L-CVRP in literature. Second, it addresses the computational limitations of existing approaches with the favourable compute times of reinforcement learning during execution. Third, the open-sourcing of the reinforcement learning environment lowers the entry barrier for other researchers to extend the literature on $3 \mathrm{~L}-\mathrm{CVRP}$.

The remainder of this work is structured as follows. In Section 2, we review the literature and reveal shortcomings of current methods and gaps in the literature. In Section 3, we define the problem formulation and develop our reinforcement learning model. In Section 4, we benchmark the model against state-of-the-art solutions and interpret the results. In Section 5, we discuss the contributions to literature, limitations, and implications for practice before concluding in Section 6.

## 2. Related Work

Two streams of research are particularly relevant for this work: First, the literature on vehicle routing and bin-packing problems. Second, the applications of reinforcement learning in operations management.

### 2.1. Vehicle routing and bin-packing problems

Increasing the utilization of HGVs requires solving two interdependent optimizations problems: vehicle routing and bin-packaging. The vehicle routing problem itself focuses on finding the shortest possible vehicle routes to fulfill customer demands (Laporte et al. 2013) and is closely related to the traveling salesman problem (Flood 1956). However, the problem formulation does not consider the loading situation of vehicles and is therefore not satisfactory for real-world problems. The bin-packing problem on the other hand solely focuses on packing items as efficiently as possible with no regard to routing considerations (Mack and Bortfeldt 2012). Therefore, we require the joint solving of both problems in practice.

To combine the vehicle routing and bin-packing problems into one, Gendreau et al. (2006) introduced the capacitated vehicle routing problem with 3D loading constraints. The Gendreau et al. (2006) formulation of the 3L-CVRP was originally solved via a tabu search approach by the authors. As surveyed by Bortfeldt and Yi (2020), numerous heuristic and metaheuristic approaches have been proposed to solve the Gendreau et al. (2006) formulation with greater speed and smaller optimality gaps. Recent publications include evolutionary local search (Zhang et al. 2015), column generation technique based heuristics (Mahvash et al. 2017), and adaptive variable neighborhood search (Wei et al. 2014). There have also been other formulations of the 3L-CVRP including Bortfeldt and Yi (2020), Zhang et al. (2017) and Pan et al. (2021)
who have worked on more realistic 3L-CVRP problems that include time constraints and split-deliveries.

All existing methods share two limitations. First, heuristics-based approaches are naturally only as good as the chosen rules and therefore need to be adapted to new scenarios that deviate from the original problem setting. Second, the existing methods are based on incremental convergence towards a near-optimal solution. This leads to significant compute times as the problem size increases and therefore requires regional restriction of the optimization to compute results on a day-to-day basis. We address these shortcomings by proposing the use of reinforcement learning to solve the Gendreau et al. (2006) formulation of the 3L-CVRP.

### 2.2. Reinforcement learning in operations management

Reinforcement learning is a subfield of machine learning in which an agent interacts with an environment while trying to maximize a given reward function. At every time step, the agent receives an observation from the environment and then chooses the best action out of all available actions based on what it has learned so far. This choice is then passed to the environment which calculates the new state after taking the chosen action. The observation of this new state is then passed back to the agent to choose the next action and the process is repeated until the interaction ends. By balancing exploration of uncertain actions and exploitation of known good actions, a decision policy is learned (Sutton and Barto 2018). While the training process is time-intensive, the learned policies only need one compute step per chosen action compared to the previously discussed convergence-based operations research methods. This provides considerable opportunities to speed up solution-finding.

Within operations management, reinforcement learning has already been successfully applied to various inventory models. Oroojlooyjadid et al. (2021) used reinforcement learning to solve the problems of compute time and the lack of one known ideal policy within the supply chain beer game. They were able to achieve near-optimal results on real-world data and performed the computations in real-time. Gijsbrechts et al. (2021) compared the performance of deep reinforcement learning models to state-of-the-art heuristics for lost sales inventory models, dual sourcing inventory models, and multi-echelon inventory models. Their results matched the performance of state-of-the-art heuristics.

The two sub-problems of 3L-CVRP, vehicle routing and bin-packing, have already been studied independently in the reinforcement learning literature. Peng et al. (2020), Xin et al. (2020), Nazari et al. (2018), and Kool et al. (2018) demonstrated the viability of reinforcement learning for the vehicle routing problem using encoder-decoder architectures. Duan et al. (2019) have demonstrated the viability of reinforcement learning for the bin-packing problem with $\mathrm{A} / \mathrm{B}$ tests at supermarket warehouse systems of Taobao, where they achieved an average of $5.47 \%$ cost reduction. However, to the best of our knowledge, the 3L-CVRP has not been solved with reinforcement learning in the literature. This work aims at closing this gap by combining vehicle routing and bin-packing into one model.

## 3. 3L-CVRP Model

This section develops a reinforcement learning model to solve the 3L-CVRP. In the following, we provide a problem definition and the model specification.

### 3.1. Problem Definition

While there are numerous formulations of the 3L-CVRP (e.g., Gendreau et al. 2006; Zhang et al. 2017; Pan et al. 2021), they generally consist of a graph $G(V, E)$ with vertices $V=\{0,1, \ldots, n\}$ and edges $E=\{0,1, \ldots\}$. The vertices $V$ consist of $n$ clients where vertex 0 corresponds to the depot from which all packages originate. The number of edges corresponds to the total number of trips from one location to another by the vehicles. Each of the $n$ clients is associated with $k=\left\{1, \ldots, m_{i}\right\}$ packages $\mathcal{I}_{i k}$. Hereby, the index $i$ represents the client and $k$ represents the package number (e.g., $\mathcal{I}_{12}$ is the second package of client one). The individual packages have a weight $d_{i k}$, height $h_{i k}$, width $w_{i k}$, and length $l_{i k}$. To deliver the packages, there are $v$ homogeneous vehicles $\mathcal{V}_{i}$ with a loading space of volume $h_{v e h} * w_{v e h} * l_{v e h}$ with a weight capacity $d_{v e h}$. The package placement in each vehicle must fulfill preset constraints (e.g., unloading order of packages). The total cost of the instance is calculated by summing up the cost of all edges $e_{i j}$ (e.g., euclidean distance between two vertices). Hereby, $e_{01}$ would represent a trip from the depot to client one. As defined by Zhang et al. (2017), our objective is therefore to minimize the total travel distance of all vehicles, with $t_{i}$ being the number of vertices in the route of vehicle $i$, resulting in

$$
\begin{equation*}
\min \sum_{i=1}^{v}\left(\sum_{j=1}^{t_{i}-1} e_{j(j+1)}\right) . \tag{1}
\end{equation*}
$$

### 3.2. Model Specification

We base our model on the attention model introduced by Kool et al. (2018) and extend it to solve the 3L-CVRP. The encoder-decoder architecture by Kool et al. (2018) was chosen as the starting point due to its demonstrated generalization performance on various routing problem settings ranging from the orienteering problem to vehicle routing. Due to the container loading constraints in $n=3$ dimensions, the feasibility checks for $m$ package placements require significant compute time and scale with $O\left(m * n^{3}\right)$. In order to reduce the number of placement locations to check, we use a least-space-wasted-furthest-back-rightmost-lowest package placement heuristic. Such a combination of reinforcement learning with heuristics-based placement has already been used Hu et al. (2017) for the 3D bin-packing problem and outperformed purely heuristics-based approaches.

### 3.2.1. Encoder

Adapted from Kool et al. (2018), the input of the encoder shown in Figure 3 consists of the depot location, the customer locations, and the customer demand. The depot location is defined by a tensor of shape [batch size, 1, 2] that describes the x and y coordinates of the depot. Similarly, the client locations are defined by a tensor of shape [batch size, $n, 2$ ] that describes the x and y coordinates for each node $n$. The customer demand tensor is of shape [batch size, $\sum_{i=1}^{n} m_{i}, 5$ ] and describes the height, weight, length, fragility, and weight of each individual package.

In order to make the model agnostic to vehicle and package sizes, we scale all dimensions relative to the vehicle dimensions (e.g., $h_{\text {veh_scaled }}=h_{\text {veh }} / h_{\text {veh }}=1$ and $\left.h_{i k_{-s c a l e d}}=h_{i k} / h_{v e h}\right)$. This information is then embedded in $d_{h}$ dimensions and passed through $a$ multi-head attention layers with $l$ heads each. The multi-head attention
![](https://cdn.mathpix.com/cropped/2025_07_31_4ded066fdc202d6cd57cg-06.jpg?height=278&width=1292&top_left_y=255&top_left_x=388)

Figure 3.: Encoder
allows the model to focus on multiple information criteria of interest at the same time (e.g., dimensions, distances). The generated node embeddings, denoted by a tensor of shape [batch size, $\left.n, d_{h}\right]$, are additionally aggregated as a graph embedding of shape [batch size, $1, d_{h}$ ] and then passed to the decoder as input.

### 3.2.2. Decoder

The decoder shown in Figure 4 combines the initial problem setting information from the encoder with the current loading and packing state to select the most suitable package to be loaded next. After loading the selected package, the current state is updated and the process is repeated until all packages have been loaded.
![](https://cdn.mathpix.com/cropped/2025_07_31_4ded066fdc202d6cd57cg-06.jpg?height=401&width=1209&top_left_y=1170&top_left_x=429)

Figure 4.: Decoder
Similarly to Kool et al. (2018), our step context information consists of three inputs. First, we extract the encoder embedding of the previously chosen node to represent our vehicle routing location, denoted by a tensor of shape [batch size, $1, d_{h}$ ]. Second, we create an embedding of the remaining weight capacity of the current vehicle, also denoted by a tensor of shape [batch size, $1, d_{h}$ ]. Third, we create an embedding of the current 3D container loading state. For computational efficiency, we translate the 3D loading space shown in Figure 5a into a 2D representation shown in Figure 5b and represent the loading heights via the cell value (Zhao et al. 2020). This representation still contains the same information as the 3D representation with improved efficiency for usage with convolutional neural networks (CNNs). In order to represent the fragility of packages, we assign a positive sign to all non-fragile height aggregations and a negative sign to all fragile ones. All values are then scaled from a $\left[-h_{\text {veh }}, h_{\text {veh }}\right]$ to $[-1,1]$ range before resizing the $w_{\text {veh }} * l_{\text {veh }}$ vehicle representation to a uniform size of $w_{c n n} * l_{c n n}$. This enables the model to be applied to varying container sizes. The scaled and resized 2D input is passed to a 2D convolution layer and subsequently embedded in $d_{h}$ dimensions. The resulting embedding is of the shape [batch size, 1 , $\left.d_{h}\right]$ and concatenated with the two other step context embeddings.

The encoder output along with the step context embeddings and a mask is passed to a multi-head attention layer which produces an output of the shape [batch size,
![](https://cdn.mathpix.com/cropped/2025_07_31_4ded066fdc202d6cd57cg-07.jpg?height=809&width=1220&top_left_y=372&top_left_x=515)

Figure 5.: Container representation
$\left.1, d_{h}\right]$. The mask filters out infeasible actions during calculation (e.g., packages that have already been packed). A single-head attention layer is used to generate a tensor of the shape [batch size, 1, actions] that represents the log probabilities of all actions (Kool et al. 2018). The actions are then passed to the environment to be updated (i.e. loading and routing the selected package) and the decoder step is repeated until all packages have been packed or no more viable placement options remain. The collection of all chosen actions is saved as the routing list.

### 3.2.3. Masking and Packing Heuristic

As computational speed is one of the main objectives of applying reinforcement learning to the 3L-CVRP, we do not compute all package placement feasibilities at every step since they are computationally expensive. Instead, we use a two-step masking approach. The first mask is determined by violations of the problem constraints that do not require a placement feasibility check (e.g., packages that are already packed) and is applied before calculating the action probabilities. Rather than passing a single action from the calculated probabilities shown in Figure 4, we pass a list of recommended actions in descending order to the environment. This action list is then used for our on-demand look-ahead feasibility check. Starting from the action with the highest probability we perform a placement feasibility check until we find an action that is feasible to be placed in the vehicle based on the constraints (see Algorithm 1 in the Appendix). This way we can reduce computation time significantly as we only have to check one package in an ideal case and all packages in the worst case. To speed up learning of the Gendreau et al. (2006) constraint that demands that all packages for a location must be delivered in a single vehicle, we add a look-ahead feasibility check. This means when there is more than one package remaining for a location, we check if they are all feasible to be loaded in the current vehicle.

Analogously to Hu et al. (2017), we place packages in the lowest, rightmost, and furthest back position available in each vehicle to reduce the action space with minimal impact on optimality. This is achieved via a least-space-wasted-furthest-back-rightmost-lowest heuristic. When an action is passed to the feasibility check outlined in Algorithm 1, the corresponding package is selected and the furthest back rightmost lowest placement is computed for all rotation possibilities. The rotation and placement with the least space wasted is selected, with the shorter total loading distance acting as a tiebreaker. Least space wasted is defined as the empty space blocked behind a package along the unloading axis.

### 3.2.4. Proximal Policy Optimization with Greedy Rollout

Given the complexity and a high number of constraints for our model, we use proximal policy optimization (PPO) to stabilize the learning process (Schulman et al. 2017). Our loss function is defined as

$$
\begin{equation*}
L(\theta)=\hat{\mathbb{E}}_{t}\left[\min \left(r_{t}(\theta) \times \hat{A}_{t}, \operatorname{clip}\left(r_{t}(\theta), 1-\epsilon, 1+\epsilon\right) \times \hat{A}_{t}\right)+\alpha \times S\left[\pi_{\theta}\right]\left(s_{t}\right)\right] \tag{2}
\end{equation*}
$$

Here, $S\left[\pi_{\theta}\right]$ denotes the entropy of the chosen actions and is used to encourage exploration. The ratio $r_{t}(\theta)=\frac{\pi_{\theta}\left(a_{t} \mid s_{t}\right)}{\pi_{\theta} \text { old }\left(a_{t} \mid s_{t}\right)}$ reflects the change of probabilities in between policy updates. Combined with the clipping parameter $\epsilon$, this ensures model updates that stay close to the original policy. The advantage $\hat{A}_{t}$ is defined as the difference between the cost and a baseline. Similar to Kool et al. (2018), we use a greedy rollout baseline to compare the current cost of the training epoch to the performance of the previously best model during training. We hereby always select the action with the highest probability for the baseline-thus greedy rollout (in comparison to sampling based on the probability during training). This direct comparison provides a robust low-variance advantage estimation. Our cost function (the negative reward function), is defined as:

$$
\begin{gather*}
C=C_{v r p}+C_{\text {packing }}  \tag{3}\\
C_{v r p}=\frac{\sum_{i=1}^{v}\left(\sum_{j=1}^{t_{i}-1} e_{j(j+1)}\right)}{p_{v r p} * \sum_{i=1}^{n} e_{i(j=0)}}  \tag{4}\\
C_{\text {packing }}=\frac{\text { number of missed packages }}{n} \tag{5}
\end{gather*}
$$

Equation 4 sums up all vehicle paths and divides them by the sum of all individual travel distances from the depot to each of the $n$ client locations multiplied by a penalty factor $p_{\text {vrp }}$. This scaling ensures that varying optimal distances caused by the randomly generated locations are comparable during training. As our agent would learn to not load any packages for a distance of zero, we penalize packages that were not loaded in Equation 5. The division by $n$ is used to keep both cost function terms similar in
magnitude. Our formulation enables the weighing of the vehicle routing ( $p_{\text {vrp }} \rightarrow 0$ ) and bin-packing ( $p_{\text {vrp }} \rightarrow \infty$ ) aspects during training.

## 4. Results

This section reports on the implementation details and the results of the proposed RL model on the benchmarking instances of Gendreau et al. (2006). We compare against the original tabu-search of Gendreau et al. (2006), the column-generation technique of Mahvash et al. (2017), and the evolutionary local search of Zhang et al. (2015) in terms of the achieved routing distances and the time to compute the solutions.

### 4.1. Implementation Details

This subsection focuses on the problem definition and the training process. We describe the used 3L-CVRP problem formulation, the chosen benchmarking instances, and the training process including data generation.

### 4.1.1. Benchmarking Problem Definition

Gendreau et al. ( 2006 ) define the cost of travelling from one vertex to another as the euclidean distance between the two and set the following constraints:
(1) Every vehicle route must start and end at the depot.
(2) Clients may not be visited more than once.
(3) All package weights $d_{i}$ combined in a vehicle must not exceed $d_{\text {max }}$.
(4) All packages must be loaded in an orthogonal three-dimensional layout without overlapping and within the vehicle space.
(5) The vertical orientation of packages is fixed.
(6) Fragile packages $f_{i k}=1$ can be placed on non-fragile packages $f_{i k}=0$ but not vice-versa.
(7) Each package must be supported by either the floor of the vehicle or other packages. The created support area $a_{\text {supp }}$ must fulfil $a_{\text {supp }}>=a_{\text {min }} * w_{i k} * l_{i k}$ with $a_{\text {min }}$ being the support area threshold.
(8) All packages must be possible to unload via the Last In First Out (LIFO) principle along the $l$ axis of the vehicle without intersecting other packages or decreasing the support area of other packages.

### 4.1.2. Benchmarking Instances

Gendreau et al. (2006) introduced 27 predefined instances of varying complexity based on the problem formulation described in Section 4.1.1. Within the scope of this work, we focus on the two smallest instances, as shown in Table 1, due to the significant training time required for bigger instances.

### 4.1.3. Training Process

The training process for our reinforcement learning model is as follows. At each epoch, we generate 100 random instances which are processed in parallel. This reduces the variance during updates after each epoch while still being fast enough for training

Table 1.: Predefined Gendreau et al. (2006) instances

| Instance | Destinations | Vehicles | Packages |
| :------- | :----------- | :------- | :------- |
| E016-03m | 15           | 5        | 32       |
| E016-05m | 15           | 5        | 26       |

on our hardware (ca. 60 seconds per epoch on the ETH Zürich Euler cluster with 8 cores). We generate the random instances by uniformly sampling from the parameters listed in Table 2. These ranges are chosen to resemble the ranges used by Gendreau et al. (2006) for the design and validation of their own tabu-search method. We speed up training by using training instances with fewer size increments due to a smaller container size than those used in the benchmarks (e.g., width dimension reduction from 25 to 5 ). This reduces the compute time for feasibility checks in the containers significantly as the search space shrinks by a factor of 125 from $30 * 25 * 60=45.000$ to $6 * 5 * 12=360$.

Table 2.: Parameter space for training instances

| Parameter                            | Value(s)                                                                |
| :----------------------------------- | :---------------------------------------------------------------------- |
| $n$                                  | 15                                                                      |
| Probability of package being fragile | 25\%                                                                    |
| $x_{i}$                              | [0, 100]                                                                |
| $y_{i}$                              | [0, 100]                                                                |
| $h_{\text {veh }}$                   | 6                                                                       |
| $w_{\text {veh }}$                   | 5                                                                       |
| $l_{\text {veh }}$                   | 12                                                                      |
| $h_{i k}$                            | $\left[0.2 \times h_{\text {veh }}, 0.6 \times h_{\text {veh }}\right]$ |
| $w_{i k}$                            | $\left[0.2 \times w_{\text {veh }}, 0.6 \times w_{\text {veh }}\right]$ |
| $l_{i k}$                            | $\left[0.2 \times l_{\text {veh }}, 0.6 \times l_{\text {veh }}\right]$ |
| $m_{i}$                              | [1,2,3]                                                                 |
| $d_{i}$                              | [1, 2, ..., 30]                                                         |

Based on the total volume and weight of all packages, we assign a number of vehicles to each instance that equals twice the needed capacity. This ensures that all packages can be packed without the computationally intensive step of testing for the minimum number of trucks based on feasible loading combinations. This upper truck limit prevents infinite looping of extra requested trucks during training.

After each epoch, the cost and loss for the routing is calculated according to Section 3.2.4. Next, the encoder and decoder are optimized with the Adam optimizer (Kingma and Ba 2014) before generating new data for the following epoch. Figure 6 shows the learning curve of our model for four 120 hour runs with different random seeds on the validation data (batch size equals training). Run 4 was trained with a batch size of 128 in comparison to all other runs with size 100 and thus performed fewer epochs within 120 hours. The model parameters are listed in Table 1 in the appendix. We selected
the epoch with the best validation performance to be used for the benchmarking on the Gendreau et al. (2006) instances in Section 4.2.
![](https://cdn.mathpix.com/cropped/2025_07_31_4ded066fdc202d6cd57cg-11.jpg?height=595&width=1412&top_left_y=439&top_left_x=322)

Figure 6.: Validation data learning curves

### 4.2. Benchmarking Results

In this subsection, we compare the performance of our reinforcement learning model against state-of-the-art methods for solving the 3L-CVRP. We compare both the routing results as well as the compute times and interpret the results.

### 4.2.1. Routing Distances

We compare our results to three existing approaches. First, the original tabu-search implementation by Gendreau et al. (2006) to illustrate the performance improvement of recent publications. Second, the evolutionary local search implementation of Zhang et al. (2015) which provides the best results in terms of pure routing distance. Third, the column-generation based approach of Mahvash et al. (2017) because of its compute speed ( $33.7 \%$ faster than Zhang et al. (2015)) paired with only a slight decrease in routing performance. Given that a good balance between routing distance and compute time is desirable for real-world applications, we will refer to Mahvash et al. (2017) as the state-of-the-art to beat.

Table 3 shows the achieved routing distances of our model compared to the literature. Our model trained in run 2 achieved the best results on our validation data as well as the Gendreau et al. (2006) instances. The vehicle routing and packing by this model can be seen in Figure 7 a and 7 b . On the E016-03m instance our model achieves a routing distance of 337.85 . Compared with the solutions from the literature this is a $6.81 \%$ to $11.86 \%$ gap. On the E016-05m instance our model achieves a routing distance of 347.86 with a gap ranging from $-0.78 \%$ to $3.85 \%$.

In order to test the robustness of our results, we perform test-time augmentation for the benchmarking instances. Hereby, we translate and flip the node locations of the two benchmarking instances to investigate how this affects the outputs. Given the $[0,100]$ plane we are using, flipping means that $x=10$ would become $x=90$ and vice versa. Given that the instances are unchanged except for translation or mirroring, the routing should remain the same in an ideal model. The results in Table 4 show that

Table 3.: Routing distance comparison of models

|                                | E016-03m | E016-05m | Avg. distance |
| :----------------------------- | :------- | :------- | :------------ |
| Gendreau et al. (2006)         | 316.32   | 350.58   | 333.45        |
| Zhang et al. (2015)            | 302.02   | 334.96   | 318.49        |
| Mahvash et al. (2017)          | 315.16   | 345.28   | 330.22        |
| RL (our best model from run 2) | 337.85   | 347.86   | 342.86        |
| RL (average of 4 runs)         | 358.26   | 356.80   | 357.53        |
| Gap to Gendreau et al. (2006)  | 6.81\%   | -0.78\%  | 2.82\%        |
| Gap to Zhang et al. (2015)     | 11.86\%  | 3.85\%   | 7.65\%        |
| Gap to Mahvash et al. (2017)   | 7.20\%   | 0.75\%   | 3.83\%        |

the two best-performing runs on the validation data do not produce consistent results during test-time augmentation. Run 4, which has been trained with a batch size of 128 achieves consistent results when all nodes are shifted along the x and y -axis. The model of run 2 with a smaller batch size of 100 is not consistent for a larger movement of +20 . Both models produce different results when an axis is flipped. Thus, steps need to be taken to improve the robustness of our models (e.g., train-time augmentation, increased batch sizes for model updates with less variance) to produce robust results.

Table 4.: Test-time augmentation

|                       | E016-03m |          | E016-05m |          |
| :-------------------- | :------- | :------- | :------- | :------- |
|                       | Run 4    | Run 2    | Run 4    | Run 2    |
| Original              | 334.99   | 337.85   | 361.86   | 347.86   |
| x and $\mathrm{y}+10$ | 334.99   | 337.85   | 361.86   | 334.95   |
| x and $\mathrm{y}+20$ | 334.99   | 303.51\* | 355.04   | 358.80   |
| x-axis flipped        | 362.81   | 329.85\* | 347.06   | 364.19   |
| y-axis flipped        | 330.54\* | 345.78   | 365.84   | 348.38   |
| x and y -axis flipped | 380.53   | 359.81   | 328.38   | 355.25\* |

- not all packages packed

As mentioned in Section 4.1.3, our model was trained on a different container size ([6,5,12]) than the benchmarks ([30,25,60]). Achieving results within a few percent of the state-of-the-art solution shows that our model is container size agnostic and can handle package sizes it has never encountered before. The current $3.83 \%$ gap in routing distance compared to Mahvash et al. (2017), therefore, seems achievable by improving the model architecture (e.g., improving the placement heuristic), training on the container size used for benchmarking itself and increasing the batch size for more robust results.
![](https://cdn.mathpix.com/cropped/2025_07_31_4ded066fdc202d6cd57cg-13.jpg?height=749&width=1335&top_left_y=328&top_left_x=349)

Figure 7.: Vehicle routing with our model

### 4.3. Compute Times

Next, we compare the compute time scaling of our best performing model against the compute times reported by Mahvash et al. (2017). Mahvash et al. (2017) was chosen as a baseline because of their $33.7 \%$ faster computation of solutions compared to Zhang et al. $(2015)$. As absolute compute time comparisons can vary greatly by the chosen implementation and hardware (e.g., C, Python, GPU, CPU), we focus on the relative scaling of computing times with increasing instance sizes.

The compute times for our model in this comparison were calculated by applying our model to randomly generated instances according to the Gendreau et al. (2006) formulation of the 3L-CVRP. The compute times for Mahvash et al. (2017) are the ones they reported for the solution of the respective Gendreau et al. (2006) benchmarking instances. Thus, the absolute comparison due to varying hardware should not be considered and the focus should be on the scaling. Figure 8 shows empirically that our model scales approximately linearly ( $R^{2}=0.91$ ) with an increasing number of destinations. The column-generation technique by Mahvash et al. (2017) on the other hand does not scale linearly.

Figure 8 highlights the potential of our model to solve the shortcoming of existing methods in regard to compute time scalability. This enables the extension of the reallife solution space beyond current regional limits as discussed in Section 1 and will allow for solutions closer to a global optimum rather than regional optima.

## 5. Discussion

In this section, we discuss our contribution to the literature, the limitations of our current model, and the implications for practice.
![](https://cdn.mathpix.com/cropped/2025_07_31_4ded066fdc202d6cd57cg-14.jpg?height=532&width=752&top_left_y=299&top_left_x=629)

Figure 8.: Comparison of compute time scaling between our model on randomly generated instances with Gendreau et al. (2006) constraints and Mahvash et al. (2017) on the 27 Gendreau et al. (2006) instances

### 5.1. Contributions to the Literature

This work proposes a reinforcement learning model to solve the 3L-CVRP. Thereby, we contribute to the literature in three major ways. First, this work is the first to apply reinforcement learning to the 3L-CVRP. We combine the reinforcement learning research streams of vehicle routing and bin-packing and lay the foundation for future work on this problem. Second, we address the problem of computational scalability in existing 3L-CVRP research by introducing a method with vastly improved scalability. This lays the foundation for future research into pure reinforcement learning approaches and hybrid approaches for the 3L-CVRP that can be applied to larger scenarios than current methods. Third, we will make our reinforcement learning environment open source to make research into this topic more accessible.

### 5.2. Limitations

Our proposed reinforcement learning model has three main limitations. First, our current model is designed to meet the Gendreau et al. (2006) requirements and needs to be adapted for real-world use-cases. This includes among others heterogeneous fleets, package pickups during routing, time constraints for deliveries, and realistic loading constraints. Second, the model relies on a placement heuristic. By replacing it with a non-heuristics-based approach, we can gain access to an increased solution space and thus improve routing distance results. While this is a considerable limitation for the Gendreau et al. (2006) formulation with greatly varying package sizes, we chose the heuristic on purpose due to the alignment with practice. The real-world use-case of our industrial partner is based on standardized pallets within standardized containers which aligns well with the chosen heuristic. The hybrid approach of reinforcement learning and a placement heuristic helps to keep the model complexity and training time lower. Three, test-time augmentation of the instances shows that our models need to be improved in terms of robustness.

We also acknowledge the limitations of reinforcement learning in general. Deep reinforcement learning models in general have two significant limitations that apply to the 3L-CVRP. First, out-of-sample data can produce unreliable results. Therefore,
the data for training must be chosen carefully, models must be designed to be robust to outliers, and models must be limited in their usage to the designed application area. Second, the model is a black box and thus may cause stakeholders to be wary of implementing such a model as a first adopter.

In order to leverage the full potential of reinforcement learning for the 3L-CVRP and beyond, these limitations must be addressed. In regards to the general reinforcement learning limitations, we aim to integrate recent advances in the fields of robust models (Derrow-Pinion et al. 2021), interpretability of reinforcement learning models (Madumal et al. 2020), and safe exploration (Turchetta et al. 2020) to make the model production-ready. Furthermore, we aim to extend the model to incorporate realworld constraints (e.g., time constraints, pick-up, heterogeneous fleets). The improved model will then be applied to real-world data of our industry partner to detect further improvement potential and to estimate the economic impact compared to current solutions.

### 5.3. Implications for Practice

Our results show that reinforcement learning provides promising opportunities to enable large-scale optimization beyond current regional boundaries. In order to increase the likelihood of success, we have two recommendations. First, we recommend the usage of a hybrid model that combines reinforcement learning with established heuristics similar to our implementation. This combines the scalability of reinforcement learning with the reliability of established heuristics. Second, we recommend creating different models for easily separable use cases to improve model performance and reliability. Such separable use cases are for example pallets versus cardboard boxes of varying sizes. Another possible split are low-volume areas and high-volume areas (e.g., London-Birmingham-Manchester versus the rest of the United Kingdom).

## 6. Conclusion

This work proposes a reinforcement learning model for the 3L-CVRP to address the main shortcoming, non-linear computational scaling, of current operations research methods. First, we demonstrated the favourable scaling of our model with increasing problem size through computational experiments. Second, we showed that the routing performance of our model lies within $0.75 \%$ to $11.86 \%$ of the current state-of-the-art methods. Based on these findings, we see reinforcement learning as a promising path to large-scale global optimization of logistics operations that lie beyond the computational scope of existing methods and thus unlock new possibilities for efficiency gains and emissions reduction.

## References

Bortfeldt, A. and Yi, J. (2020), 'The split delivery vehicle routing problem with threedimensional loading constraints', European Journal of Operational Research 282(2), 545558.

Derrow-Pinion, A., She, J., Wong, D., Lange, O., Hester, T., Perez, L., Nunkesser, M., Lee, S., Guo, X., Wiltshire, B. et al. (2021), 'Eta prediction with graph neural networks in google maps', arXiv preprint arXiv:2108.11482 .

Duan, L., Hu, H., Qian, Y., Gong, Y., Zhang, X., Xu, Y. and Wei, J. (2019), 'A multi-task selected learning approach for solving 3d flexible bin packing problem', arXiv:1804.06896 [cs, stat] . arXiv: 1804.06896.
Flood, M. M. (1956), 'The traveling-salesman problem', Operations Research 4(1), 61-75.
Freight Transport Association (2019), 'FTA logistics report 2019', <https://www>. santandercb.co.uk/sites/default/files/documents/fta_logistics_report_2019. pdf. (Accessed on 08/10/2021).
Gansterer, M. and Hartl, R. F. (2018), 'Collaborative vehicle routing: A survey', European Journal of Operational Research 268(1), 1-12.
Gendreau, M., Iori, M., Laporte, G. and Martello, S. (2006), 'A tabu search algorithm for a routing and container loading problem', Transportation Science 40, 342-350.
Gijsbrechts, J., Boute, R. N., Van Mieghem, J. A. and Zhang, D. (2021), 'Can deep reinforcement learning improve inventory management? Performance on dual sourcing, lost sales and multi-echelon problems', <http://dx.doi.org/10.2139/ssrn.3302881>. (Accessed on 08/19/2021).
Hu, H., Zhang, X., Yan, X., Wang, L. and Xu, Y. (2017), 'Solving a new 3D bin packing problem with deep reinforcement learning method', arXiv:1708.05930 [cs] . arXiv: 1708.05930.
Kingma, D. P. and Ba, J. (2014), 'Adam: A method for stochastic optimization', arXiv preprint arXiv:1412.6980 .
Kool, W., van Hoof, H. and Welling, M. (2018), Attention, learn to solve routing problems!, in 'International Conference on Learning Representations'.
Laporte, G., Toth, P. and Vigo, D. (2013), 'Vehicle routing: Historical perspective and recent contributions', EURO Journal on Transportation and Logistics 2(1-2), 1-4.
Mack, D. and Bortfeldt, A. (2012), 'A heuristic for solving large bin packing problems in two and three dimensions', Central European Journal of Operations Research 20(2), 337-354.
Madumal, P., Miller, T., Sonenberg, L. and Vetere, F. (2020), 'Explainable reinforcement learning through a causal lens', Proceedings of the AAAI Conference on Artificial Intelligence 34(03), 2493-2500. Number: 03.
Mahvash, B., Awasthi, A. and Chauhan, S. (2017), 'A column generation based heuristic for the capacitated vehicle routing problem with three-dimensional loading constraints', International Journal of Production Research 55(6), 1730-1747.
Nazari, M., Oroojlooy, A., Snyder, L. V. and Takáč, M. (2018), 'Reinforcement learning for solving the vehicle routing problem', arXiv:1802.04240 [cs, stat] . arXiv: 1802.04240.
Oroojlooyjadid, A., Nazari, M., Snyder, L. V. and Takáč, M. (2021), 'A deep q-network for the beer game: Deep reinforcement learning for inventory optimization', Manufacturing ${ }^{\mathcal{E}}$ Service Operations Management .
Pan, B., Zhang, Z. and Lim, A. (2021), 'A hybrid algorithm for time-dependent vehicle routing problem with time windows', Computers $\mathscr{E}$ Operations Research 128, 105193.
Peng, B., Wang, J. and Zhang, Z. (2020), 'A deep reinforcement learning algorithm using dynamic attention model for vehicle routing problems', arXiv:2002.03282 [cs, stat] . arXiv: 2002.03282.

Schulman, J., Wolski, F., Dhariwal, P., Radford, A. and Klimov, O. (2017), 'Proximal policy optimization algorithms', arXiv preprint arXiv:1707.06347.
Sutton, R. S. and Barto, A. G. (2018), Reinforcement learning: An introduction, MIT press.
Transport Statistics Great Britain (2020), 'Transport statistics great britain 2020', <https://assets.publishing.service.gov.uk/government/uploads/system/uploads/> \attachment_data/file/945829/tsgb-2020.pdf. (Accessed on 07/18/2021).
Turchetta, M., Kolobov, A., Shah, S., Krause, A. and Agarwal, A. (2020), 'Safe reinforcement learning via curriculum induction', arXiv preprint arXiv:2006.12136.
Wei, L., Zhang, Z. and Lim, A. (2014), 'An adaptive variable neighborhood search for a heterogeneous fleet vehicle routing problem with three-dimensional loading constraints', IEEE Computational Intelligence Magazine 9(4), 18-30.
Xin, L., Song, W., Cao, Z. and Zhang, J. (2020), 'Multi-decoder attention model with embedding glimpse for solving vehicle routing problems', arXiv:2012.10638 [cs] . arXiv: 2012.10638
version: 1.
Zhang, D., Cai, S., Ye, F., Si, Y.-W. and Nguyen, T. T. (2017), 'A hybrid algorithm for a vehicle routing problem with realistic constraints', Information Sciences 394-395, 167-182.
Zhang, Z., Wei, L. and Lim, A. (2015), 'An evolutionary local search for the capacitated vehicle routing problem minimizing fuel consumption under three-dimensional loading constraints', Transportation Research Part B: Methodological 82, 20-35.
Zhao, H., She, Q., Zhu, C., Yang, Y. and Xu, K. (2020), 'Online 3D bin packing with constrained deep reinforcement learning', arXiv preprint arXiv:2006.14978 .

## Appendix

```
Algorithm 1 Package loading feasibility check for selected container
    $l_{\text {skip }}$ : prev. determined min. viable $l$
    for $l$ in range 0 to $l_{\text {container }}-l_{\text {package }}$ do
        if $l_{i} l_{\text {skip }}$ then
            skip to next $l$ iteration
        end if
        $h_{\text {contour }}=\min$. height for each $w$ along $w(l)$
        for $w$ in range 0 to $w_{\text {container }}-l_{\text {package }}$ do
            if $h_{\text {package }}-h_{\text {contour }}(w)<0$ then
                skip to next $w$ iteration
            end if
            for $h$ in range $h_{\text {contour }}(w)$ to $h_{\text {container }}-h_{\text {package }}$ do
                if container ( $h, w, l$ ) not empty then
                    skip to next $h$ iteration
                end if
                if $h i j$ then
                    if Fragility and min. support area is not fullfilled then
                        skip to next $w$ iteration
                    end if
                end if
                if LIFO is not fullfilled then
                    skip to next $h$ iteration
                end if
                return found feasible location, ( $h, w, l$ )
            end for
            if there were no future feasible placements left then
                $l_{\text {skip }}=l$
            end if
        end for
    end for
    return no feasible location found
```

| Parameter                                     | Parameter range                 |
| :-------------------------------------------- | :------------------------------ |
| Batch size (training and validation)          | 64, 100, 128                    |
| Learning rate                                 | $1 \mathrm{e}-3,1 \mathrm{e}-4$ |
| Learning rate decay                           | 0.9 per 10000 steps             |
| Epochs                                        | max. 10000 or 120 hours         |
| Gradient norm clipping                        | 0.1, 0.5, 1.0                   |
| Embedding dimensions $d_{h}$                  | 128                             |
| Multi-head attention encoder layers $a$       | 3                               |
| Neurons per multi-head attention layer        | 512                             |
| Multi-head attention heads $l$                | 8                               |
| 2D resizing target ( $w_{c n n}, l_{c n n}$ ) | $(30,60)$                       |
| 2D convolutional layer kernel size            | $(5,5)$                         |
| Single-head attention tanh clipping           | 10                              |
| Greedy baseline update frequency              | 100 epochs                      |
| PPO "minibatches"                             | 3, 5                            |
| PPO clipping $\epsilon$                       | 0.2                             |
| Entropy factor $\alpha$                       | 0.0001                          |
| Penalty factor $p_{\text {vrp }}$             | 1, 2, 10                        |

Notes: The selected parameters are highlighted in bold.

Table 1.: Training parameters

[^0]: Schoepf S. Email: <ss2823@cam.ac.uk>
