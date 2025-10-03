from enum import Enum
from typing import List, Dict, Any, Optional, TypedDict
import os
import json
import logging

logging.basicConfig(filename='task-traker.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


class TaskModel(TypedDict):
    id: str
    description: str
    status: TaskStatus
    createdAt: str
    updatedAt: str


class FileWriteException(Exception):
    pass


class FileReadException(Exception):
    pass



class Constants:
    TASK_FILE_PATH = "tasks.json"



def get_last_id() -> int:
    try:
        __all_data = read_file_to_local()
        if not __all_data:
            return 1
        return int(__all_data[-1].get("id", 0)) + 1
    except Exception:
        return 1


def update_whole_file(task_model: List[Dict[str, Any]]):
    try:
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, Constants.TASK_FILE_PATH)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(task_model, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error("Error updating file:", e)
        raise FileWriteException("Cannot update tasks.json")


def read_file_to_local() -> List[Dict[str, Any]]:
    try:
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, Constants.TASK_FILE_PATH)

        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("[]")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            return json.loads(content) if content else []
    except Exception as e:
        logger.error("Error reading file:", e)
        raise FileReadException("Error reading tasks.json")


def get_data_via_task_id(task_id: str) -> TaskModel:
    try:
        __data = read_file_to_local()
        if not __data:
            raise FileReadException("Error in reading file")

        task = next((t for t in __data if t.get("id") == task_id), None)
        if not task:
            raise ValueError(f"Task not found with id {task_id}")

        return {
            "id": task["id"],
            "description": task["description"],
            "status": TaskStatus(task["status"]),
            "createdAt": task["createdAt"],
            "updatedAt": task["updatedAt"],
        }
    except Exception as e:
        logger.error(e)
        return None


def save_file_to_local(new_task: TaskModel):
    try:
        all_task_list = read_file_to_local()
        current_dir = os.getcwd()
        file_path = os.path.join(current_dir, Constants.TASK_FILE_PATH)

        new_task_dict = new_task.copy()
        new_task_dict["status"] = (
            new_task["status"].value if isinstance(new_task["status"], TaskStatus) else new_task["status"]
        )

        index = next((i for i, t in enumerate(all_task_list) if t.get("id") == new_task["id"]), None)
        if index is not None:
            all_task_list[index] = new_task_dict
        else:
            all_task_list.append(new_task_dict)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(all_task_list, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error("Error writing file:", e)
        raise FileWriteException("Error writing tasks.json")
