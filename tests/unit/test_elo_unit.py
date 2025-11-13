"""
Testes unitários para o sistema ELO.

Validação de:
- Cálculo de win probability
- Cálculo de novo rating
- K-factor dinâmico
- Match outcome completo
"""

import sys
from elo import (
    calculate_win_probability,
    calculate_new_rating,
    update_ratings,
    get_k_factor,
    calculate_match_outcome,
    INITIAL_RATING
)

def test_initial_rating():
    """Verificar se rating inicial é 1200"""
    assert INITIAL_RATING == 1200, f"Initial rating should be 1200, got {INITIAL_RATING}"
    print("✓ Initial rating is 1200")


def test_equal_ratings():
    """Jogadores com rating igual devem ter 50% chance de ganhar"""
    prob_a, prob_b = calculate_win_probability(1200, 1200)
    assert abs(prob_a - 0.5) < 0.001, f"Equal ratings should give 50%, got {prob_a}"
    assert abs(prob_a + prob_b - 1.0) < 0.001, f"Probabilities should sum to 1"
    print(f"✓ Equal ratings: P(A)={prob_a:.3f}, P(B)={prob_b:.3f}")


def test_higher_rating_advantage():
    """Jogador com rating mais alto deve ter vantagem"""
    prob_strong, prob_weak = calculate_win_probability(1400, 1200)
    assert prob_strong > 0.5, f"Higher rating should have > 50%, got {prob_strong}"
    assert prob_weak < 0.5, f"Lower rating should have < 50%, got {prob_weak}"
    print(f"✓ Higher rating advantage: Strong={prob_strong:.3f}, Weak={prob_weak:.3f}")


def test_example_from_spec():
    """
    Exemplo de João (1200) vencendo Maria (1400).
    
    Expected:
    - João ganha ~+22.8
    - Maria perde ~-22.8
    """
    # João vs Maria
    result = calculate_match_outcome(1200, 1400, 1, 1, 2)
    
    print(f"\nExemplo da Especificação: João (1200) vs Maria (1400), João vence")
    print(f"  João: {result['player1_change']:+.1f} (novo: {result['player1_new_rating']:.1f})")
    print(f"  Maria: {result['player2_change']:+.1f} (novo: {result['player2_new_rating']:.1f})")
    
    # Validações
    assert result['player1_change'] > 20, f"João deve ganhar +20~23, ganhou {result['player1_change']}"
    assert result['player2_change'] < -20, f"Maria deve perder -20~23, perdeu {result['player2_change']}"
    print("✓ Exemplo da especificação validado")


def test_k_factor_novice():
    """Novos jogadores (< 5 partidas) devem ter K=32"""
    k = get_k_factor(1200, match_count=2)
    assert k == 32, f"Novice should have K=32, got {k}"
    print(f"✓ Novice K-factor: {k}")


def test_k_factor_intermediate():
    """Intermediários (5+ partidas, rating < 2200) devem ter K=24"""
    k = get_k_factor(1500, match_count=50)
    assert k == 24, f"Intermediate should have K=24, got {k}"
    print(f"✓ Intermediate K-factor: {k}")


def test_k_factor_master():
    """Masters (rating >= 2200) devem ter K=16"""
    k = get_k_factor(2300, match_count=100)
    assert k == 16, f"Master should have K=16, got {k}"
    print(f"✓ Master K-factor: {k}")


def test_dynamic_k_factor():
    """K-factor deve se ajustar baseado em match_count e rating"""
    # Início (< 5 matches)
    k1 = get_k_factor(1200, match_count=3)
    assert k1 == 32
    
    # Depois (intermediate)
    k2 = get_k_factor(1600, match_count=50)
    assert k2 == 24
    
    # Master
    k3 = get_k_factor(2500, match_count=10)
    assert k3 == 16
    
    print(f"✓ Dynamic K-factors: novice={k1}, intermediate={k2}, master={k3}")


def test_upset_win_larger_gain():
    """Ganhar contra alguém muito mais forte deve dar mais pontos"""
    # Weak wins against strong - calcula apenas a diferença de rating, não novo rating
    prob_weak, _ = calculate_win_probability(1200, 1400)
    weak_gain = 32 * (1 - prob_weak)  # 32 * (1 - 0.240)
    
    # Strong wins against weak
    prob_strong, _ = calculate_win_probability(1400, 1200)
    strong_gain = 32 * (1 - prob_strong)  # 32 * (1 - 0.760)
    
    assert weak_gain > strong_gain, \
        f"Upset win should give more points: weak_gain={weak_gain:.1f} vs strong_gain={strong_gain:.1f}"
    
    print(f"✓ Upset advantage: Weak wins +{weak_gain:.1f}, Strong wins +{strong_gain:.1f}")


def test_rating_sum_conservation():
    """Soma total de ratings deve ser conservada em cada match (com K-factor igual)"""
    p1_initial, p2_initial = 1200, 1300
    total_before = p1_initial + p2_initial
    
    # Qualquer um pode ganhar
    new_p1, new_p2 = update_ratings(p1_initial, p2_initial, 1, 1, 2, k_factor=32)
    total_after = new_p1 + new_p2
    
    # Com K-factor fixo, total deve ser conservado
    assert abs(total_after - total_before) < 1, \
        f"Total ratings should be conserved. Before={total_before}, After={total_after}"
    
    print(f"✓ Rating conservation: {total_before} → {total_after} (diff: {total_after - total_before:.2f})")


def test_symmetric_result():
    """Se dois jogadores têm o mesmo rating, o ganho/perda deve ser simétrico"""
    initial_rating = 1200
    
    result = calculate_match_outcome(initial_rating, initial_rating, 1, 1, 2, k_factor=32)
    
    change_p1 = result['player1_change']
    change_p2 = result['player2_change']
    
    assert abs(change_p1 + change_p2) < 0.1, \
        f"Changes should be symmetric for equal ratings: {change_p1} vs {change_p2}"
    assert abs(change_p1) == abs(change_p2), \
        f"Magnitudes should be equal: {abs(change_p1)} vs {abs(change_p2)}"
    
    print(f"✓ Symmetric result: P1={change_p1:+.1f}, P2={change_p2:+.1f}")


def run_all_tests():
    """Executar todos os testes"""
    print("="*60)
    print("TESTES DO SISTEMA ELO")
    print("="*60)
    
    tests = [
        test_initial_rating,
        test_equal_ratings,
        test_higher_rating_advantage,
        test_k_factor_novice,
        test_k_factor_intermediate,
        test_k_factor_master,
        test_dynamic_k_factor,
        test_upset_win_larger_gain,
        test_rating_sum_conservation,
        test_symmetric_result,
        test_example_from_spec,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: Unexpected error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    if failed == 0:
        print("✓ TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print(f"✗ {failed} teste(s) falharam")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
