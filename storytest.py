import unittest
import validator
from prettytable import PrettyTable


class fooTest(unittest.TestCase):
    def test_story_us23(self):
        self.assertEqual(validator.StoryIDUS23(),['US23 - Error : Individual I1 and I16 Might be the same'])

    def test_story_us25(self):
        us25=set()
        self.assertEqual(validator.StoryIDUS25(),['US25 - Error : Individual I1 I16 might be the same  in Family F4'] )
    
    def test_story_us30(self):
        x = PrettyTable()
        x.field_names = ['Husband ID', 'Husband Name', 'Wife ID', 'Wife Name']
        x.add_row(['I2', 'Kanye /West/', 'I1', 'Kim /Kardashian/'])
        x.add_row(['I7', 'Bruce /Jenner/', 'I6', 'Kris /Jenner/'])
        x.add_row(['I13', 'Travis /Scott/', 'I12', 'Kylie Jenner'])
        self.assertTrue(validator.StoryIDUS30(), x)
        y = PrettyTable()
        y.field_names = ['Husband ID', 'Husband Name', 'Wife ID', 'Wife Name']
        y.add_row(['I20', 'Kanye /West/', 'I1', 'Kim /Kardashian/'])
        y.add_row(['I7', 'Bruce /Jenner/', 'I6', 'Kris /Jenner/'])
        y.add_row(['I13', 'Prateek /Jani/', 'I12', 'Kylie Jenner'])
        self.assertFalse(validator.StoryIDUS30(), y)
    
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

    def test_story_us01(self):
        self.assertEqual(validator.StoryIDUS01(),['US01 - Error : Individual ID - I15 Birthday 3 MAR 2021 occurs in the future'])

    def test_story_us02(self):
        self.assertEqual(validator.StoryIDUS02(),['US02 - Error : individual I6 birthdate occurs before marriage'])


if __name__=='__main__':
    unittest.main()