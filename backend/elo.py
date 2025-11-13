"""
Elo rating system implementation for Ping Champions tournament.

The Elo rating system is a method for calculating the relative skill levels
of players in zero-sum games such as tennis or ping-pong.

Reference: https://en.wikipedia.org/wiki/Elo_rating_system
"""

import math

# Standard Elo parameters
K_FACTOR = 32  # Controls the maximum rating change per game (default, per-player adjusted in get_k_factor)
INITIAL_RATING = 1200  # Initial rating for new players (from REFINAMENTO_FEATURE_1.md)
RATING_MULTIPLIER = 400  # Used in win probability calculation


def calculate_win_probability(rating_a: float, rating_b: float) -> tuple[float, float]:
    """
    Calculate win probabilities for two players based on their ratings.
    
    Uses the standard Elo formula:
    P(A wins) = 1 / (1 + 10^((Rating_B - Rating_A) / 400))
    P(B wins) = 1 - P(A wins)
    
    Args:
        rating_a: Player A's current rating
        rating_b: Player B's current rating
    
    Returns:
        Tuple of (probability_a_wins, probability_b_wins)
        
    Examples:
        >>> prob_a, prob_b = calculate_win_probability(1600, 1600)
        >>> abs(prob_a - 0.5) < 0.001  # Equal ratings = 50% chance
        True
        >>> prob_a, prob_b = calculate_win_probability(1700, 1600)
        >>> prob_a > 0.5  # Higher rating should have > 50% chance
        True
    """
    rating_diff = rating_b - rating_a
    expected_a = 1 / (1 + math.pow(10, rating_diff / RATING_MULTIPLIER))
    expected_b = 1 - expected_a
    
    return expected_a, expected_b


def calculate_new_rating(
    current_rating: float,
    expected_win_probability: float,
    game_result: int,
    k_factor: int = K_FACTOR
) -> float:
    """
    Calculate a player's new rating after a game.
    
    Formula: New Rating = Old Rating + K * (Actual - Expected)
    - game_result = 1 if the player won
    - game_result = 0 if the player lost
    
    Args:
        current_rating: Player's current Elo rating
        expected_win_probability: Expected probability of winning (0.0 to 1.0)
        game_result: 1 if won, 0 if lost
        k_factor: K-factor that controls rating volatility (default: 32)
    
    Returns:
        Player's new rating (float)
        
    Examples:
        >>> # Stronger player wins (expected result)
        >>> new_rating = calculate_new_rating(1600, 0.75, 1)
        >>> new_rating > 1600  # Rating increases
        True
        
        >>> # Weaker player wins (upset)
        >>> new_rating = calculate_new_rating(1600, 0.25, 1)
        >>> new_rating - 1600 > calculate_new_rating(1600, 0.75, 1) - 1600
        True  # Bigger rating gain for upset win
    """
    rating_change = k_factor * (game_result - expected_win_probability)
    return current_rating + rating_change


def update_ratings(
    player1_rating: float,
    player2_rating: float,
    winner_id: int,
    player1_id: int,
    player2_id: int,
    k_factor: int = K_FACTOR
) -> tuple[float, float]:
    """
    Update both players' ratings after a match.
    
    Calculates new ratings for both players based on the match result,
    using their pre-match ratings and win probabilities.
    
    Args:
        player1_rating: Player 1's current rating
        player2_rating: Player 2's current rating
        winner_id: ID of the winning player (player1_id or player2_id)
        player1_id: Player 1's ID
        player2_id: Player 2's ID
        k_factor: K-factor for rating volatility (default: 32)
    
    Returns:
        Tuple of (new_player1_rating, new_player2_rating)
        
    Examples:
        >>> p1_new, p2_new = update_ratings(1600, 1600, 1, 1, 2)
        >>> p1_new > 1600  # Winner's rating increases
        True
        >>> p2_new < 1600  # Loser's rating decreases
        True
        >>> abs(p1_new - p2_new) < 64  # Ratings don't diverge too much
        True
    """
    # Calculate expected win probabilities
    expected_p1, expected_p2 = calculate_win_probability(player1_rating, player2_rating)
    
    # Determine game results (1 = win, 0 = loss)
    p1_result = 1 if winner_id == player1_id else 0
    p2_result = 1 if winner_id == player2_id else 0
    
    # Calculate new ratings
    new_p1_rating = calculate_new_rating(
        player1_rating,
        expected_p1,
        p1_result,
        k_factor
    )
    new_p2_rating = calculate_new_rating(
        player2_rating,
        expected_p2,
        p2_result,
        k_factor
    )
    
    return new_p1_rating, new_p2_rating


