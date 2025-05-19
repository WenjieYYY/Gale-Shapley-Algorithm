"""
Author: Jason Yang
Starting Date: 05/14/2025

Implementation of the Gale-Shapley algorithm.

The Gale-Shapley algorithm is an algorithm that,
given two non-overlapping groups—group A and group B—and each
group member's preference for the members of the other group,
makes pairings of A and B members, so that no two people would both
be happier if they switched partners with each other.
"""

import math
import random
import time


class Student:
    """
    A class to represent a student and their preferences for partners.

    Attributes:
        group (Group): The Group that this student belongs to.
            Useful for looking up group members by name in order to propose to them.
        name (str): The (unique) name for this student.
            We assume names are unique for this simulation
            In the real world, names are not unique, so we would use
                a unique identifier like NetID.
        partner_ratings (list[str]): A list of all student names in the other group (A or B).
            It is sorted by how much this student prefers them.
            NOTE: this must be ordered from LEAST to MOST preferred to make get_rating() easier
                (e.g. ["Alice", "Adam", "Anya", "Allen"] <- prefers "Allen" *the most*).
        partner (Student | None): This student's current partner.
            If None, then this student does not have a partner
            Starts as None until we reset it with reset_partnerships().
        to_propose (list[str]): A list of students that we have yet to propose a partnership to.
            NOTE: The contents are added in create_gale_shapely_partnerships().
    """

    def randomize_ratings(self):
        """
        Randomize this student's preferences

        Useful for testing and running random experiments
        """
        random.shuffle(self.partner_ratings)

    # Part 1: Setup
    # ---------------------------------------------

    def __init__(self, group: 'Group', name: str, partner_ratings: list[str]):
        """
        Initialize this Student by storing arguments as attributes.

        Set partner to None.
        Sets to_propose to an empty list initially
        """
        self.group = group
        self.name = str(name)
        self.partner_ratings = partner_ratings[:]
        self.partner = None
        self.to_propose = []

    def __str__(self) -> str:
        """
        Returns a string representation of this student

        For example, if this student's name is Jake, with no partner:
            'Jake (no-one)'.
        If this student's nam is Jake, with a partner named 'Mary':
            'Jake (Mary)'.
        """
        if self.partner == None:
            return f'{self.name} (no-one)'
        else:
            return f'{self.name} ({self.partner.name})'

    def has_partner(self):
        """
        Returns True if this student has a partner, and False otherwise.
        """
        if self.partner:
            return True
        return False

    def get_rating_of_name(self, name: str) -> int:
        """
        Returns the rating of the named Student
        If the given name is not rated by this Student, instead returns -1

        Each student is ordered sequentially:
            the least preferred student is rated 0
            the second-least preferred student is rated 1
            etc
        """
        if name in self.partner_ratings:
            return self.partner_ratings.index(name)
        else:
            return -1

    def get_rating_of_current_partner(self):
        """
        Returns the rating of this student's current partner
        If the current partner is not rated by this Student,
            or if this Student does not have a partner, returns -1
        """
        if self.partner != None:
            if self.partner.name in self.partner_ratings:
                return self.partner_ratings.index(self.partner.name)
            else:
                return -1
        else:
            return -1

    def break_partnership(self):
        """
        Break this student's partnership.

        That is, if we have a partner, set both the partner
            of this student and the former partner to None
        Otherwise, do nothing
        """
        if self.has_partner():
            former = self.partner
            self.partner = None
            former.partner = None

    def make_partnership(self, new_partner: 'Student'):
        """
        Form a partnership between this student and new_partner Student
        If either this student or the new partner already has a partner
        This method will first break that partnership
        """
        if self.partner != None:
            self.break_partnership()
        if new_partner.partner != None:
            new_partner.break_partnership()
        self.partner = new_partner
        new_partner.partner = self


    # Part 3: Algorithm
    # ---------------------------------------------

    def propose_to_top_choice(self):
        """
        Propose a partnership to our top choice.

        Pops the name from our self.to_propose list and finds the
            associated student by name as a potential partner from our Group

        Consider three cases for the potential partner:
            (1) If the potential partner does *not* have a partner yet,
                then they accept the proposal. Make the partnership.
            (2) If the potential partner *does* have a partner
                and if we are preferred more than their current partner,
                then they accept the proposal and break up with their current partner
            (3) If we are preferred less than their current partner or if no student is found,
                then nothing happens, but they are now removed (with .pop()) from
                our list of potential partners so that we can't propose to them again.
        """
        if self.to_propose:
            propose_str = self.to_propose.pop()
            propose_student = self.group.get_student_by_name(propose_str)
            if not propose_student.has_partner():
                self.make_partnership(propose_student)
            else:
                if propose_student.get_rating_of_name(self.name) > propose_student.get_rating_of_current_partner():
                    self.make_partnership(propose_student)


