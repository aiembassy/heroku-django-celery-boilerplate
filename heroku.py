#!/usr/bin/env python
"""A CLI interface for running the Heroku commands in a proper context"""

from pathlib import Path

import subprocess
import dotenv
import sys


def get_or_create_heroku_config(config_name, config_value, environment_name):
    """Checks is provided config variable is set, and if not, creates it."""
    result = subprocess.run([
        "heroku", "config:get", config_name, "--remote", environment_name],
        capture_output=True, encoding="utf-8"
    )
    current_value = result.stdout.strip()
    if len(current_value) > 0:
        return 0

    return subprocess.run(
        ["heroku", "config:set", f"{config_name}={config_value}", "--remote",
         environment_name]
    ).returncode

# Check current git branch for the further processing
result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                        capture_output=True, encoding="utf-8")
if 0 != result.returncode:
    print("Could not check the current git branch. "
          "Are you already in a git repository?")
    exit(result.returncode)

# Extract the target Heroku environment, if possible. Otherwise, all the changes
# will be done on the local development environment only.
current_branch = result.stdout.strip()
env_variables = dotenv.main.DotEnv(Path("./.boilerplate/.branches"))
target_env = env_variables.get(current_branch)

# Find a proper command to be called
if "deploy" == sys.argv[1]:
    target_env_variables = dotenv.main.DotEnv(f".env.{target_env}")
    for variable_name, variable_value in target_env_variables.dict().items():
        get_or_create_heroku_config(variable_name, variable_value, target_env)
    target_command = ["git", "push", target_env, current_branch]
else:
    target_command = ["heroku"] + sys.argv[1:] + ["--remote", target_env]

# Run the target command and display the results
exit(subprocess.run(target_command).returncode)
