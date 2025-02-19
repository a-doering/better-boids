import os
import yaml
from nose.tools import assert_almost_equal, assert_equal, assert_greater, assert_less
from numpy.testing import assert_array_equal
from boids import Boid, Flock


def test_bad_boids_regression():
    with open(os.path.join(os.path.dirname(__file__), "fixture.yml")) as fixture_file:
        regression_data = yaml.safe_load(fixture_file)
    boid_count = 50
    flock = Flock.with_default_parameters(boid_count)
    flock.initialize_from_data(regression_data["before"])
    flock.update()
    for index, boid in enumerate(flock.boids):
        assert_almost_equal(
            boid.position[0], regression_data["after"][0][index], delta=0.01
        )
        assert_almost_equal(
            boid.position[1], regression_data["after"][1][index], delta=0.01
        )
        assert_almost_equal(
            boid.velocity[0], regression_data["after"][2][index], delta=0.01
        )
        assert_almost_equal(
            boid.velocity[1], regression_data["after"][3][index], delta=0.01
        )


def test_bad_boids_initialization():
    boid_count = 15
    flock = Flock.with_default_parameters(boid_count)
    x_range = (-450, 50.0)
    y_range = (300.0, 600.0)
    xv_range = (0, 10.0)
    yv_range = (-20.0, 20.0)
    flock.initialize_random(
        boid_count,
        x_range=x_range,
        y_range=y_range,
        xv_range=xv_range,
        yv_range=yv_range,
    )
    assert_equal(len(flock.boids), boid_count)
    assert_equal(flock.boid_count, boid_count)
    for boid in flock.boids:
        assert_less(boid.position[0], x_range[1])
        assert_greater(boid.position[0], x_range[0])
        assert_less(boid.position[1], y_range[1])
        assert_greater(boid.position[1], y_range[0])
        assert_less(boid.velocity[0], xv_range[1])
        assert_greater(boid.velocity[0], xv_range[0])
        assert_less(boid.velocity[1], yv_range[1])
        assert_greater(boid.velocity[1], yv_range[0])


def test_bad_boids_initialization_seed():
    boid_count = 15
    random_seed = 789
    flock1 = Flock.with_default_parameters(boid_count)
    flock1.initialize_random(boid_count, random_seed=random_seed)
    flock2 = Flock.with_default_parameters(boid_count)
    flock2.initialize_random(boid_count, random_seed=random_seed)
    for boid1, boid2 in zip(flock1.boids, flock2.boids):
        assert_array_equal(boid1.position, boid2.position)
        assert_array_equal(boid1.velocity, boid2.velocity)


def test_boid_interaction_fly_to_middle():
    parameters = {
        "flock_attraction": 3,
        "avoidance_radius": 2,
        "formation_flying_radius": 10,
        "speed_matching_strength": 0,
    }
    flock = Flock(parameters)
    first = Boid(0, 0, 1, 0, flock)
    second = Boid(0, 5, 0, 0, flock)
    assert_array_equal(first.interaction(second), [0.0, 15.0])


def test_boid_interaction_avoidance():
    parameters = {
        "flock_attraction": 3,
        "avoidance_radius": 10,
        "formation_flying_radius": 10,
        "speed_matching_strength": 0,
    }
    flock = Flock(parameters)
    first = Boid(0, 0, 1, 0, flock)
    second = Boid(0, 5, 0, 0, flock)
    assert_array_equal(first.interaction(second), [0.0, 10.0])


def test_boid_interaction_formation():
    parameters = {
        "flock_attraction": 3,
        "avoidance_radius": 2,
        "formation_flying_radius": 10,
        "speed_matching_strength": 7,
    }
    flock = Flock(parameters)
    first = Boid(0, 0, 0.0, 0, flock)
    second = Boid(0, 5, 11.0, 0, flock)
    assert_array_equal(first.interaction(second), [11.0 * 7.0, 15.0])
