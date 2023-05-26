#!/usr/bin/python

import os

from src.utils import flush_spacer


def main():
    import inquirer
    import re

    aws_file = "~/.aws/credentials"
    credentials = os.path.expanduser(aws_file)

    if os.path.isfile(credentials):
        print("AWS credentials detected: {}".format(aws_file))
    else:
        questions = [
            inquirer.Text(
                "aws_access_key_id",
                message="AWS Access Key ID",
                validate=lambda _, x: re.match(
                    "(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])", x
                ),
            ),
            inquirer.Password(
                "aws_secret_access_key",
                message="AWS Secret Access Key",
                echo="*",
                validate=lambda _, x: re.match(
                    "(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])", x
                ),
            ),
        ]

        answers = inquirer.prompt(questions)
        config = "[default]\naws_access_key_id={}\naws_secret_access_key={}\n".format(
            answers["aws_access_key_id"], answers["aws_secret_access_key"]
        )

        # Write Config File
        with open(credentials, "w") as outfile:
            outfile.write(config)

        print("AWS credentials saved: {}".format(aws_file))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print("Exited Application")
        exit(0)
