"""
Bracket Generator for Different Tournament Types

Generates brackets for:
- Single Elimination
- Swiss System
- Group + Knockout
- Round Robin
"""

import math
import random
from typing import List, Dict, Any
from enum import Enum


class BracketGenerator:
    """Generates tournament brackets based on tournament type"""
    
    def generate(
        self,
        tournament_type: str,
        participants_ids: List[int],
        best_of: int = 1,
        num_groups: int = 2,
        swiss_rounds: int = 3,
        seed: int = None
    ) -> Dict[str, Any]:
        """
        Generate bracket structure for tournament
        
        Args:
            tournament_type: SINGLE_ELIMINATION, SWISS, GROUP_KNOCKOUT, ROUND_ROBIN
            participants_ids: List of player IDs
            best_of: For SINGLE_ELIMINATION (1, 3, 5, or 7)
            num_groups: For GROUP_KNOCKOUT (2-16)
            swiss_rounds: For SWISS (1-10)
            seed: Random seed for reproducible brackets
        
        Returns:
            Dict with bracket structure
        """
        if seed:
            random.seed(seed)
        
        if tournament_type == "SINGLE_ELIMINATION":
            return self._generate_single_elimination(participants_ids, best_of)
        elif tournament_type == "SWISS":
            return self._generate_swiss(participants_ids, swiss_rounds)
        elif tournament_type == "GROUP_KNOCKOUT":
            return self._generate_group_knockout(participants_ids, num_groups)
        elif tournament_type == "ROUND_ROBIN":
            return self._generate_round_robin(participants_ids)
        else:
            raise ValueError(f"Unknown tournament type: {tournament_type}")
    
    # ============ Single Elimination ============
    
    def _generate_single_elimination(
        self,
        participants_ids: List[int],
        best_of: int = 1
    ) -> Dict[str, Any]:
        """
        Generate single elimination bracket
        
        Structure:
        - Round 1: All players (seeded)
        - Round 2: Winners of Round 1
        - ... continue until 1 winner
        
        Returns bracket with seeding and match structure.
        """
        n_players = len(participants_ids)
        
        # Validate number of players
        if n_players < 2:
            raise ValueError(f"Need at least 2 players (have {n_players})")
        
        # Calculate number of rounds needed
        n_rounds = math.ceil(math.log2(n_players))
        
        # Calculate total slots needed (power of 2)
        total_slots = 2 ** n_rounds
        
        # Seed the bracket (ideally ranked)
        seeded_players = self._seed_players(participants_ids, total_slots)
        
        # Generate matches for each round
        bracket = {
            "type": "SINGLE_ELIMINATION",
            "total_rounds": n_rounds,
            "best_of": best_of,
            "rounds": {}
        }
        
        # Round 1: Pair adjacent seeded players
        current_round = 1
        matchups = []
        for i in range(0, len(seeded_players), 2):
            p1 = seeded_players[i]
            p2 = seeded_players[i + 1] if i + 1 < len(seeded_players) else None
            
            match = {
                "match_id": f"R{current_round}M{len(matchups) + 1}",
                "round": current_round,
                "p1_id": p1,
                "p2_id": p2,
                "winner_id": None,
                "status": "PENDING"
            }
            matchups.append(match)
        
        bracket["rounds"][current_round] = matchups
        
        # Subsequent rounds: Winners advance
        for round_num in range(2, n_rounds + 1):
            prev_winners = len(bracket["rounds"][round_num - 1])
            matchups = []
            
            for i in range(0, prev_winners, 2):
                match = {
                    "match_id": f"R{round_num}M{len(matchups) + 1}",
                    "round": round_num,
                    "p1_id": None,  # Will be filled as prev round progresses
                    "p2_id": None,
                    "winner_id": None,
                    "status": "PENDING"
                }
                matchups.append(match)
            
            bracket["rounds"][round_num] = matchups
        
        return bracket
    
    # ============ Swiss System ============
    
    def _generate_swiss(
        self,
        participants_ids: List[int],
        num_rounds: int = 3
    ) -> Dict[str, Any]:
        """
        Generate Swiss system bracket
        
        Structure:
        - Round 1: Random pairings
        - Subsequent rounds: Pair players with similar records
        
        Returns bracket with round-by-round pairings.
        """
        n_players = len(participants_ids)
        
        if n_players < 2:
            raise ValueError(f"Need at least 2 players (have {n_players})")
        
        # Shuffle for initial random pairing
        shuffled = participants_ids.copy()
        random.shuffle(shuffled)
        
        bracket = {
            "type": "SWISS",
            "total_rounds": num_rounds,
            "rounds": {},
            "standings": {player_id: {"wins": 0, "losses": 0} for player_id in participants_ids}
        }
        
        current_players = shuffled.copy()
        
        for round_num in range(1, num_rounds + 1):
            # Sort by wins (descending), then by losses (ascending)
            sorted_players = sorted(
                current_players,
                key=lambda p_id: (
                    bracket["standings"][p_id]["wins"],
                    -bracket["standings"][p_id]["losses"]
                ),
                reverse=True
            )
            
            # Create pairings using "fold" method
            matchups = []
            n = len(sorted_players)
            
            for i in range(n // 2):
                match = {
                    "match_id": f"R{round_num}M{i + 1}",
                    "round": round_num,
                    "p1_id": sorted_players[i],
                    "p2_id": sorted_players[n - 1 - i],
                    "winner_id": None,
                    "status": "PENDING"
                }
                matchups.append(match)
            
            # Handle bye (if odd number of players)
            if n % 2 == 1:
                matchups.append({
                    "match_id": f"R{round_num}M{n // 2 + 1}",
                    "round": round_num,
                    "p1_id": sorted_players[n // 2],
                    "p2_id": None,  # Bye
                    "winner_id": sorted_players[n // 2],  # Auto-win
                    "status": "COMPLETED"
                })
            
            bracket["rounds"][round_num] = matchups
        
        return bracket
    
    # ============ Group + Knockout ============
    
    def _generate_group_knockout(
        self,
        participants_ids: List[int],
        num_groups: int = 2
    ) -> Dict[str, Any]:
        """
        Generate group stage + knockout bracket
        
        Structure:
        - Phase 1: Groups (round robin within each group)
        - Phase 2: Knockout (top players from each group)
        
        Returns bracket with group assignments and knockout structure.
        """
        n_players = len(participants_ids)
        
        if n_players < num_groups * 2:
            raise ValueError(f"Need at least {num_groups * 2} players for {num_groups} groups")
        
        # Distribute players into groups
        players_per_group = math.ceil(n_players / num_groups)
        shuffled = participants_ids.copy()
        random.shuffle(shuffled)
        
        groups = {}
        for group_idx in range(num_groups):
            start = group_idx * players_per_group
            end = start + players_per_group
            groups[f"Group_{chr(65 + group_idx)}"] = shuffled[start:end]
        
        bracket = {
            "type": "GROUP_KNOCKOUT",
            "num_groups": num_groups,
            "phases": {
                "group_stage": {
                    "groups": groups,
                    "rounds": {}
                },
                "knockout_stage": {
                    "rounds": {}
                }
            }
        }
        
        # Generate group stage matches (round robin)
        for group_name, group_players in groups.items():
            matchups = []
            match_id = 0
            
            for i in range(len(group_players)):
                for j in range(i + 1, len(group_players)):
                    match_id += 1
                    match = {
                        "match_id": f"{group_name}_M{match_id}",
                        "round": 1,
                        "p1_id": group_players[i],
                        "p2_id": group_players[j],
                        "winner_id": None,
                        "status": "PENDING",
                        "group": group_name
                    }
                    matchups.append(match)
            
            bracket["phases"]["group_stage"]["rounds"][group_name] = matchups
        
        # Generate knockout stage (top player from each group advances)
        knockout_players = [group_players[0] for group_players in groups.values()]
        knockout_bracket = self._generate_single_elimination(
            knockout_players,
            best_of=1
        )
        bracket["phases"]["knockout_stage"]["rounds"] = knockout_bracket["rounds"]
        
        return bracket
    
    # ============ Round Robin ============
    
    def _generate_round_robin(
        self,
        participants_ids: List[int]
    ) -> Dict[str, Any]:
        """
        Generate round robin bracket (all vs all)
        
        Every player plays every other player once.
        
        Returns bracket with all pairings.
        """
        n_players = len(participants_ids)
        
        if n_players < 2:
            raise ValueError(f"Need at least 2 players (have {n_players})")
        
        bracket = {
            "type": "ROUND_ROBIN",
            "total_players": n_players,
            "total_matches": n_players * (n_players - 1) // 2,
            "rounds": {}
        }
        
        # Generate all unique pairings
        matchups = []
        match_id = 0
        
        for i in range(n_players):
            for j in range(i + 1, n_players):
                match_id += 1
                match = {
                    "match_id": f"M{match_id}",
                    "round": 1,  # All matches in one round conceptually
                    "p1_id": participants_ids[i],
                    "p2_id": participants_ids[j],
                    "winner_id": None,
                    "status": "PENDING"
                }
                matchups.append(match)
        
        bracket["rounds"][1] = matchups
        
        return bracket
    
    # ============ Helper Methods ============
    
    def _seed_players(
        self,
        participants_ids: List[int],
        total_slots: int
    ) -> List[int]:
        """
        Seed players for single elimination bracket
        
        Uses "balanced seeding" to spread top players throughout bracket.
        """
        n_players = len(participants_ids)
        seeded = [None] * total_slots
        
        # Simple seeding: alternate high and low seed positions
        low = 0
        high = total_slots - 1
        
        for idx, player_id in enumerate(participants_ids):
            if idx % 2 == 0:
                seeded[low] = player_id
                low += 1
            else:
                seeded[high] = player_id
                high -= 1
        
        return seeded
    
    def calculate_match_count(
        self,
        n_players: int,
        tournament_type: str,
        num_groups: int = 2
    ) -> int:
        """
        Calculate total number of matches for tournament type
        """
        if tournament_type == "SINGLE_ELIMINATION":
            return n_players - 1
        elif tournament_type == "SWISS":
            # Approximate (varies with rounds)
            return n_players * 3 // 2
        elif tournament_type == "GROUP_KNOCKOUT":
            # Group stage + knockout
            group_size = math.ceil(n_players / num_groups)
            group_matches = num_groups * (group_size * (group_size - 1) // 2)
            knockout_matches = num_groups - 1
            return group_matches + knockout_matches
        elif tournament_type == "ROUND_ROBIN":
            return n_players * (n_players - 1) // 2
        else:
            raise ValueError(f"Unknown tournament type: {tournament_type}")
