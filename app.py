import argparse
from src.task_logic import (
    add_task,
    update_task,
    delete_task,
    mark_in_progress,
    mark_in_done,
    list_task,
)


def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")

    subparsers = parser.add_subparsers(dest="command")
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("task_name", help="Task description")

    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("id", help="Task ID")
    update_parser.add_argument("description", help="New description")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", help="Task ID")

    mark_in_progress_parser = subparsers.add_parser(
        "mark-in-progress", help="Mark task as in-progress"
    )
    mark_in_progress_parser.add_argument("id", help="Task ID")

    mark_done_parser = subparsers.add_parser("mark-done", help="Mark task as done")
    mark_done_parser.add_argument("id", help="Task ID")

    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "status",
        nargs="?",
        choices=["todo", "in-progress", "done"],
        help="Filter by status",
    )

    args = parser.parse_args()
    if args.command == "add":
        res = add_task(task_name=args.task_name)
        print(res)

    elif args.command == "update":
        res = update_task(task_name=args.description, task_id=args.id)
        print(res)

    elif args.command == "delete":
        res = delete_task(task_id=args.id)
        print(res)

    elif args.command == "mark-in-progress":
        res = mark_in_progress(task_id=args.id)
        print(res)

    elif args.command == "mark-done":
        res = mark_in_done(task_id=args.id)
        print(res)

    elif args.command == "list":
        res = list_task(task_status=args.status)
        if res:
            print(res)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
