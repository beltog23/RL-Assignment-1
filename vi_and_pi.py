### MDP Value Iteration and Policy Iteration
import numpy
import numpy as np
from riverswim import RiverSwim

np.set_printoptions(precision=3)

def bellman_backup(state, action, R, T, gamma, V):
    """
    Perform a single Bellman backup.

    Parameters
    ----------
    state: int
    action: int
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)
    gamma: float
    V: np.array (num_states)

    Returns
    -------
    backup_val: float
    """
    backup_val = 0.0
    ############################
    # YOUR IMPLEMENTATION HERE #
    num_states=V.shape[0]
    print(num_states)
    for nextState in range(num_states):
            backup_val+=T[state,action,nextState]*(R[state,action]+gamma*V[nextState])

    ############################

    return backup_val

def policy_evaluation(policy, R, T, gamma, tol=1e-3):
    """
    Compute the value function induced by a given policy for the input MDP
    Parameters
    ----------
    policy: np.array (num_states)
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)
    gamma: float
    tol: float

    Returns
    -------
    value_function: np.array (num_states)
    """
    num_states, num_actions = R.shape
    value_function = np.zeros(num_states)

    ############################
    # YOUR IMPLEMENTATION HERE #

    while True:
        delta=0
        for currState in range(num_states):
            v=value_function[currState]
            a_prob=policy[currState]
            updatedVal=0
            for currAction in range(num_actions):
                updatedVal=R[currState,currAction]
                for nextState in range(num_states):
                    updatedVal+=gamma*T[currState,currAction,nextState]*value_function[nextState]

            value_function[currState]=updatedVal
            delta = max(delta, abs(v - updatedVal))
        if delta<tol:
            break
    ############################
    return value_function


def policy_improvement(policy, R, T, V_policy, gamma):
    """
    Given the value function induced by a given policy, perform policy improvement
    Parameters
    ----------
    policy: np.array (num_states)
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)
    V_policy: np.array (num_states)
    gamma: float

    Returns
    -------
    new_policy: np.array (num_states)
    """
    num_states, num_actions = R.shape
    new_policy = np.zeros(num_states, dtype=int)

    ############################
    # YOUR IMPLEMENTATION HERE #
    policy_stable=True
    for state in range(num_states):
        Q_arr=np.zeros(num_actions)
        for action in range(num_actions):
            for nextState in range(num_states):
                Q_arr[action]+=T[state,action,nextState]*(R[state,action]+gamma*V_policy[nextState])
        new_policy[state]=np.argmax(Q_arr)

    ############################
    return new_policy


def policy_iteration(R, T, gamma, tol=1e-3):
    """Runs policy iteration.

    You should call the policy_evaluation() and policy_improvement() methods to
    implement this method.
    Parameters
    ----------
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)

    Returns
    -------
    V_policy: np.array (num_states)
    policy: np.array (num_states)
    """
    num_states, num_actions = R.shape
    V_policy = np.zeros(num_states)
    policy = np.zeros(num_states, dtype=int)
    ############################
    # YOUR IMPLEMENTATION HERE #
    while True:
        V_policy=policy_evaluation(policy,R,T,gamma,tol)
        updated_policy=policy_improvement(policy,R,T,V_policy,gamma)
        if np.array_equal(policy,updated_policy):
            break
        policy=updated_policy
    ############################
    return V_policy, policy


def value_iteration(R, T, gamma, tol=1e-3):
    """Runs value iteration.
    Parameters
    ----------
    R: np.array (num_states, num_actions)
    T: np.array (num_states, num_actions, num_states)

    Returns
    -------
    value_function: np.array (num_states)
    policy: np.array (num_states)
    """
    num_states, num_actions = R.shape
    value_function = np.zeros(num_states)
    policy = np.zeros(num_states, dtype=int)
    ############################
    # YOUR IMPLEMENTATION HERE #
    while True:
        delta=0
        for state in range(num_states):
            v = value_function[state]
            Q_values=np.zeros(num_actions)
            for action in range(num_actions):
                Q_values[action]=0
                for next_state in range(num_states):
                    Q_values[action]+=T[state,action, next_state]+R[state,action]+gamma*value_function[next_state]
            value_function[state]=np.max(Q_values)
            delta=max(delta,v-value_function[state])
        if (delta<tol):
            break


    ############################
    return value_function, policy


# Edit below to run policy and value iteration on different configurations
# You may change the parameters in the functions below
if __name__ == "__main__":

    SEED = 1234

    RIVER_CURRENT = 'WEAK'
    assert RIVER_CURRENT in ['WEAK', 'MEDIUM', 'STRONG']
    env = RiverSwim(RIVER_CURRENT, SEED)

    R, T = env.get_model()
    discount_factor = 0.99


    print("\n" + "-" * 25 + "\nBeginning Policy Iteration\n" + "-" * 25)

    V_pi, policy_pi = policy_iteration(R, T, gamma=discount_factor, tol=1e-3)
    print(V_pi)
    #print(bellman_backup(0,1,R,T,discount_factor,V_pi))
    #print(policy_evaluation(policy_pi,R,T,discount_factor,tol=1e-3))
    print([['L', 'R'][a] for a in policy_pi])

    print("\n" + "-" * 25 + "\nBeginning Value Iteration\n" + "-" * 25)

    V_vi, policy_vi = value_iteration(R, T, gamma=discount_factor, tol=1e-3)
    print(V_vi)
    print([['L', 'R'][a] for a in policy_vi])

