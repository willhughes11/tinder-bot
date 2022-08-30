import argparse

def get_input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--remote', type=bool)

    args = parser.parse_args()

    return args