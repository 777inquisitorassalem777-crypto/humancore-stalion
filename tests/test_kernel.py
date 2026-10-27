from ccos.kernel import CCOSKernel
from ccos.benchmark import generate_tasks

def test_process_advances_cycle_and_returns_components():
    kernel = CCOSKernel()
    result = kernel.process("I promised Mira I would protect the village.")
    assert result["cycle"] == 1
    assert result["event"]["text"].startswith("I promised")
    assert result["hypotheses"]
    assert "soul_emergence_index" in result

def test_status_and_benchmark_generation():
    kernel = CCOSKernel()
    kernel.process("The river flooded the village road.")
    assert kernel.status()["memory_size"] == 1
    tasks = generate_tasks(100)
    assert len(tasks) == 100
    assert len({task.task_id for task in tasks}) == 100
