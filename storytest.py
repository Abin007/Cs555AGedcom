import unittest
import validator
from prettytable import PrettyTable


class fooTest(unittest.TestCase):
    def test_story_us23(self):
        self.assertEqual(validator.StoryIDUS23(),"No errors found")

    def test_story_us25(self):
        self.assertEqual(validator.StoryIDUS25(),"No error detected.")
    
    def test_story_us30(self):
        x = PrettyTable()
        x.field_names = ['Husband ID', 'Husband Name', 'Wife ID', 'Wife Name']
        x.add_row(['I2', 'Kanye /West/', 'I1', 'Kim /Kardashian/'])
        x.add_row(['I7', 'Bruce /Jenner/', 'I6', 'Kris /Jenner/'])
        x.add_row(['I13', 'Travis /Scott/', 'I12', 'Kylie Jenner'])
        self.assertTrue(validator.StoryIDUS30(), x)
    
    def test_story_us31(self):
        x = PrettyTable()
        x.field_names = ['ID','Name']
        x.add_row(['I8', 'KhloÃ© /Kardashian/'])
        x.add_row(['I9', 'Kourtney /kardashian/'])
        x.add_row(['I10', 'Saint /West/'])
        x.add_row(['I11', 'North /West/'])
        x.add_row(['I14', 'Kendall /Jenner/'])
        x.add_row(['I15', 'Stormi /Webster/'])
        self.assertTrue(validator.StoryIDUS31(), x)


if __name__=='__main__':
    unittest.main()