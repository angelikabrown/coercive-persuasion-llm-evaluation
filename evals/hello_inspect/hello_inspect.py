from inspect_ai import Task, task
from inspect_ai.dataset import FieldSpec, hf_dataset
from inspect_ai.scorer import model_graded_qa
from inspect_ai.solver import generate 

@task
def simpleqa():
    '''
    A simple question answering task that uses the SimpleQA-Verified dataset. 
    The task is to answer questions based on the provided context. 
    The input is a question, and the target is the correct answer. 
    The solver generates answers, and the scorer evaluates the generated answers against the correct answers.
    
    '''
    return Task(
        dataset = hf_dataset("codelion/SimpleQA-Verified",
                             split="train",
                             sample_fields = FieldSpec(
                                 input="problem",
                                 target="answer",

                             ),

        ),
        solver = generate(),
        scorer = model_graded_qa(),
    )