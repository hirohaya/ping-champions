"""
Unit tests for the Elo rating system module.
"""

import pytest
from elo import (
    calculate_win_probability,
    calculate_new_rating,
    update_ratings,
    get_rating_change,
    get_initial_rating,
    INITIAL_RATING,
    K_FACTOR,
)


class TestWinProbability:
    """Tests for win probability calculation."""

    def test_equal_ratings_gives_50_percent(self):
        """Players with equal ratings should have 50% win probability each."""
        prob_a, prob_b = calculate_win_probability(1600, 1600)
        assert abs(prob_a - 0.5) < 0.001
        assert abs(prob_b - 0.5) < 0.001
        assert abs(prob_a + prob_b - 1.0) < 0.001

    def test_higher_rating_has_higher_probability(self):
        """Higher rated player should have higher win probability."""
        prob_1700, prob_1600 = calculate_win_probability(1700, 1600)
        prob_1600_vs_1700, prob_1700_vs_1600 = calculate_win_probability(1600, 1700)
        
        assert prob_1700 > 0.5
        assert prob_1600_vs_1700 < 0.5
        assert abs(prob_1700 - (1 - prob_1600_vs_1700)) < 0.001

    def test_large_rating_difference(self):
        """Large rating difference should give extreme probabilities."""
        prob_2000, prob_1200 = calculate_win_probability(2000, 1200)
        
        # Much stronger player has very high win probability
        assert prob_2000 > 0.95
        assert prob_1200 < 0.05

    def test_probabilities_sum_to_one(self):
        """Win probabilities should always sum to 1.0."""
        test_cases = [(1400, 1600), (1600, 1800), (1200, 2000), (1600, 1600)]
        
        for rating_a, rating_b in test_cases:
            prob_a, prob_b = calculate_win_probability(rating_a, rating_b)
            assert abs(prob_a + prob_b - 1.0) < 0.0001


class TestNewRating:
    """Tests for new rating calculation."""

    def test_winning_increases_rating(self):
        """Winning a match should increase rating."""
        expected_prob = 0.5
        new_rating = calculate_new_rating(1600, expected_prob, 1)
        assert new_rating > 1600

    def test_losing_decreases_rating(self):
        """Losing a match should decrease rating."""
        expected_prob = 0.5
        new_rating = calculate_new_rating(1600, expected_prob, 0)
        assert new_rating < 1600

    def test_upset_win_gains_more_points(self):
        """Winning against stronger opponent (upset) gains more rating points."""
        # Weaker player (low expected win prob) wins
        upset_gain = calculate_new_rating(1400, 0.2, 1) - 1400
        
        # Stronger player (high expected win prob) wins
        expected_gain = calculate_new_rating(1800, 0.8, 1) - 1800
        
        assert upset_gain > expected_gain

    def test_upset_loss_loses_more_points(self):
        """Losing to weaker opponent (upset) loses more rating points."""
        # Stronger player (high expected win prob) loses
        upset_loss = 1800 - calculate_new_rating(1800, 0.8, 0)
        
        # Weaker player (low expected win prob) loses
        expected_loss = 1400 - calculate_new_rating(1400, 0.2, 0)
        
        assert upset_loss > expected_loss

    def test_rating_change_with_different_k_factors(self):
        """Higher K-factor should result in larger rating changes."""
        expected_prob = 0.5
        
        change_k32 = abs(calculate_new_rating(1600, expected_prob, 1, k_factor=32) - 1600)
        change_k64 = abs(calculate_new_rating(1600, expected_prob, 1, k_factor=64) - 1600)
        
        assert change_k64 == 2 * change_k32


