"""Tests for multi-coordinate and cross-body scientific invariants."""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import numpy as np

import cross_body


class CrossBodyTests(unittest.TestCase):
    def test_apparent_residuals_and_vectors_use_selected_reference(self):
        dates = [datetime(2000, 1, 1) + timedelta(days=i) for i in range(3)]
        ty = {d: {'ra': 1.0, 'dec': 5.0} for d in dates}
        jp = {d: {'ra_app': 359.0, 'dec_app': 4.0,
                  'ra_icrf': 20.0, 'dec_icrf': -10.0} for d in dates}
        config = {'reference': 'apparent-of-date', 'tychos': 'unused', 'jpl': 'unused',
                  'start': '2000-01-01', 'stop_exclusive': '2000-01-04', 'cadence_hours': 24}
        with patch.object(cross_body, 'read_tychos', return_value=ty), \
                patch.object(cross_body, 'read_jpl', return_value=jp):
            result = cross_body.load_body(config, {'moon': {'target_id': '301'}}, 'moon')
        np.testing.assert_allclose(result['residuals'][:, 0], 2.0)
        np.testing.assert_allclose(result['residuals'][:, 1], 1.0)
        np.testing.assert_allclose(result['residuals'][:, 2], 2*np.cos(np.radians(4)))
        np.testing.assert_allclose(result['jpl_vec'], cross_body.unit_vectors(
            np.full(3, 359.0), np.full(3, 4.0)))

    def test_apparent_fit_reports_ra_and_declination(self):
        dates = [datetime(2000, 1, 1) + timedelta(days=i) for i in range(90)]
        split = np.array(['train']*30 + ['validation']*30 + ['test']*30)
        config = {'reference': 'apparent-of-date', 'start': '2000-01-01',
                  'periods_by_body': {'moon': [14.765294]}, 'ridge_alphas': [1]}
        result, _ = cross_body.fit_body(config, 'moon', dates, np.ones((90, 4)), split)
        for metrics in result['splits'].values():
            self.assertEqual(set(metrics['baseline']), {'ra', 'declination', 'east', 'north'})
            self.assertEqual(set(metrics['unexplained']), {'ra', 'declination', 'east', 'north'})

    def test_ridge_does_not_penalize_intercept(self):
        x = np.column_stack((np.ones(20), np.linspace(-1, 1, 20)))
        y = np.column_stack((np.full(20, 3.0), np.full(20, -2.0)))
        coefficients = cross_body.ridge_fit(x, y, 1000.0)
        np.testing.assert_allclose(coefficients[0], [3.0, -2.0], atol=1e-12)
        np.testing.assert_allclose(coefficients[1], [0.0, 0.0], atol=1e-12)

    def test_global_rotation_preserves_pairwise_separation(self):
        first = cross_body.unit_vectors(np.array([10.0, 20.0]), np.array([5.0, -4.0]))
        second = cross_body.unit_vectors(np.array([70.0, 80.0]), np.array([-3.0, 8.0]))
        angle = np.radians(31.0)
        rotation = np.array(((np.cos(angle), -np.sin(angle), 0.0),
                             (np.sin(angle), np.cos(angle), 0.0),
                             (0.0, 0.0, 1.0)))
        before = cross_body.angular_separation(first, second)
        after = cross_body.angular_separation(first @ rotation.T, second @ rotation.T)
        np.testing.assert_allclose(before, after, atol=1e-12)

    def test_tangent_metric_uses_both_coordinates(self):
        residuals = np.zeros((2, 4))
        residuals[:, 2] = [3.0, 0.0]
        residuals[:, 3] = [4.0, 0.0]
        self.assertAlmostEqual(cross_body.combined_tangent_rmse(residuals),
                               np.sqrt(12.5))


if __name__ == "__main__":
    unittest.main()
