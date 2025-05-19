"""
Author: Jason Yang
Starting Date: 05/14/2025

Test cases for the Gale-Shapely experimental setup
"""

from experiment import Student, Group, calculate_average_happiness
import math

# Part 1
# -------------------------------------------------------------

def test_student_constructor():
    """
    Test cases for the Student constructor
    """
    # Create some test students, with names and rankings of prefered partners
    # Note that we do not include a group, so the partner_ratings
    #   list is permitted to include names of otherwise-undefined students
    # NOTE: you may use any of these students when writing test cases
    #  or you can construct new students instead
    s0 = Student(None, 'Jason', ['Riley', 'Ryan'])
    s1 = Student(None, 'Joy', ['Ryan', 'Riley', 'Richard'])
    s2 = Student(None, 'Ryan', ['Joy', 'Jason'])
    s3 = Student(Group([], []), 'Riley', [])

    # Test that "None" values are set explicitly
    # NOTE: we use "is None" rather than "== None" to test a value is None
    assert s0.group is None, f'Expected None, got {s0.group}'
    assert s0.partner is None, f'Expected None, got {s0.partner}'

    # Check that the other fields are set
    result = s0.name
    expected = 'Jason'
    assert expected == result, f'expected {expected}, got {result}'

    result = s0.partner_ratings
    expected = ['Riley', 'Ryan']
    assert expected == result, f'expected {expected}, got {result}'

    result = s0.to_propose
    expected = []
    assert expected == result, f'expected {expected}, got {result}'

    # Test that the group is set if given
    assert s3.group is not None, f'Group not set when given'

    result = s3.name
    expected = 'Riley'
    assert expected == result, f'expected {expected}, got {result}'

    result = s1.partner_ratings
    expected = ['Ryan', 'Riley', 'Richard']
    assert expected == result, f'expected {expected}, got {result}'

    print("tests for student constructor passed")


def test_student_str():
    """
    Test cases for the student string representation
    """
    # Create some test students, with names and rankings of prefered partners
    # Note that we do not include a group, so the partner_ratings
    #   list is permitted to include names of otherwise-undefined students
    # NOTE: you may use any of these students when writing test cases
    #  or you can construct new students instead
    s0 = Student(None, 'Jason', ['Riley', 'Ryan'])
    s1 = Student(None, 'Joy', ['Ryan', 'Riley', 'Richard'])
    s2 = Student(None, 'Ryan', ['Joy', 'Jason'])
    s3 = Student(Group([], []), 'Riley', [])
    s4 = Student(Group([], []), 'Jayden', ['Riley', 'Jason'])

    # Check that adding a partner gives that name back
    s0.partner = s1

    expected = 'Jason (Joy)'
    result = str(s0)
    assert expected == result, f'Expected {expected}, got {result}'

    expected = 'Ryan (no-one)'
    result = str(s2)
    assert expected == result, f'Expected {expected}, got {result}'

    s3.partner = s4
    expected = 'Riley (Jayden)'
    result = str(s3)
    assert expected == result, f'Expected {expected}, got {result}'

    print("tests for student string representation passed")


def test_has_partner():
    """
    Test cases for has_partner
    """
    # Create some test students, with names and rankings of prefered partners
    # Note that we do not include a group, so the partner_ratings
    #   list is permitted to include names of otherwise-undefined students
    # NOTE: you may use any of these students when writing test cases
    #  or you can construct new students instead
    s0 = Student(None, 'Jason', ['Riley', 'Ryan'])
    s1 = Student(None, 'Joy', ['Ryan', 'Riley', 'Richard'])
    s2 = Student(None, 'Ryan', ['Joy', 'Jason'])
    s3 = Student(Group([], []), 'Riley', [])

    # No partner case
    expected = False
    result = s0.has_partner()
    assert expected == result, f'Expected {expected}, got {result}'

    s1.partner = s2
    expected = True
    result = s1.has_partner()
    assert expected == result, f'Expected {expected}, got {result}'

    expected = False
    result = s3.has_partner()
    assert expected == result, f'Expected {expected}, got {result}'

    print("tests for has_partner passed")


