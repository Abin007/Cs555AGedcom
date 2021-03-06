import unittest
import validator
from prettytable import PrettyTable


class fooTest(unittest.TestCase):
    def test_story_us23(self):
        self.assertEqual(validator.StoryIDUS23(),['US23 - Error : Individual I1 and I16 Might be the same'])

    def test_story_us25(self):
        #us25=set()
        self.assertEqual(validator.StoryIDUS25(),['US25 - Error : Family F4 have children with same name and dob'])

    def test_story_us16(self):
        self.assertEqual(validator.StoryIDUS16(),['US16 - Error : Family F6 has male members with different last names'])

    def test_story_us17(self):
        self.assertEqual(validator.StoryIDUS17(),['US17 - Error : In Family F6 has parents who are married to their children '])
    
    def test_story_us15(self):
        self.assertEqual(validator.StoryIDUS15(),['US15 - Family F4 has more than 15 siblings'])
    
    def test_story_us21(self):
        self.assertEqual(validator.StoryIDUS21(),['US21 - Error : In Family F3 have parents of wrong gender', 'US21 - Error : In Family F6 have parents of wrong gender'])

    def test_story_us22(self):
        self.assertEqual(validator.StoryIDUS22(),'US22 - Error : ID I26 are found to be not unique')

    def test_story_us27(self):
        self.assertEqual(validator.StoryIDUS27(),'US27 - Error : Individual I24 has no ages displayed')

    
    def test_story_us30(self):
        x = PrettyTable()
        x.field_names = ['Husband ID', 'Husband Name', 'Wife ID', 'Wife Name']
        x.add_row(['I2', 'Kanye /West/', 'I1', 'Kim /Kardashian/'])
        x.add_row(['I13', 'Travis /Scott/', 'I14', 'Stormi /Webster/'])
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
        x.add_row(['I12','Kylie /Jenner/'])
        x.add_row(['I15', 'Kendall /Jenner/'])
        x.add_row(['I16', 'Kim /Kardashian/'])
        x.add_row(['I17', 'Rob /Kardashian/'])
        x.add_row(['I18', 'Bilbo /Kardashian/'])
        x.add_row(['I19', 'Katleyn /Kardashian/'])
        x.add_row(['I20', 'Kanya /Kardashian/'])
        x.add_row(['I21', 'Konte /Kardashian/'])
        x.add_row(['I22', 'Krit /Kardashian/'])
        x.add_row(['I23', 'Brian /Kardashian/'])
        x.add_row(['I24', 'Nathan /Kardashian/'])
        x.add_row(['I25', 'Nadia /Kardashian/'])
        x.add_row(['I26', 'Nathaniel /Kardashian/'])
        x.add_row(['I26', 'Rick /Kardashian/'])
        x.add_row(['I28', 'Hailey /Kardashian/'])
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
        self.assertEqual(validator.StoryIDUS01(),['US01 - Error : Individual - I14 Birthday 3 MAR 2021 occurs in the future'])

    def test_story_us02(self):
        self.assertEqual(validator.StoryIDUS02(),['US02 - Error : individual I2 birthdate 2020-02-29 00:00:00 occurs after marriage 2014-07-15 00:00:00', 'US02 - Error : individual I6 birthdate-1955-11-05 00:00:00 occurs after marriage 1954-05-05 00:00:00', 'US02 - Error : individual I14 birthdate-2021-03-03 00:00:00 occurs after marriage 2015-04-19 00:00:00'])

    def test_story_us03(self):
        self.assertEqual(validator.StoryIDUS03(),'US03 - Error : Individual - I5 have death before birthday')

    def test_story_us04(self):
        self.assertEqual(validator.StoryIDUS04(),'US04 - Error : Family - F3 have been divorced before marriage')
    
    def test_story_us05(self):
        self.assertEqual(validator.StoryIDUS05(),'US05 - Error : Individual - I5 have death before marriage')

    def test_story_us06(self):
        self.assertEqual(validator.StoryIDUS06(),'US06 - Error : Individual - I3 have death before divorce')

    def test_story_us07(self):
        self.assertEqual(validator.StoryIDUS07(),'US07 - Error : Individual - I8 have age more than 150 years old')
    
    def test_story_us10(self):
        self.assertEqual(validator.StoryIDUS10(),'US10 - Error : Individual - I2 I4 I6 I7 I14 have been married before 14 years old')

    def test_story_us35(self):
        self.assertEqual(validator.StoryIDUS35(),['US35 - Error : Individual - I18 Birthday 30 MAR 2020 is born recently'])
    
    def test_story_us36(self):
        self.assertEqual(validator.StoryIDUS36(),['US36 - Error : Individual - I8 Birthday 15 APR 2020 died recently'])

    def test_story_us38(self):
        self.assertEqual(validator.StoryIDUS38(),['US38 - Individual - I9 have Birthdays in the next 30 days-2020-04-18 ', 'US38 - Individual - I13 have Birthdays in the next 30 days-2020-04-20 ', 'US38 - Individual - I19 have Birthdays in the next 30 days-2020-05-02 '])

    def test_story_us39(self):
        self.assertEqual(validator.StoryIDUS39(),['US39 - Couple - I13,I14 have anniversaries in the next 30 days'])
            
    def test_story_us32(self):
        self.assertEqual(validator.StoryIDUS32(),['US32 - Multiple Births - 21 OCT 1980 is a multiple birthdate.'])
    
    def test_story_us33(self):
        self.assertEqual(validator.StoryIDUS33(),['US33 - Child Name - Rob /Kardashian/ is an Orphan.', 'US33 - Child Name - Krit /Kardashian/ is an Orphan.', 'US33 - Child Name - Brian /Kardashian/ is an Orphan.'])


        
        
if __name__=='__main__':
    unittest.main()
