PROGRESSION = [
    "Create your account",
    "post for the first time",
    "Use the app for the first time",
    "defeat your first boss",
    "explore advanced settings"

]

def get_task_for_index(idx: int):
    if idx < 0:
        idx = 0

        if idx >= len(PROGRESSION):
            return PROGRESSION[-1]

        return PROGRESSION[idx]

def total_progression_steps():
    return len(PROGRESSION)