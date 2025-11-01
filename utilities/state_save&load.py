import json


def save_state(agent, filename):
    """Saves the state to a file."""
    state = agent.save_state()

    with open(filename, "w") as f:
        json.dump(state, f)


def load_state(agent, filename):
    """Loads the state from a file."""
    with open(filename, "r") as f:
        state = json.load(f)

    return agent.load_state(state)
