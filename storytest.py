import unittest
import validator


class fooTest(unittest.TestCase):
    def test_story_us23(self):
        self.assertEqual(validator.StoryIDUS23(),"Error : Might be the same I1:Kim Kardashian and I16:Kim Kardashian")

    def test_story_us25(self):
        self.assertEqual(validator.StoryIDUS25(),"family Id F4 has same name - ['Robert', 'Kris', 'Kim', 'Khloé', 'Kourtney', 'Kim']")
    
    def test_story_us30(self):
        print("Testing in progress")
    
    def test_story_us31(self):
        print("Testing in progress")


if __name__=='__main__':
    unittest.main()