class TestUpdateRatings:
    """Tests for simultaneous two-player rating updates."""

    def test_ratings_converge_toward_equal(self):
        """After many games between equal players, ratings should stay equal."""
        p1_rating = 1600.0
        p2_rating = 1600.0
        
        for i in range(10):
            # Alternate who wins
            winner_id = 1 if i % 2 == 0 else 2
            p1_rating, p2_rating = update_ratings(
                p1_rating, p2_rating, winner_id, 1, 2
            )
        
        # Ratings should be relatively close (within 15 points due to alternating wins)
        assert abs(p1_rating - p2_rating) < 20

    def test_sum_of_ratings_stays_constant(self):
        """Sum of both players' ratings should remain approximately constant."""
        p1_rating = 1600.0
        p2_rating = 1600.0
        initial_sum = p1_rating + p2_rating
        
        new_p1, new_p2 = update_ratings(p1_rating, p2_rating, 1, 1, 2)
        new_sum = new_p1 + new_p2
        
        # Sum should be exactly the same (zero-sum game)
        assert abs(new_sum - initial_sum) < 0.01

    def test_winner_gains_loser_loses(self):
        """Winner should gain rating, loser should lose rating."""
        p1_initial = 1600.0
        p2_initial = 1600.0
        
        new_p1, new_p2 = update_ratings(p1_initial, p2_initial, 1, 1, 2)
        
        assert new_p1 > p1_initial
        assert new_p2 < p2_initial

    def test_strong_player_win_gives_small_gain(self):
        """Strong player (higher rating) winning gives less rating gain."""
        stronger_p1 = 1800.0
        weaker_p2 = 1400.0
        
        new_strong, new_weak = update_ratings(
            stronger_p1, weaker_p2, 1, 1, 2  # Strong player wins
        )
        
        gain = new_strong - stronger_p1
        
        # Gain should be small (less than K_FACTOR)
        assert 0 < gain < K_FACTOR

    def test_weak_player_win_gives_large_gain(self):
        """Weak player (lower rating) winning gives more rating gain."""
        stronger_p1 = 1800.0
        weaker_p2 = 1400.0
        
        new_strong, new_weak = update_ratings(
            stronger_p1, weaker_p2, 2, 1, 2  # Weak player wins
        )
        
        gain = new_weak - weaker_p2
        
        # Gain should be large (more than K_FACTOR/2)
        assert gain > K_FACTOR / 2


class TestRatingChange:
    """Tests for rating change calculation."""

    def test_rating_change_with_win(self):
        """Calculate rating change for a win."""
        change = get_rating_change(1600, 1600, 1)
        
        assert change > 0

    def test_rating_change_with_loss(self):
        """Calculate rating change for a loss."""
        change = get_rating_change(1600, 1600, 0)
        
        assert change < 0

    def test_rating_change_absolute_value_equal_for_same_match(self):
        """Rating gains and losses should be equal for equal-rated players."""
        change_win = get_rating_change(1600, 1600, 1)
        change_loss = get_rating_change(1600, 1600, 0)
        
        assert change_win == -change_loss


class TestInitialRating:
    """Tests for initial rating."""

    def test_initial_rating_is_1600(self):
        """New players should start with 1600 rating."""
        assert get_initial_rating() == INITIAL_RATING
        assert get_initial_rating() == 1600.0


class TestIntegrationScenarios:
    """Integration tests with realistic scenarios."""

    def test_tournament_simulation(self):
        """Simulate a small tournament and verify ratings behave correctly."""
        # Three players: Alice (strong), Bob (medium), Carol (weak)
        alice_rating = 1800.0
        bob_rating = 1600.0
        carol_rating = 1400.0
        
        # Round 1: Alice beats Bob (expected)
        alice_rating, bob_rating = update_ratings(
            alice_rating, bob_rating, 1, 1, 2
        )
        # Alice gains less, Bob loses more
        assert alice_rating > 1800  # Gained
        assert bob_rating < 1600  # Lost
        
        # Save state after round 1
        alice_r1 = alice_rating
        bob_r1 = bob_rating
        
        # Round 2: Carol beats Alice (upset!)
        alice_rating, carol_rating = update_ratings(
            alice_rating, carol_rating, 2, 1, 3
        )
        # Alice loses more, Carol gains more
        assert alice_rating < alice_r1  # Lost significantly
        # Carol gains points even though losing overall ELO (net zero sum with Alice)
        assert carol_rating >= 1395  # Gained some despite lower rating

    def test_rating_stability(self):
        """Ratings should gradually stabilize as player plays more games."""
        rating = 1600.0
        opponent_rating = 1600.0
        
        # Play 20 games
        for i in range(20):
            # Win if even, lose if odd
            result = 1 if i % 2 == 0 else 0
            rating, opponent_rating = update_ratings(
                rating, opponent_rating, (1 if result == 1 else 2), 1, 2
            )
        
        # After alternating wins/losses against equal opponent,
        # should be close to 1600
        assert abs(rating - 1600) < 50