class Group:
    """
    Contains two groups of students and methods for matchmaking.

    The two groups (students_a and students_b) must always be the same length

    Attributes:
        students_a (list[Student]): The students in group A.
        students_b (list[Student]) The students in group B.
        all_students (list[Student]): The students in both groups.
    """

    def __init__(self, names_a: list[str], names_b: list[str]):
        """
        Initialize the Group object.

        Creates Student objects given lists of names.

        Args:
            names_a (list[str]): The names of students to place in group A.
            names_b (list[str]): The names of students to place in group B.
        """
        self.students_a : list[Student] = []
        self.students_b : list[Student] = []

        # For ratings, start everyone with shuffled ratings
        for name in names_a:
            ratings = names_b[:]
            random.shuffle(ratings)
            self.students_a.append(Student(self, name, ratings))

        for name in names_b:
            ratings = names_a[:]
            random.shuffle(ratings)
            self.students_b.append(Student(self, name, ratings))

        self.all_students : list[Student] = self.students_a + self.students_b

    def get_student_by_name(self, name: str) -> 'None | Student':
        """
        Return the student with that name,
          or None if that student is not found
        """
        found = [s for s in self.all_students if s.name == name]

        if found:
            return found[0]

        return None

    def set_ratings(self, names_to_ratings: dict[str, int]):
        """
        Set each student's preferences to their partner rankings.
        names_to_ratings must be a dictionary mapping
          from student name to that student's rating
        """
        for name, partner_ratings in names_to_ratings.items():
            s = self.get_student_by_name(name)
            s.partner_ratings = partner_ratings

    def randomize_ratings(self):
        """
        Randomize each student's preferences.

        Used for running experiments.
        """
        for s in self.all_students:
            s.randomize_ratings()

    def break_all_partnerships(self):
        """
        Remove all partnerships from this group.
        """
        for s in self.all_students:
            s.break_partnership()

    def make_gale_shapely_partnerships(self):
        """
        Make partnerships with the Gale Shapley algorithm.

        This should result in better partnerships than the naive approach.

        Some visual animations of how it works:
        https://www.youtube.com/watch?v=fudb8DuzQlM
        https://mindyourdecisions.com/blog/2015/03/03/the-stable-marriage-problem-gale-shapley-algorithm-an-algorithm-recognized-in-the-2012-nobel-prize-and-used-in-the-residency-match/
        """
        # Implement the Gale Shapley algorithm
        #
        # First, break all existing partnerships
        # Group A contains the proposers
        #     Add a to_propose list to each student in group A
        #     that is a *copy* of the partner_ratings list for that student
        #
        #     We will be *removing* names from it, so we want a copy, not a reference
        #     (see https://therenegadecoder.com/code/how-to-clone-a-list-in-python/)
        #     Use any of the techniques in this article to make a copy of
        #     the student.partner_ratings list (a slice is the easiest)
        #
        # While there are any unpartnered proposers left:
        #     Each unpartnered proposer offers to their top choice partner
        #     - That partner may accept or not (that is handled by offer_to_top_choice)
        #     Eventually, if the algoritm is implemented correctly,
        #     everyone will be partnered
        #
        # Why is propose_to_top_choice() a method of Student rather than Group?
        #     It is easier to think about it as *one* student making a choice!

        self.break_all_partnerships()

        for s in self.students_a:
            s.to_propose = s.partner_ratings[:]

        while self.get_unpartnered():
            proposers = self.get_unpartnered()
            for s in proposers:
                s.propose_to_top_choice()

    # -------------------------------
    # Useful data-printing methods

    def print_partnership_quality(self):
        """
        Print how happy everyone is with their partner.
        """
        partnerships = [(a, a.partner) for a in self.students_a if a.partner]

        # Keep track of how happy A and B are
        for a, b in partnerships:
            a_happy = a.get_rating_of_current_partner()
            b_happy = b.get_rating_of_current_partner()
            print(f"{a.name:10}({a_happy}) {b.name:10}({b_happy})")

        unpartnered = [s for s in self.all_students if not s.has_partner()]

        print("Unpartnered: " + ", ".join([str(s) for s in unpartnered]))

        print(
            f"Group A happiness = {calculate_average_happiness(self.students_a)}")
        print(
            f"Group B happiness = {calculate_average_happiness(self.students_b)}")
        print(
            f"  Total happiness = {calculate_average_happiness(self.all_students)}")

    def print_student_information(self):
        """
        Print out all student information.
        """
        all_students = self.students_a + self.students_b

        # ** Reuse this code if you want to print students later! **
        print("\nAll students: ")
        for s in all_students:
            print(
                f"\t{str(s).ljust(30)} happiness: {s.get_rating_of_current_partner()}, ratings: {','.join(s.partner_ratings)}")

    # Part 2: Groups
    # -------------------------------------

    def get_unpartnered(self) -> list['Student']:
        """
        Returns a list of all students in group A of this Group without a partner.
        """
        result = []
        for s in self.students_a:
            if not s.has_partner():
                result.append(s)
        return result

    def make_naive_partnerships(self):
        """
        Makes (not very good) partnerships.

        First, break up all existing partnerships

        Second, pair up the first student in students_a with the first student in students_b
          then pair up the second student in students_a with the second student in students_b
          ...
        that is, student_a[i] is paired with student_b[i].
        """
        # Note: per the class attributes, len(students_a) is same as len(students_b)
        # Hint: use a for loop over either
        #   an *enumerated* list of students_a:
        #       for i, student_a in enumerate(students_a):
        #   OR a *zipped* list of (students_a, students_b).
        #       for student_a, student_b in zip(students_a, students_b):

        self.break_all_partnerships()
        for i, student_a in enumerate(self.students_a):
            student_a.make_partnership(self.students_b[i])


