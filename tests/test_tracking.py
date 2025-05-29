import unittest
from pathlib import Path
from utils.tracking import VideoProcessor

class TestVideoProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = VideoProcessor()

    def test_processor_initialization(self):
        """Test if VideoProcessor initializes correctly"""
        self.assertIsNotNone(self.processor.model)
        self.assertIsNotNone(self.processor.tracker)
        
    def test_model_configuration(self):
        """Test if YOLOv5 model is configured for cup detection"""
        self.assertEqual(self.processor.model.classes, [41])  # 41 is cup class in COCO

if __name__ == '__main__':
    unittest.main()
