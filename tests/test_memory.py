from ccos.models import NarrativeEvent
from ccos.memory import NarrativeMemory

def test_memory_records_and_recalls_matching_event():
    memory = NarrativeMemory()
    event = NarrativeEvent(text="Mira hid the key under the blue stone", cycle=1, importance=0.9, emotion=0.7)
    memory.record(event)
    results = memory.recall("where is the key under blue stone", current_cycle=1, limit=3)
    assert results
    assert results[0][0].id == event.id
    assert results[0][1] > 0

def test_memory_gravity_decays_with_age():
    memory = NarrativeMemory()
    event = NarrativeEvent(text="village bridge damaged", cycle=1, importance=0.8)
    memory.record(event)
    recent_score = memory.gravity_score("village bridge", event, current_cycle=1)
    old_score = memory.gravity_score("village bridge", event, current_cycle=100)
    assert recent_score > old_score