def test_get_rating_of_name():
    """
    Test cases for get_rating_of_name
    """
    # Create some test students, with names and rankings of prefered partners
    # Note that we do not include a group, so the partner_ratings
    #   list is permitted to include names of otherwise-undefined students
    # NOTE: you may use any of these students when writing test cases
    #  or you can construct new students instead
    s0 = Student(None, 'Jason', ['Riley', 'Ryan'])
    s1 = Student(None, 'Joy', ['Ryan', 'Riley', 'Richard'])
    s2 = Student(None, 'Ryan', ['Joy', 'Jason'])
    s3 = Student(Group([], []), 'Riley', [])

    # Ratings for a two-element rating list
    expected = 0
    result = s0.get_rating_of_name('Riley')
    assert expected == result, f'Expected {expected}, got {result}'

    expected = 1
    result = s0.get_rating_of_name('Ryan')
    assert expected == result, f'Expected {expected}, got {result}'

    expected = -1
    result = s2.get_rating_of_name('Riley')
    assert expected == result, f'Expected {expected}, got {result}'

    expected = 2
    result = s1.get_rating_of_name('Richard')
    assert expected == result, f'Expected {expected}, got {result}'

    print("tests for get_rating_of_name passed")


def test_get_rating_of_current_partner():
    """
    Test cases for get_rating_of_current_partner
    """
    # Create some test students, with names and rankings of prefered partners
    # Note that we do not include a group, so the partner_ratings
    #   list is permitted to include names of otherwise-undefined students
    # NOTE: you may use any of these students when writing test cases
    #  or you can construct new students instead
    s0 = Student(None, 'Jason', ['Riley', 'Ryan'])
    s1 = Student(None, 'Joy', ['Ryan', 'Riley', 'Richard'])
    s2 = Student(None, 'Ryan', ['Joy', 'Jason'])
    s3 = Student(Group([], []), 'Riley', [])

    # Rating for the no-partner case
    expected = -1
    result = s0.get_rating_of_current_partner()
    assert expected == result, f'Expected {expected}, got {result}'

    # Rating if we have a partner
    s0.partner = s2
    expected = 1
    result = s0.get_rating_of_current_partner()
    assert expected == result, f'Expected {expected}, got {result}'

    s3.partner = s0
    expected = -1
    result = s3.get_rating_of_current_partner()
    assert expected == result, f'Expected {expected}, got {result}'

    s1.partner = s2
    expected = 0
    result = s1.get_rating_of_current_partner()
    assert expected == result, f'Expected {expected}, got {result}'

    print("tests for get_rating_of_current_partner passed")


def test_break_partnership():
    """
    Test cases for break_partnership
    """
    # Create some test students, with names and rankings of prefered partners
    # Note that we do not include a group, so the partner_ratings
    #   list is permitted to include names of otherwise-undefined students
    # NOTE: you may use any of these students when writing test cases
    #  or you can construct new students instead
    s0 = Student(None, 'Jason', ['Riley', 'Ryan'])
    s1 = Student(None, 'Joy', ['Ryan', 'Riley', 'Richard'])
    s2 = Student(None, 'Ryan', ['Joy', 'Jason'])
    s3 = Student(Group([], []), 'Riley', [])

    # Manually create a partnership, and break it
    s0.partner = s1
    s1.partner = s0

    s0.break_partnership()

    # Both Students should now not have a partner
    # Note that we should have already tested has_partner
    assert not s0.has_partner(), f'Partnership not broken for original student'
    assert not s1.has_partner(), f'Partnership not broken for former partner'

    assert not s2.has_partner(), f'Partnership not broken for original student'
    assert not s3.has_partner(), f'Partnership not broken for former partner'

    print("tests for break_partnership passed")


def test_make_partnership():
    """
    Test cases for make_partnership
    """

    # Create some test students, with names and rankings of prefered partners
    # Note that we do not include a group, so the partner_ratings
    #   list is permitted to include names of otherwise-undefined students
    s0 = Student(None, 'Jason', ['Riley', 'Ryan'])
    s1 = Student(None, 'Joy', ['Ryan', 'Riley', 'Richard'])
    s2 = Student(None, 'Ryan', ['Joy', 'Jason'])
    s3 = Student(Group([], []), 'Riley', [])

    # Make a simple partnership
    s0.make_partnership(s2)

    # First, make sure we have a partner
    assert s0.has_partner(), f'No partner was assigned for given student'
    assert s2.has_partner(), f'No partner was assigned for other student'

    # Then, make sure it's the correct partner for each
    expected = 'Ryan'
    result = s0.partner.name
    assert expected == result, f'Expected {expected}, got {result}'

    expected = 'Jason'
    result = s2.partner.name
    assert expected == result, f'Expected {expected}, got {result}'

    # Make another partnership (which should break the old one)
    s0.make_partnership(s3)

    # First, make sure we updated each partner
    assert s0.has_partner(), f'No partner was assigned for given student'
    assert s3.has_partner(), f'No partner was assigned for other student'
    assert not s2.has_partner(), f'Partnership was not broken for previous partner'

    # Then, make sure we have the correct new partner name
    expected = 'Riley'
    result = s0.partner.name
    assert expected == result, f'Expected {expected}, got {result}'

    expected = 'Jason'
    result = s3.partner.name
    assert expected == result, f'Expected {expected}, got {result}'

    print("tests for make_partnership passed")


