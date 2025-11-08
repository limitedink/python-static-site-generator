import unittest
import os
from gencontent import generate_page, extract_title


class TestGenContent(unittest.TestCase):
    def test_extract_title_basic(self):
        md = "# Hello\n\n## Sub"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_raises_without_h1(self):
        with self.assertRaises(Exception):
            extract_title("No title here\n## Sub")

    def test_generate_page_writes_file_flat_path(self):
        mdp, tp, outp = "t_i.md", "t_t.html", "t_out.html"
        try:
            with open(mdp, "w") as f:
                f.write("# Title\n\nHello")
            with open(tp, "w") as f:
                f.write("<title>{{ Title }}</title><article>{{ Content }}</article>")
            generate_page(mdp, tp, outp)
            self.assertTrue(os.path.exists(outp))
            with open(outp) as f:
                html = f.read()
            self.assertIn("<title>Title</title>", html)
            self.assertIn("<article>", html)
        finally:
            for p in (mdp, tp, outp):
                if os.path.exists(p):
                    os.remove(p)


if __name__ == "__main__":
    unittest.main()
