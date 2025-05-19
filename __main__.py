from gale_shapley import run_experiment, print_test_result
import math

print("-" * 50 + "\nRunning experiments")

# Try out a few experiments by changing these values
# What do you notice about increasing the number of students, or the run count?
# How does fairness and satisfaction change if you use naive or Gale-Shapley?
run_count = 100
student_count = 100
fxn_name = "make_gale_shapely_partnerships"
fxn_name = "make_naive_partnerships"

result = run_experiment(student_count=student_count,
                        run_count=run_count, matchmaking_fxn=fxn_name)
print_test_result(result)

# How long does this take to run?
# Adjust the range for whatever your computer can handle
# or control-C to stop the experiment when you see the pattern
# Notice that it gets slower PER STUDENT

print("\nTest run speed")
for i in range(1, 31):
    run_count = 10
    student_count = 10 * i
    result = run_experiment(
        student_count=student_count,
        run_count=run_count,
        matchmaking_fxn="make_gale_shapely_partnerships",
    )
    avg_time = result["time"]
    time_per_student = avg_time / student_count
    bar = "▇" * round(avg_time * 0.2)
    print(f"{student_count:10}: {time_per_student:.4f} ms/student {bar}")

# A few asserts to verify that
# * Naive is unsatisfying but fair
# * Gale-Shapley makes more people happy, but is unfair to group B
# INTERESTING QUESTION: Which one would you use in the real world?
# # When we assign Peer Mentors, who should be group A, profs or peer mentors?

naive_result = run_experiment(
    student_count=20, run_count=100, matchmaking_fxn="make_naive_partnerships")

print_test_result(naive_result)

assert math.isclose(naive_result["unfairness"], 1,
                    abs_tol=0.05), "We expect GS algorithm to be biased in favor of group A"
assert math.isclose(
    naive_result["all"], 0.5, abs_tol=0.05), "We expect an average of about .5 happiness for this size group"

gs_result = run_experiment(
    student_count=20, run_count=100, matchmaking_fxn="make_gale_shapely_partnerships")
print_test_result(gs_result)

assert gs_result["a"] > gs_result["b"], "We expect GS algorithm to be biased in favor of group A"
assert math.isclose(
    gs_result["all"], 0.812, abs_tol=0.05), "We expect an average of about .812 for this size group"
