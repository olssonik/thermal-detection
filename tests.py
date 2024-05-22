import os
from main import main, read

def test_video():
    main("test.mp4")
    assert read() == True

def test_output():
    assert len(os.listdir("out/")) >= 1


