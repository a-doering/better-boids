import os
import yaml
from nose.tools import assert_almost_equal, assert_equal, assert_greater, assert_less
from boids import Boids


def test_bad_boids_regression():
    with open(os.path.join(os.path.dirname(__file__), "fixture.yml")) as fixture_file:
        regression_data = yaml.safe_load(fixture_file)
    boid_count = 50
    boids = Boids.with_default_parameters(boid_count)
    boids.initialise_from_data(regression_data["before"])
    boids.update()
    for index, boid in enumerate(boids.boids):
        assert_almost_equal(boid.x, regression_data["after"][0][index], delta=0.01)
        assert_almost_equal(boid.y, regression_data["after"][1][index], delta=0.01)
        assert_almost_equal(boid.xv, regression_data["after"][2][index], delta=0.01)
        assert_almost_equal(boid.yv, regression_data["after"][3][index], delta=0.01)


def test_bad_boids_initialisation():
    boid_count = 15
    boids = Boids.with_default_parameters(boid_count)
    x_range = (-450, 50.0)
    y_range = (300.0, 600.0)
    xv_range = (0, 10.0)
    yv_range = (-20.0, 20.0)
    boids.initialise_random(
        boid_count,
        x_range=x_range,
        y_range=y_range,
        xv_range=xv_range,
        yv_range=yv_range,
    )
    assert_equal(len(boids.boids), 15)
    for boid in boids.boids:
        assert_less(boid.x, x_range[1])
        assert_greater(boid.x, x_range[0])
        assert_less(boid.y, y_range[1])
        assert_greater(boid.y, y_range[0])
        assert_less(boid.xv, xv_range[1])
        assert_greater(boid.xv, xv_range[0])
        assert_less(boid.yv, yv_range[1])
        assert_greater(boid.yv, yv_range[0])
