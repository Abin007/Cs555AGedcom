import unittest
import validator
from prettytable import PrettyTable


class fooTest(unittest.TestCase):
    def test_story_us23(self):
        self.assertEqual(validator.StoryIDUS23(),['US23 - Error : Individual I1 and I16 Might be the same'])

    def test_story_us25(self):
        us25=set()
        self.assertEqual(validator.StoryIDUS25(),['US25 - Error : Individual I1 I16 might be the same  in Family F4'])

    def test_story_us16(self):
        self.assertEqual(validator.StoryIDUS16(),['US16 - Error : Family F6 has male members with different last names'])

    def test_story_us17(self):
        self.assertEqual(validator.StoryIDUS17(),['US17 - Error : In Family F6 has parents who are married to their children '])
    
    def test_story_us30(self):
        x = PrettyTable()
        x.field_names = ['Husband ID', 'Husband Name', 'Wife ID', 'Wife Name']
        x.add_row(['I2', 'Kanye /West/', 'I1', 'Kim /Kardashian/'])
        x.add_row(['I7', 'Bruce /Jenner/', 'I6', 'Kris /Jenner/'])
        x.add_row(['I13', 'Travis /Scott/', 'I15', 'Stormi /Webster/'])
        self.assertEqual(str(validator.StoryIDUS30()), str(x))
        y = PrettyTable()
        y.field_names = ['Husband ID', 'Husband Name', 'Wife ID', 'Wife Name']
        y.add_row(['I20', 'Kanye /West/', 'I1', 'Kim /Kardashian/'])
        y.add_row(['I7', 'Bruce /Jenner/', 'I6', 'Kris /Jenner/'])
        y.add_row(['I13', 'Prateek /Jani/', 'I12', 'Kylie /Jenner/'])
        self.assertNotEqual(str(validator.StoryIDUS30()), str(y))
    
    def test_story_us31(self):
        x = PrettyTable()
        x.field_names = ['ID','Name']
        x.add_row(['I8', 'Khloe /Kardashian/'])
        x.add_row(['I9', 'Kourtney /Kardashian/'])
        x.add_row(['I10', 'Saint /West/'])
        x.add_row(['I11', 'North /West/'])
        x.add_row(['I14', 'Kendall /Jenner/'])
        x.add_row(['I15', 'Stormi /Webster/'])
        x.add_row(['I16', 'Kim /Kardashian/'])
        self.assertEqual(str(validator.StoryIDUS31()), str(x))
        
        y = PrettyTable()
        y.field_names = ['ID','Name']
        y.add_row(['I8', 'Khloe /Kardashian/'])
        y.add_row(['I9', 'Kourtney /Kardashian/'])
        y.add_row(['I10', 'Saint /West/'])
        y.add_row(['I11', 'North /West/'])
        y.add_row(['I14', 'Kendall /Jenner/'])
        y.add_row(['I15', 'Prateek /Jani/'])
        y.add_row(['I16', 'Kim /Kardashian/'])
        self.assertNotEqual(str(validator.StoryIDUS31()),str(y))

    def test_story_us01(self):
        self.assertEqual(validator.StoryIDUS01(),['US01 - Error : Individual - I15 Birthday 3 MAR 2021 occurs in the future'])

    def test_story_us02(self):
        self.assertEqual(validator.StoryIDUS02(),['US02 - Error : individual I6 birthdate-1955-11-05 00:00:00 occurs after marriage 1954-05-05 00:00:00', 'US02 - Error : individual I15 birthdate-2021-03-03 00:00:00 occurs after marriage 2015-07-19 00:00:00'])

    def test_story_us03(self):
        self.assertEqual(validator.StoryIDUS03(),['US03 - Error : Individual - I5 have death before birthday'])

    def test_story_us04(self):
        self.assertEqual(validator.StoryIDUS04(),['US04 - Error : Family - F3 have been married after divorce'])
    
    def test_story_us35(self):
        self.assertEqual(validator.StoryIDUS35(),'[ US35 - There are no recent births ]')
    
    def test_story_us36(self):
        self.assertEqual(validator.StoryIDUS36(),'[ US36 - There are no recent deaths ]')

        
        
if __name__=='__main__':
    unittest.main()