def get_rating_change(
    current_rating: float,
    opponent_rating: float,
    game_result: int,
    k_factor: int = K_FACTOR
) -> int:
    """
    Calculate the rating change for a single player in a match.
    
    Useful for displaying how much a rating changed after a match.
    
    Args:
        current_rating: Player's current rating
        opponent_rating: Opponent's current rating
        game_result: 1 if won, 0 if lost
        k_factor: K-factor (default: 32)
    
    Returns:
        Rating change (positive or negative integer)
        
    Examples:
        >>> # Strong player wins (small gain)
        >>> change = get_rating_change(1700, 1600, 1)
        >>> 0 < change < 10  # Small positive change
        True
        
        >>> # Weak player wins (large gain)
        >>> change = get_rating_change(1500, 1600, 1)
        >>> change > 20  # Large positive change
        True
    """
    expected_win_prob, _ = calculate_win_probability(current_rating, opponent_rating)
    return round(k_factor * (game_result - expected_win_prob))


def get_initial_rating() -> float:
    """Get the initial rating for a new player."""
    return float(INITIAL_RATING)


def get_k_factor(rating: float, match_count: int = 0) -> int:
    """
    Get the appropriate K-factor based on player rating and match history.
    
    K-Factor defines volatility (how much rating changes per match):
    - Novice (< 5 matches): K=32 (large changes)
    - Intermediate (5+ matches, rating < 2200): K=24 (medium changes)  
    - Master (rating >= 2200): K=16 (small changes)
    
    Args:
        rating: Player's current rating
        match_count: Number of matches played
    
    Returns:
        K-factor value (int)
    """
    if match_count < 5:
        return 32  # Novice
    elif rating >= 2200:
        return 16  # Master
    else:
        return 24  # Intermediate


def calculate_match_outcome(
    player1_rating: float,
    player2_rating: float,
    winner_id: int,
    player1_id: int,
    player2_id: int,
    k_factor: int = None,
    player1_match_count: int = 0,
    player2_match_count: int = 0
) -> dict:
    """
    Calculate detailed match outcome including rating changes.
    
    Returns a dictionary with new ratings and rating changes for both players.
    
    Args:
        player1_rating: Player 1's rating before match
        player2_rating: Player 2's rating before match
        winner_id: ID of winning player (player1_id or player2_id)
        player1_id: Player 1's ID
        player2_id: Player 2's ID
        k_factor: K-factor (if None, calculated dynamically)
        player1_match_count: Number of matches player 1 played
        player2_match_count: Number of matches player 2 played
    
    Returns:
        Dictionary with:
            - player1_new_rating: Player 1's new rating
            - player2_new_rating: Player 2's new rating
            - player1_change: Rating change for player 1
            - player2_change: Rating change for player 2
            - player1_k_factor: K-factor used for player 1
            - player2_k_factor: K-factor used for player 2
    """
    # Calculate K-factors if not provided
    if k_factor is None:
        k_factor_p1 = get_k_factor(player1_rating, player1_match_count)
        k_factor_p2 = get_k_factor(player2_rating, player2_match_count)
        # Use player1's k_factor for consistency
        k_factor_to_use = k_factor_p1
    else:
        k_factor_p1 = k_factor
        k_factor_p2 = k_factor
        k_factor_to_use = k_factor
    
    # Calculate new ratings
    new_rating_p1, new_rating_p2 = update_ratings(
        player1_rating,
        player2_rating,
        winner_id,
        player1_id,
        player2_id,
        k_factor_to_use
    )
    
    return {
        'player1_new_rating': new_rating_p1,
        'player2_new_rating': new_rating_p2,
        'player1_change': round(new_rating_p1 - player1_rating, 1),
        'player2_change': round(new_rating_p2 - player2_rating, 1),
        'player1_k_factor': k_factor_p1,
        'player2_k_factor': k_factor_p2
    }

