from typing import Dict, List
from datetime import datetime
from src.utils import (
    TaskStatus,
    TaskModel,
    save_file_to_local,
    get_data_via_task_id,
    read_file_to_local,
    get_last_id,
    update_whole_file
)

import logging

logging.basicConfig(filename='task-traker.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

def print_task_table(tasks: List[Dict]):
    """Displays tasks in a formatted table using native Python (no external libraries)"""
    headers = ["ID", "Description", "Status", "CreatedAt", "UpdatedAt"]

    col_widths = [len(h) for h in headers]
    for task in tasks:
        col_widths[0] = max(col_widths[0], len(str(task["id"])))
        col_widths[1] = max(col_widths[1], len(task["description"]))
        col_widths[2] = max(col_widths[2], len(task["status"]))
        col_widths[3] = max(col_widths[3], len(task["createdAt"]))
        col_widths[4] = max(col_widths[4], len(task["updatedAt"]))

    row_format = "| " + " | ".join(f"{{:<{w}}}" for w in col_widths) + " |"

    print("-" * (sum(col_widths) + 3 * len(col_widths) + 1))
    print(row_format.format(*headers))
    print("-" * (sum(col_widths) + 3 * len(col_widths) + 1))
    for task in tasks:
        print(row_format.format(
            task["id"],
            task["description"],
            task["status"],
            task["createdAt"],
            task["updatedAt"]
        ))
    print("-" * (sum(col_widths) + 3 * len(col_widths) + 1))

def add_task(task_name: str) -> str:
    try:
        if not task_name:
            logger.error("Task name cannot be empty")
            raise ValueError("Task name cannot be empty")
        else:
            id = str(get_last_id())
            model = TaskModel(
                id=id,
                description=task_name,
                status=TaskStatus.TODO,
                createdAt=datetime.utcnow().isoformat(),
                updatedAt=datetime.utcnow().isoformat()
            )
            save_file_to_local(new_task=model)
            return f"Output: Task added successfully (ID: {id})"
    except Exception as e:
        logger.error(e)
        return str(e)
    

def update_task(task_name: str, task_id: str) -> str:
    try:
        if not task_name or not task_id:
            raise ValueError("Task name and id not found ....")

        model = get_data_via_task_id(task_id=task_id)
        if not model:
            logger.error(f"No Tasks found with id: {task_id}")
            raise ValueError(f"Error in finding Task with id: {task_id}")

        __model = TaskModel(
            id=task_id,
            description=task_name,
            createdAt=model["createdAt"],
            status=model["status"],
            updatedAt=datetime.utcnow().isoformat()
        )
        save_file_to_local(new_task=__model)
        return f"Output: Task updated successfully (ID: {task_id})"
    except Exception as e:
        logger.error(e)
        return str(e)
    

def delete_task(task_id: str) -> str:
    try:
        if not task_id:
            raise ValueError("Task Id Should be present")

        __all_data = read_file_to_local()
        if not __all_data:
            logger.error(f"No Tasks found with id: {task_id}")
            raise ValueError(f"No Tasks found with id: {task_id}")

        index = next((i for i, t in enumerate(__all_data) if t.get("id") == task_id), None)
        if index is None:
            logger.error(f"No Tasks found with id: {task_id}")
            raise ValueError(f"Task with ID {task_id} not found")

        __all_data.pop(index)
        update_whole_file(task_model=__all_data)
        return f"Output: Task deleted successfully (ID: {task_id})"
    except Exception as e:
        logger.error(e)
        return str(e)
    

def mark_in_progress(task_id: str) -> str:
    try:
        if not task_id:
            raise ValueError("Task Id Should be present")

        __all_data = read_file_to_local()
        if not __all_data:
            logger.error(f"No Tasks found with id: {task_id}")
            raise ValueError(f"No Tasks found with id: {task_id}")

        index = next((i for i, t in enumerate(__all_data) if t.get("id") == task_id), None)
        if index is None:
            logger.error(f"No Tasks found with id: {task_id}")
            raise ValueError(f"Task with ID {task_id} not found")

        __all_data[index]["status"] = TaskStatus.IN_PROGRESS.value
        __all_data[index]["updatedAt"] = datetime.utcnow().isoformat()
        update_whole_file(task_model=__all_data)
        return f"Output: Task marked as in-progress (ID: {task_id})"
    except Exception as e:
        logger.error(e)
        return str(e)
    

def mark_in_done(task_id: str) -> str:
    try:
        if not task_id:
            raise ValueError("Task Id Should be present")

        __all_data = read_file_to_local()
        if not __all_data:
            logger.error(f"No Tasks found with id: {task_id}")
            raise ValueError(f"No Tasks found with id: {task_id}")

        index = next((i for i, t in enumerate(__all_data) if t.get("id") == task_id), None)
        if index is None:
            logger.error(f"No Tasks found with id: {task_id}")
            raise ValueError(f"Task with ID {task_id} not found")

        __all_data[index]["status"] = TaskStatus.DONE.value
        __all_data[index]["updatedAt"] = datetime.utcnow().isoformat()
        update_whole_file(task_model=__all_data)
        return f"Output: Task marked as done (ID: {task_id})"
    except Exception as e:
        logger.error(e)
        return str(e)


def list_task(task_status: str = ""):
    try:
        __all_data = read_file_to_local()
        if not __all_data:
            logger.info("No tasks found.")
            return

        filtered = [t for t in __all_data if t["status"] == task_status] if task_status else __all_data

        if not filtered:
            print(f"No tasks with status: {task_status}")
            return

        print_task_table(filtered)
    except Exception as e:
        logger.error(e)
        return str(e)
