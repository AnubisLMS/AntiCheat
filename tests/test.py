import unittest
import os

from mayat.frontends import C, Python, TS_C, TS_Java, TS_Python

C_SAMPLE_DIR = "c_samples"
JAVA_SAMPLE_DIR = "java_samples"
PYTHON_SAMPLE_DIR = "python_samples"

def check_similarity(result):
    for entry in result["result"]:
        assert entry["similarity"] >= 0
        assert entry["similarity"] <= 1

class TestMayat(unittest.TestCase):
    def test_TS_C_frontend(self):
        c_files = [os.path.join(C_SAMPLE_DIR, f) for f in os.listdir(C_SAMPLE_DIR)]
        result = TS_C.main(c_files, "*", 5)
        check_similarity(result)

    def test_TS_Java_frontend(self):
        java_files = [os.path.join(JAVA_SAMPLE_DIR, f) for f in os.listdir(JAVA_SAMPLE_DIR)]
        result = TS_Java.main(java_files, "*", 20)
        check_similarity(result)

    def test_TS_Python_frontend(self):
        python_files = [os.path.join(PYTHON_SAMPLE_DIR, f) for f in os.listdir(PYTHON_SAMPLE_DIR)]
        result = TS_Java.main(python_files, "*", 5)
        check_similarity(result)

if __name__ == '__main__':
    unittest.main()
