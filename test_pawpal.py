from pawpal_system import Task, Pet


def test_task_mark_complete():
    t = Task(title="Test Task", duration_minutes=5)
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_pet_add_task_increases_count():
    p = Pet(name="TestPet", species="Dog", age=2)
    assert len(p.tasks) == 0
    t = Task(title="Feed", duration_minutes=10)
    p.add_task(t)
    assert len(p.tasks) == 1
    assert p.tasks[0] is t