# ---------------------------
# Experiment-running functions
# ---------------------------

def calculate_average_happiness(students: list[Student]) -> int:
    """
    Returns a score denoting the average of every student's happiness.
    """
    happiness_per_person = [s.get_rating_of_current_partner()
                            for s in students]
    total = sum(happiness_per_person)

    # What is our total number of choices?
    # This normalizes it so happiness is between 0 and 1
    option_count = len(students[0].partner_ratings) - 1
    student_count = len(students)
    return total / (student_count * option_count)


def run_experiment(student_count: int = 10,
                   run_count: int = 10,
                   matchmaking_fxn: int = "make_gale_shapely_partnerships") \
        -> dict[str, int | float]:
    """
    Returns the result of running an experiment as a dictionary


    Create a Group of student_count pairs of Students.
    Run run_count times:
        randomize the group's ratings
        call the correct method on the group
        calculate and add the total happiness for group A, B, and all students
    """
    # Uncomment this to print which experiment we are running
    # print(f"\n----\nRun experiment with {student_count} students for {run_count} runs ({matchmaking_fxn})\n")

    # Setup the groups
    # We need unique names, but because this is an experiement,
    #   we don't need them to be memorable
    # Create names ["A0", "A1", ..] etc

    names_a = ["A" + str(i) for i in range(0, student_count)]
    names_b = ["B" + str(i) for i in range(0, student_count)]
    g = Group(names_a, names_b)

    total_happiness_a = 0.0
    total_happiness_b = 0.0
    total_happiness = 0.0

    # Let's run an experiment
    # How happy is everyone *on average?*
    # How long does it take *on average?*

    # Run matchmaking run_count times for
    # * for run_count times:
    #   * randomize the ratings for this group
    #   * call the correct matchmaking-method for this group
    #       you can use this approach https://stackoverflow.com/questions/3061/calling-a-function-of-a-module-by-using-its-name-a-string
    #       or an if-statement
    #   * use calculate_average_happiness to get the happiness
    #       after matchmaking, for A, B and all students
    #       and add that to the totals

    # We often want to measure the time our code takes to run
    # So Python includes a very accurate way to get the current time:
    #   https://realpython.com/python-timer/
    # Use time.perfcounter() to get the starting time
    #   and the time when you finish the for loop
    # Compute the difference, and divide by run_count
    #   to find the *time each matchmaking takes*

    start = time.perf_counter()

    fxn = getattr(g, matchmaking_fxn)  # Assign function to a variable!

    for i in range(0, run_count):
        g.randomize_ratings()
        fxn()
        total_happiness_a += calculate_average_happiness(g.students_a)
        total_happiness_b += calculate_average_happiness(g.students_b)
        total_happiness += calculate_average_happiness(g.all_students)

    stop = time.perf_counter()
    total_time = (stop - start) / run_count

    # these calculations are provided for you
    # We measure unfairness as the ratio of how much happier A is than B
    unfairness = total_happiness_a / total_happiness_b

    # Return the results
    return {
        "matchmaking_fxn": matchmaking_fxn,
        "student_count": student_count,
        "run_count": run_count,
        "a": total_happiness_a / run_count,  # Average over *all runs*
        "b": total_happiness_b / run_count,
        "all": total_happiness / run_count,
        "unfairness": unfairness,
        "time": total_time * 1_000,  # Convert to milliseconds not seconds
    }

# Use this to easily print the results of any test
def print_test_result(result):
    print(
        f"Experiment with {result['student_count']} students for {result['run_count']} runs ({result['matchmaking_fxn']})")
    print(f"\tA happiness:       {result['a']:.2f}")
    print(f"\tB happiness:       {result['b']:.2f}")
    print(f"\tAverage happiness: {result['all']:.2f}")
    print(
        f"\tUnfairness:        {result['unfairness']:.2f} (1 is perfectly fair)")
    print(f"\tTime per run: {result['time']:.4f} milliseconds")
