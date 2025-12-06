"""Main entry point for TaskLang Compiler."""

from .cli import TaskLangCLI


def main():
    """Main function that delegates to TaskLangCLI."""
    cli = TaskLangCLI()
    cli.run()


if __name__ == "__main__":
    main()