# Part 2
# -------------------------------------------------------------

def test_get_unpartnered():
    """
    Test cases for get_rating_of_name
    """

    # Create a Group of 5 students in each of A and B
    # As a reminder, this shuffles the names of the students
    student_names_a = ['Ana', 'Avery', 'Alastair', 'Amelia', 'Abby']
    student_names_b = ['Bailey', 'Brian', 'Beverly', 'Bob', 'Biyu']
    student_group = Group(student_names_a, student_names_b)

    # Check that every student in A is initially unpartnered
    expected = 5
    result = student_group.get_unpartnered()
    assert expected == len(result), f'Expected that all students were unpartnered, got a list {result}'

    # partner a student at random
    student_group.students_a[0].make_partnership(student_group.students_b[0])

    expected = 4
    result = student_group.get_unpartnered()
    assert expected == len(result), f'Expected that 4/5 students were unpartnered, got a list {result}'

    # partner all students at random
    for i in range(1, 5):
        student_group.students_a[0].make_partnership(
            student_group.students_b[0])

    expected = []
    result = student_group.get_unpartnered()
    assert expected == [], f'Expected that all students were partnered, got a list {result}'

    print("tests for get_unpartnered passed")


def test_make_naive_partnerships():
    """
    Test cases for get_rating_of_name
    """

    # Create a Group of 5 students in each of A and B
    student_names_a = ['Ana', 'Avery', 'Alastair', 'Amelia', 'Abby']
    student_names_b = ['Bailey', 'Brian', 'Beverly', 'Bob', 'Biyu']
    student_group = Group(student_names_a, student_names_b)

    # Set ratings explicitly for testing to avoid randomness
    student_group.set_ratings(
        {
            'Ana': ['Bob', 'Brian', 'Bailey', 'Beverly', 'Biyu'],
            'Amelia': ['Bailey', 'Brian', 'Beverly', 'Bob', 'Biyu'],
            'Avery': ['Bailey', 'Biyu', 'Beverly', 'Bob', 'Brian'],
            'Abby': ['Bob', 'Bailey', 'Beverly', 'Biyu', 'Brian'],
            'Alastair': ['Biyu', 'Bob', 'Beverly', 'Bailey', 'Brian'],
            'Biyu': ['Amelia', 'Abby', 'Avery', 'Ana', 'Alastair'],
            'Bailey': ['Ana', 'Avery', 'Alastair', 'Amelia', 'Abby'],
            'Beverly': ['Avery', 'Alastair', 'Amelia', 'Abby', 'Ana'],
            'Bob': ['Amelia', 'Alastair', 'Abby', 'Ana', 'Avery'],
            'Brian': ['Avery', 'Ana', 'Amelia', 'Abby', 'Alastair'],
        }
    )

    # Make the naive partnerships
    student_group.make_naive_partnerships()

    # Check that we obtained exactly the matches we expected

    expected = [2, 4, 2, 3, 3]
    result = []
    for student in student_group.students_a:
        result.append(student.get_rating_of_current_partner())
    assert expected == result, f'Expected a naive partnership happiness of exactly {expected}, got {result}\nConsider creating a smaller test case to isolate the bug'

    expected = [0, 0, 1, 0, 1]
    result = []
    for student in student_group.students_b:
        result.append(student.get_rating_of_current_partner())
    assert expected == result, f'Expected a naive partnership happiness of exactly {expected}, got {result}\nConsider creating a smaller test case to isolate the bug'

    print("tests for make_naive_partnerships passed")


# Part 3
# -------------------------------------------------------------

