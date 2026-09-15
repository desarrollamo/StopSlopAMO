import unittest,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import tool
class Smoke(unittest.TestCase):
    def test_core(self):
        m=tool.MODE
        if m=="uiux": self.assertIn("palette",tool.uiux({"domain":"medical"}))
        elif m=="taste": self.assertLess(tool.taste("linear-gradient linear-gradient")["score"],100)
        elif m=="impec": self.assertFalse(tool.impec("<html></html>")["pass"])
        elif m=="slides": self.assertIn("Deck plan",tool.slides({"title":"X","sections":["A"]}))
        elif m=="design": self.assertIn("# Visual direction",tool.design({"name":"X"}))
        elif m=="humanize": self.assertLess(tool.humanize("This is a game-changer.")["score"],100)
        elif m=="stopslop": self.assertLess(tool.stopslop("Let's dive in.")["score"],100)
        elif m=="diagram": self.assertIn("<svg",tool.diagram({"nodes":[{"id":"a"}],"edges":[]}))
        elif m=="understand":
            with tempfile.TemporaryDirectory() as d:
                (Path(d)/"README.md").write_text("x"); self.assertEqual(tool.understand(d)["files"],1)
        elif m=="library":
            with tempfile.TemporaryDirectory() as d:
                p=Path(d)/"x"; p.mkdir(); (p/"DESIGN.md").write_text("# Alpha"); self.assertEqual(tool.library(d)["count"],1)
if __name__=="__main__": unittest.main()
