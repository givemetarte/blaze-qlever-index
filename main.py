import os
import sys
import random
import string
import subprocess
import argparse
import configparser
from typing import Optional


def generate_random_string(length=6):
    """Generate a random string for server name."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def get_qleverfile_config(endpoint, port, name):
    """
    Define configs for Qleverfile updating base url.
    """
    config = configparser.ConfigParser()

    # [data] section
    config["data"] = {
        "NAME": name,
        "BASE_URL": endpoint,
        "GET_DATA_CMD": (
            f"curl -X POST {endpoint} "
            f'--data-urlencode \'query=CONSTRUCT WHERE {{ hint:Query hint:analytic "true" . hint:Query hint:constructDistinctSPO "false" . ?s ?p ?o }}\' '
            f"-H 'Accept:application/x-turtle' | gzip > blazegraph_data.ttl.gz"
        ),
        "DESCRIPTION": "TTL data from blazegraph",
    }

    # [index] section
    config["index"] = {
        "INPUT_FILES": "*.ttl.gz",
        "CAT_INPUT_FILES": "zcat ${INPUT_FILES}",
        "SETTINGS_JSON": '{"locale": { "language": "ko", "country": "KR", "ignore-punctuation": true }, "ascii-prefixes-only": true, "num-triples-per-batch": 500000 }',
        "STXXL_MEMORY": "10G",
    }

    # [server] section
    config["server"] = {
        "PORT": port,
        "ACCESS_TOKEN": "${data:NAME}",
        "MEMORY_FOR_QUERIES": "10G",
        "CACHE_MAX_SIZE": "6G",
    }

    # [runtime] section
    config["runtime"] = {
        "SYSTEM": "docker",
        "IMAGE": "docker.io/adfreiburg/qlever:latest",
    }

    # [ui] section
    config["ui"] = {
        "UI_CONFIG": name,
    }

    return config


def write_qleverfile(config, file_path):
    """
    Write the Qleverfile configuration to a file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as configfile:
        config.write(configfile)


def run_command(
    command: str, show_output: Optional[bool] = False, cwd: Optional[str] = None
):
    """
    Run the command in the shell and show the output if show_output is True.
    """
    try:
        result = subprocess.run(
            command.split(), check=True, capture_output=True, text=True, cwd=cwd
        )

        if show_output:
            print(result.stdout)
            # print(result.stderr)

        return True  # Command succeeded

    except subprocess.CalledProcessError as e:
        print("Error occurred while executing command:", e)

        return False  # Command failed


def main():
    parser = argparse.ArgumentParser(
        description="Update SPARQL endpoint and run data command."
    )
    parser.add_argument(
        "--name",
        type=str,
        default=generate_random_string(),
        help="The name of the index server.",
    )
    parser.add_argument("--endpoint", type=str, help="The new SPARQL endpoint URL.")
    parser.add_argument(
        "--port", type=int, default=7000, help="The port number for the index server."
    )
    args = parser.parse_args()

    if run_command("docker info"):
        print("### Docker is running.\n")
    else:
        print(
            "### It looks like Docker is not running. Please start Docker and try again."
        )
        sys.exit(1)

    index_dir = "index"
    qleverfile_path = os.path.join(index_dir, "Qleverfile")

    if args.endpoint:
        print("### New endpoint provided:", args.endpoint, "\n")

        # write the Qleverfile configuration
        data = get_qleverfile_config(args.endpoint, args.port, args.name)
        write_qleverfile(data, qleverfile_path)
        print("### Qleverfile is generated.\n")

        # run the command to get data
        run_command("qlever get-data", show_output=True, cwd=index_dir)
        print("### Data is downloaded.\n")

        # run the command to index data
        run_command("qlever index", show_output=True, cwd=index_dir)
        print("### Index build is completed.\n")

        # run the command to start qlever
        run_command("qlever start", show_output=True, cwd=index_dir)
        print(f"### Index server is ready. Go to localhost:{args.port}.\n")
    else:
        print("### No endpoint provided.\n")


if __name__ == "__main__":
    main()