def test_propose_to_top_choice():
    """
    Test cases for get_rating_of_name
    """

    jacob_ratings = ["Amy", "Jessica", "Emily"]
    jacob = Student(None, "Jacob", jacob_ratings)
    amy_ratings = ["Rob", "Joe", "Jacob"]
    amy = Student(None, "Amy", amy_ratings)
    emily_ratings = ["Rob", "Jacob", "Joe"]
    emily = Student(None, "Emily", emily_ratings)
    joe_ratings = ["Jessica", "Amy", "Emily"]
    # And test group
    group = Group(["Rob", "Joe", "Jacob"], ["Amy", "Jessica", "Emily"])

    # Find Jacob
    jacob = group.get_student_by_name("Jacob")
    jacob.partner_ratings = jacob_ratings
    # Same for Emily
    emily = group.get_student_by_name("Emily")
    emily.partner_ratings = emily_ratings

    # Propose a top choice for Jacob
    jacob.to_propose = jacob.partner_ratings[:]
    output = jacob.propose_to_top_choice()
    assert output is None, "Function should have no return value"
    assert 2 == len(jacob.to_propose), "Should be popping from self.to_propose, regardless of whether partnership is made"
    assert "Emily" not in jacob.to_propose, "Should have removed the last name from self.propose"
    # Emily also has no partner, so match them
    assert emily == jacob.partner, "Should match with student if they have no partner"
    assert emily.partner == jacob, "Partner who got paired hasn't updated its partner attribute"
    # Let's try to match Amy with Jacob (her highest choice right now)
    # Amy has no partner, but Jacob has Emily (who he ranks as 2 (highest!))
    # So no switch should occur
    amy = group.get_student_by_name("Amy")
    amy.to_propose = amy_ratings
    amy.propose_to_top_choice()
    assert amy.partner is None, "Switched the proposed student's highest-rated partner for a lower rated one"
    assert jacob.partner == emily, "Switched the proposed student's highest-rated partner for a lower rated one"
    # Let's try to match Joe with Emily
    # Joe has no partner, but Emily has Jacob (who she ranks as 1 (okay))
    # She ranks Joe as 2 (highest), so they should match
    joe = group.get_student_by_name("Joe")
    joe.to_propose = joe_ratings
    joe.propose_to_top_choice()
    joe.partner == emily, "Not switching for a partner who ranks proposer higher"
    emily.partner == joe, "Proposed partner should now have its partner attribute updated"
    jacob.partner is None, "Student who's partner is now with someone else should have no partner"

    print("tests for propose_to_top_choice passed")


def test_algorithm():
    """
    Test case to validate that the algorithm was implemented in a reasonable way
    This test case relies on a hand-written example of the
        expected result of the entire algorithm rather than a single function
    """

    student_names_a = ['Ana', 'Avery', 'Alastair', 'Amelia', 'Abby']
    student_names_b = ['Bailey', 'Brian', 'Beverly', 'Bob', 'Biyu']
    student_group = Group(student_names_a, student_names_b)

    student_group.set_ratings(
        {
            'Ana': ['Bob', 'Brian', 'Bailey', 'Beverly', 'Biyu'],
            'Amelia': ['Bailey', 'Brian', 'Beverly', 'Bob', 'Biyu'],
            'Avery': ['Bailey', 'Biyu', 'Beverly', 'Bob', 'Brian'],
            'Abby': ['Bob', 'Bailey', 'Beverly', 'Biyu', 'Brian'],
            'Alastair': ['Biyu', 'Bob', 'Beverly', 'Bailey', 'Brian'],
            'Biyu': ['Amelia', 'Abby', 'Avery', 'Ana', 'Alastair'],
            'Bailey': ['Ana', 'Avery', 'Alastair', 'Amelia', 'Abby'],
            'Beverly': ['Avery', 'Alastair', 'Amelia', 'Abby', 'Ana'],
            'Bob': ['Amelia', 'Alastair', 'Abby', 'Ana', 'Avery'],
            'Brian': ['Avery', 'Ana', 'Amelia', 'Abby', 'Alastair'],
        }
    )

    # Make Gale-Shapely pairings
    student_group.make_gale_shapely_partnerships()

    # If everything was implemented correctly, we should have around .825 average happiness
    expected = 0.75
    result = calculate_average_happiness(student_group.all_students)
    assert math.isclose(expected, result),\
        "Gale Shapley algorithm should've made partnerships so that the average happiness is 0.75\n" +\
        f'Instead got {result} -- double-check your previous tests'

    print("tests for entire algorithm passed")


def test_all():
    test_student_constructor()
    test_student_str()
    test_has_partner()
    test_get_rating_of_name()
    test_get_rating_of_current_partner()
    test_break_partnership()
    test_make_partnership()
    test_get_unpartnered()
    test_make_naive_partnerships()
    test_propose_to_top_choice()
    test_algorithm()
    print('All tests passed!')


if __name__ == "__main__":
    test_all()
