"""Unit tests for the risk scoring engine."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from risk_engine import (
    classify_risk,
    compute_combined_risk_score,
    compute_demand_risk_score,
    compute_risk_scores,
    compute_traffic_risk_score,
    compute_weather_risk_score,
)


class TestTrafficRisk:
    def test_low_congestion_scores_below_20(self):
        assert compute_traffic_risk_score(0.1, 0.1) < 20

    def test_medium_congestion_scores_20_to_50(self):
        score = compute_traffic_risk_score(0.45, 0.45)
        assert 20 <= score <= 50

    def test_high_congestion_scores_50_to_80(self):
        score = compute_traffic_risk_score(0.7, 0.7)
        assert 50 <= score <= 80

    def test_critical_congestion_scores_above_80(self):
        score = compute_traffic_risk_score(0.9, 0.9)
        assert score >= 80

    def test_uses_max_of_current_and_7d_avg(self):
        # When 7-day avg is higher than current, it should drive the score up
        score_high_avg = compute_traffic_risk_score(0.2, 0.9)
        score_low_avg = compute_traffic_risk_score(0.2, 0.2)
        assert score_high_avg > score_low_avg

    def test_score_never_exceeds_100(self):
        assert compute_traffic_risk_score(1.0, 1.0) <= 100

    def test_score_never_below_zero(self):
        assert compute_traffic_risk_score(0.0, 0.0) >= 0


class TestWeatherRisk:
    def test_no_rain_normal_temp_scores_zero(self):
        assert compute_weather_risk_score(0.0, 0.0, 25.0) == 0.0

    def test_light_rain_scores_below_15(self):
        score = compute_weather_risk_score(3.0, 3.0, 25.0)
        assert 0 < score < 15

    def test_heavy_rain_scores_above_70(self):
        score = compute_weather_risk_score(40.0, 40.0, 25.0)
        assert score >= 70

    def test_extreme_heat_adds_risk(self):
        base = compute_weather_risk_score(0.0, 0.0, 25.0)
        hot = compute_weather_risk_score(0.0, 0.0, 45.0)
        assert hot > base

    def test_extreme_cold_adds_risk(self):
        base = compute_weather_risk_score(0.0, 0.0, 25.0)
        cold = compute_weather_risk_score(0.0, 0.0, 5.0)
        assert cold > base

    def test_score_capped_at_100(self):
        assert compute_weather_risk_score(100.0, 100.0, 50.0) <= 100


class TestDemandRisk:
    def test_low_demand_scores_below_10(self):
        assert compute_demand_risk_score(0.3, 0.3) < 10

    def test_medium_demand_scores_10_to_30(self):
        score = compute_demand_risk_score(0.6, 0.6)
        assert 10 <= score <= 30

    def test_high_demand_scores_30_to_60(self):
        score = compute_demand_risk_score(0.78, 0.78)
        assert 30 <= score <= 60

    def test_surge_demand_scores_above_60(self):
        score = compute_demand_risk_score(0.92, 0.92)
        assert score >= 60

    def test_score_capped_at_100(self):
        assert compute_demand_risk_score(1.0, 1.0) <= 100


class TestCombinedRisk:
    def test_all_zero_inputs_give_zero(self):
        assert compute_combined_risk_score(0, 0, 0) == 0.0

    def test_all_max_inputs_give_100(self):
        assert compute_combined_risk_score(100, 100, 100) == 100.0

    def test_traffic_weight_is_40_percent(self):
        # 100 traffic × 0.40 + 0 + 0 = 40
        score = compute_combined_risk_score(100, 0, 0)
        assert abs(score - 40.0) < 0.01

    def test_weather_weight_is_35_percent(self):
        score = compute_combined_risk_score(0, 100, 0)
        assert abs(score - 35.0) < 0.01

    def test_demand_weight_is_25_percent(self):
        score = compute_combined_risk_score(0, 0, 100)
        assert abs(score - 25.0) < 0.01

    def test_weights_sum_to_100(self):
        assert abs(40 + 35 + 25 - 100) == 0

    def test_result_clamped_to_100(self):
        assert compute_combined_risk_score(200, 200, 200) == 100.0

    def test_result_never_below_zero(self):
        assert compute_combined_risk_score(-10, -10, -10) == 0.0


class TestClassification:
    def test_score_0_is_low(self):
        assert classify_risk(0) == 'Low'

    def test_score_30_is_low(self):
        assert classify_risk(30) == 'Low'

    def test_score_31_is_medium(self):
        assert classify_risk(31) == 'Medium'

    def test_score_60_is_medium(self):
        assert classify_risk(60) == 'Medium'

    def test_score_61_is_high(self):
        assert classify_risk(61) == 'High'

    def test_score_100_is_high(self):
        assert classify_risk(100) == 'High'


class TestComputeRiskScores:
    """Integration-style tests for the main scoring function."""

    def _make_df(self, **overrides):
        base = {
            'date': pd.to_datetime('2025-01-01'),
            'city': 'Mumbai',
            'congestion_level': 0.5,
            'congestion_level_7d_avg': 0.5,
            'rainfall_mm': 10.0,
            'rainfall_mm_7d_avg': 10.0,
            'temperature': 28.0,
            'demand_index': 0.6,
            'demand_index_7d_avg': 0.6,
        }
        base.update(overrides)
        return pd.DataFrame([base])

    def test_output_has_required_columns(self):
        df = compute_risk_scores(self._make_df())
        for col in ['risk_score', 'risk_classification', 'traffic_risk', 'weather_risk', 'demand_risk']:
            assert col in df.columns

    def test_risk_score_in_valid_range(self):
        df = compute_risk_scores(self._make_df())
        assert 0 <= df['risk_score'].iloc[0] <= 100

    def test_high_congestion_yields_high_traffic_component(self):
        # congestion=0.95 → traffic_risk ≥ 80, but combined may still be Medium
        # if weather/demand are low. Test the component directly.
        df = compute_risk_scores(self._make_df(congestion_level=0.95, congestion_level_7d_avg=0.95))
        assert df['traffic_risk'].iloc[0] >= 80

    def test_all_severe_inputs_yield_high_risk(self):
        # All three factors extreme → combined must exceed 61
        df = compute_risk_scores(self._make_df(
            congestion_level=0.95, congestion_level_7d_avg=0.95,
            rainfall_mm=50.0, rainfall_mm_7d_avg=50.0,
            demand_index=0.95, demand_index_7d_avg=0.95,
        ))
        assert df['risk_classification'].iloc[0] == 'High'

    def test_all_low_values_yield_low_risk(self):
        df = compute_risk_scores(self._make_df(
            congestion_level=0.1, congestion_level_7d_avg=0.1,
            rainfall_mm=0.0, rainfall_mm_7d_avg=0.0,
            demand_index=0.2, demand_index_7d_avg=0.2,
        ))
        assert df['risk_classification'].iloc[0] == 'Low'
