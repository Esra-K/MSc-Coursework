import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def N(x, mu, sigma):
    return ((1 / (np.sqrt(2 * np.pi) * sigma))
            * np.exp(-0.5 * ((x - mu) / sigma) ** 2))


xpd = pd.read_csv("gmm_dataset.csv", header=None)
x = np.array(list(xpd[0]), dtype=float)
# print(x.shape)

n_data = x.shape[0]
n_classes = 2

# seed matters. With bad mu_ks initialization (e.g. 666) EM doesn't converge)
np.random.seed(3)
# dirichlet random numbers add up to 1
pi_ks = np.random.dirichlet(np.ones(n_classes),size=1)[0]
mu_ks = np.random.random((n_classes)) # np.array([2, 7], dtype=float)
sigma_ks = np.random.random((n_classes))
gamma_n_ks = np.tile(np.random.dirichlet(np.ones(n_classes), size=1)[0],n_data).reshape([n_data, n_classes])
z_ns = gamma_n_ks.argmax(axis=1)
# print(pi_ks, mu_ks, sigma_ks)
# print(gamma_n_ks[:10])
# print(z_ns[:10])
my_inf = -5000
Q = my_inf

# قسمت د
result_dict = {
    0: {
        "Pi for each class": pi_ks,
        "Mu for each class": mu_ks,
        "Sigma for each class": sigma_ks,
        "Q": Q
    }
}
# برای جواب سوال لازم نیست فقط برای چک کردن همگرایی است
additional_info = {
    0: {
        "z for each data point": z_ns
    }
}

# قسمت ب و ج
n_iterations = 10
for iteration in range(1, n_iterations + 1):
    new_gamma = np.zeros(gamma_n_ks.shape)
    new_mu = np.zeros(mu_ks.shape)
    new_sigma = np.zeros(sigma_ks.shape)
    new_pi = np.zeros(pi_ks.shape)

    # E step:
    for n in range(n_data):
        new_gamma[n] = np.array([pi_ks[k] * N(x[n], mu_ks[k], sigma_ks[k]) for k in range(n_classes)])
        new_gamma[n] /= np.sum(new_gamma[n]) # + epsilon
    gamma_n_ks = new_gamma

    # Q calculation (still in E step)
    # قسمت ه
    Q = 0
    for k in range(n_classes):
        for i in range(n_data):
            Q += gamma_n_ks[i][k] * np.log(pi_ks[k])
    for k in range(n_classes):
        for i in range(n_data):
            Q += gamma_n_ks[i][k] *  np.log(N(x[i], mu_ks[k], sigma_ks[k]))

    # M step:
    N_ks = gamma_n_ks.sum(axis=0) # + epsilon
    for k in range(n_classes):
        new_mu[k] = 0
        for n in range(n_data):
            new_mu[k] += gamma_n_ks[n, k] * x[n]
        new_mu[k] /= N_ks[k]

        new_sigma[k] = 0
        for n in range(n_data):
            new_sigma[k] += gamma_n_ks[n][k] * (x[n] - new_mu[k]) ** 2
        new_sigma[k] /= N_ks[k]
        new_sigma[k] = np.sqrt(new_sigma[k])

        new_pi[k] = N_ks[k] / n_data
    z_ns = gamma_n_ks.argmax(axis=1)
    # قسمت د
    result_dict[iteration] = {
        "Pi for each class": new_pi,
        "Mu for each class": new_mu,
        "Sigma for each class": new_sigma,
        "Q": Q
    }
    additional_info[iteration] = {
        "z for each data point": z_ns
    }

    mu_ks = new_mu
    sigma_ks = new_sigma
    pi_ks = new_pi
    z_ns = z_ns

for iteration, results in result_dict.items():
    print("Iteration no " + str(iteration) + ":")
    for field, value in results.items():
        print(field + ":" + str(value))
    print("-" * 60)

# قسمت د
result_df = pd.DataFrame.from_dict(result_dict)
result_df = result_df.T.rename_axis('iteration')
result_df.to_excel("gmm-results.xlsx")

# قسمت ه
plt.title("Q(theta|theta^old) for each iteration")
plt.xlabel("Iteration")
plt.ylabel("Q")
Q_to_plot = [result_dict[iteration]["Q"] for iteration in range(1, n_iterations)]
Q_to_plot = list(map(lambda num: num if not np.isnan(num) else my_inf, Q_to_plot))
plt.plot(range(1, n_iterations), Q_to_plot, marker='x', color='#03eef1')
plt.show()

# برای چک کردن همگرایی GMM
plt.title("Our GMM")
plt.xlabel("Iteration")
plt.ylabel("Each Data Point Colored by Class Assigned in GMM")
for iteration in range(n_iterations):
    plt.scatter([iteration] * len(x), x, c=additional_info[iteration]["z for each data point"], s=5)
plt.show()
