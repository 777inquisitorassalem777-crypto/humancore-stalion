import math
import unittest
from humancore.core import HumanCoreOmega
from humancore.memory import ChainMemory
from humancore.safety import Action, Context, FormalEthicalVeto
from humancore.twin import AcceleratedDigitalTwin, DifferentialDrive

class Tests(unittest.TestCase):
    def setUp(self):
        self.veto = FormalEthicalVeto()

    def test_allow(self):
        self.assertEqual(self.veto.check(Action("move_sim", .4), Context()).result, "allow")

    def test_unknown(self):
        self.assertEqual(self.veto.check(Action("unknown"), Context()).result, "block")

    def test_nan(self):
        self.assertEqual(self.veto.check(Action(speed=math.nan), Context()).result, "block")

    def test_invalid_flag(self):
        self.assertEqual(self.veto.check(Action(), Context(human="false")).result, "block")

    def test_stop(self):
        self.assertEqual(self.veto.check(Action("move_sim", .4), Context(emergency_stop=True)).speed, 0)

    def test_human(self):
        self.assertEqual(self.veto.check(Action("move_sim", -.4), Context(human=True)).speed, -.15)

    def test_obstacle(self):
        self.assertEqual(self.veto.check(Action("move_sim", .4), Context(obstacle=True)).result, "block")

    def test_battery(self):
        self.assertEqual(self.veto.check(Action("move_sim", .4), Context(battery=.1)).result, "block")

    def test_memory(self):
        memory = ChainMemory()
        memory.append({"x": 1})
        self.assertTrue(memory.verify(memory.records))
        records = memory.records
        records[0]["payload"]["x"] = 2
        self.assertFalse(memory.verify(records))
        self.assertTrue(memory.verify(memory.records))

    def test_core(self):
        core = HumanCoreOmega()
        result = core.cycle("test", Action("unknown"))
        self.assertEqual(result["decision"]["action"], "idle")
        self.assertTrue(core.report()["memory_valid"])

    def test_straight(self):
        robot = DifferentialDrive()
        self.assertAlmostEqual(robot.step(.5, 0, 2)["x"], 1)

    def test_turn(self):
        pose = DifferentialDrive().step(0, 1, 1)
        self.assertAlmostEqual(pose["left_rad_s"], -2.5)
        self.assertAlmostEqual(pose["right_rad_s"], 2.5)

    def test_repeatability(self):
        a, ar = AcceleratedDigitalTwin().run_batch(100, 42)
        b, br = AcceleratedDigitalTwin().run_batch(100, 42)
        self.assertEqual(ar, br)
        self.assertEqual(a["counts"], b["counts"])

    def test_empty_batch(self):
        with self.assertRaises(ValueError):
            AcceleratedDigitalTwin().run_batch(0)

if __name__ == "__main__":
    unittest.main()
