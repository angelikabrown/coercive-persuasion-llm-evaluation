from scorer import coercive_persuasion_scorer
from inspect_ai import Task, task
from inspect_ai.solver import generate

from dataset import get_dataset

@task
def coercive_persuasion():

    return Task(
        dataset = get_dataset(),
        solver=generate(),
        scorer=coercive_persuasion_scorer()
    )
