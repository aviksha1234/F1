"""Automated verification suite for F1 Pit Stop Master.
Exercises all game states, math, audio, data persistence, AI adaptation, and rendering.
"""
import sys
import os
import pygame

# Set dummy video driver for headless test if needed, or normal
os.environ["SDL_VIDEODRIVER"] = "dummy"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from game.constants import (
    CHAMPIONSHIP_CIRCUITS, DIFFICULTY_DATA, STATE_INTRO, STATE_MENU,
    STATE_CAR_SELECT, STATE_DIFFICULTY, STATE_RACE, STATE_PIT_COMMAND,
    STATE_PIT_LANE, STATE_TASK_REMOVE_WHEELS, STATE_TASK_INSTALL_TYRES,
    STATE_TASK_WHEEL_GUN, STATE_TASK_FRONT_WING, STATE_TASK_RELEASE,
    STATE_AI_COMPARISON, STATE_PERF_ANALYSIS, STATE_GARAGE, STATE_UPGRADES,
    STATE_CHAMPIONSHIP, STATE_LEADERBOARD, STATE_SETTINGS, STATE_PAUSE,
    STATE_GAME_OVER, STATE_VICTORY
)
from game.sound_manager import SoundManager
from game.graphics import GraphicsRenderer
from game.particles import ParticleSystem
from game.player import Player
from game.car import CAR_CATALOG, get_car_by_id
from game.pitcrew import PitCrew
from game.ai import AIPitCrew
from game.race import RaceSimulation
from game.pitstop import PitStopManager
from game.scoring import calculate_pit_score, generate_race_engineer_analysis
from game.leaderboard import Leaderboard
from game.upgrades import UPGRADES_DEFINITION, get_upgrade_cost, get_upgrade_bonus

def test_subsystems():
    print(">> Step 1: Initializing pygame and core subsystems...")
    pygame.init()
    sound = SoundManager()
    renderer = GraphicsRenderer()
    particles = ParticleSystem()
    player = Player()
    leaderboard = Leaderboard()
    pitcrew = PitCrew()
    ai = AIPitCrew("MEDIUM")
    print("   Subsystems initialized successfully.")

    print(">> Step 2: Testing SoundManager SFX & Music...")
    for s_name in sound.sounds:
        sound.play_sfx(s_name)
    sound.start_music()
    sound.stop_music()
    sound.toggle_music()
    sound.toggle_sfx()
    sound.set_master_volume(0.5)
    print("   SoundManager passed.")

    print(">> Step 3: Testing GraphicsRenderer & procedural assets...")
    surf = pygame.Surface((1280, 720))
    renderer.draw_carbon_background(surf)
    renderer.draw_glowing_panel(surf, (100, 100, 200, 100))
    renderer.draw_button(surf, (100, 220, 150, 40), "TEST BTN", hovered=True)
    renderer.draw_f1_car_side(surf, 200, 300, scale=1.5, damaged_wing=True)
    renderer.draw_topdown_f1_car(surf, 500, 300, heading_angle=45.0)
    for maya_state in ["IDLE", "RUNNING", "KNEELING", "GUNNING", "CHECKING", "SIGNALING"]:
        renderer.draw_maya_mechanic(surf, 700, 200, state=maya_state, anim_time=1.2)
    renderer.draw_pit_box_environment(surf, 0, 0, 1280, 720)
    print("   GraphicsRenderer passed all procedural drawing tests.")

    print(">> Step 4: Testing Player Save/Load and Upgrades...")
    orig_coins = player.coins
    player.add_coins(1000)
    assert player.coins == orig_coins + 1000, "Coin addition mismatch"
    success, cost = player.purchase_upgrade("wheel_gun")
    assert success, f"Upgrade purchase failed (cost: {cost})"
    player.save()
    player.load()
    assert player.upgrades["wheel_gun"] >= 2, "Upgrade level persistence mismatch"
    print("   Player persistence & upgrades passed.")

    print(">> Step 5: Testing AI Pit Crew & Adaptive AI Engine...")
    t_sim, splits = ai.simulate_pit_stop()
    assert 1.80 <= t_sim <= 5.0, f"Simulated time out of realistic bounds: {t_sim}"
    # Test adaptation
    player.stats["recent_pit_times"] = [2.10, 2.05, 2.12]
    adapted, msg = ai.check_adaptation(player.stats)
    assert adapted, "AI should have adapted to fast times"
    assert ai.adapted_target is not None, "Adapted target should be set"
    print(f"   AI Pit Crew passed. Adapted message:\n{msg}")

    print(">> Step 6: Testing Race Simulation & Telemetry...")
    car = CAR_CATALOG[0]
    race = RaceSimulation(CHAMPIONSHIP_CIRCUITS[0], car, sound, particles)
    # Simulate keys pressed
    keys = {pygame.K_UP: True, pygame.K_w: False, pygame.K_DOWN: False,
            pygame.K_s: False, pygame.K_LEFT: False, pygame.K_RIGHT: True,
            pygame.K_a: False, pygame.K_d: False}
    race.handle_input(keys, 0.1)
    race.update(1.0)
    race.trigger_random_event()
    react = race.confirm_pit_entry()
    assert react > 0, "Reaction time should be recorded"
    race.draw(surf, renderer)
    print("   RaceSimulation passed.")

    print(">> Step 7: Testing 5 Pit Stop Tasks...")
    pitstop = PitStopManager(player, car, sound, particles, pitcrew)
    pitstop.start_pit_timer()

    # Task 1: Wheel Removal sequence
    for wid in ["FL", "FR", "RL", "RR"]:
        c = pitstop.hub_coords[wid]
        done = pitstop.handle_wheel_removal_click(c)
    assert all(pitstop.wheels_removed.values()), "All wheels should be removed"
    pitstop.draw_task_remove_wheels(surf, renderer)

    # Task 2: Tyre Drag & Snap
    for tyre in pitstop.new_tyres:
        wid = tyre["id"]
        target = pitstop.hub_coords[wid]
        pitstop.handle_tyre_drag_start((tyre["x"], tyre["y"]))
        pitstop.handle_tyre_drag_motion(target)
        pitstop.handle_tyre_drag_release(target)
    assert all(t["locked"] for t in pitstop.new_tyres), "All tyres should be locked"
    pitstop.draw_task_install_tyres(surf, renderer)

    # Task 3: Wheel Gun Timing
    pitstop.gun_needle_pos = 0.50 # Dead center
    pitstop.trigger_wheel_gun()
    assert pitstop.gun_accuracy == "PERFECT", "Dead center should be PERFECT"
    pitstop.draw_task_wheel_gun(surf, renderer)

    # Task 4: Front Wing Decision
    pitstop.make_wing_decision(change_wing=True)
    assert pitstop.wing_changed, "Wing change should be recorded"
    pitstop.draw_task_front_wing(surf, renderer)

    # Task 5: Pit Release
    pitstop.release_light_state = "GREEN"
    pitstop.green_lit_timestamp = pygame.time.get_ticks() - 100 # 100ms reaction
    pitstop.trigger_release()
    assert pitstop.release_complete, "Release should be complete"
    assert pitstop.total_pit_time > 0, "Total pit time should be calculated"
    pitstop.draw_task_release(surf, renderer)
    print(f"   All 5 Pit Stop Tasks passed. Total Pit Time: {pitstop.total_pit_time:.2f}s")

    print(">> Step 8: Testing Scoring & AI Race Engineer feedback...")
    score, rank, rank_col = calculate_pit_score(pitstop.total_pit_time, 0.35, 0, "PERFECT", 0.10)
    assert 0 <= score <= 100, f"Score out of bounds: {score}"
    analysis = generate_race_engineer_analysis(pitstop.total_pit_time, 0.35, 0, "PERFECT", 0.10, wing_changed=True)
    assert len(analysis) > 30, "Analysis text should be rich and descriptive"
    print(f"   Score: {score} ({rank}). Feedback generated successfully.")

    print(">> Step 9: Testing Leaderboard persistence...")
    leaderboard.add_or_update_entry("TEST_CHAMP", 2.11, 2.25, 94, 5, 1)
    top = leaderboard.get_top(5)
    assert len(top) > 0, "Leaderboard should have entries"
    print(f"   Leaderboard entries verified. Top entry: {top[0]['name']} ({top[0]['fastest_pit']}s)")

    print(">> Step 10: Testing Master Game class & All 22 States transition...")
    from game.game import Game
    game = Game()
    all_states = [
        STATE_INTRO, STATE_MENU, STATE_CAR_SELECT, STATE_DIFFICULTY,
        STATE_RACE, STATE_PIT_COMMAND, STATE_PIT_LANE,
        STATE_TASK_REMOVE_WHEELS, STATE_TASK_INSTALL_TYRES,
        STATE_TASK_WHEEL_GUN, STATE_TASK_FRONT_WING, STATE_TASK_RELEASE,
        STATE_AI_COMPARISON, STATE_PERF_ANALYSIS, STATE_GARAGE,
        STATE_UPGRADES, STATE_CHAMPIONSHIP, STATE_LEADERBOARD,
        STATE_SETTINGS, STATE_PAUSE, STATE_GAME_OVER, STATE_VICTORY
    ]

    # Initialize session state objects for full rendering pass
    game.race_sim = race
    game.pitstop_manager = pitstop
    game.last_pit_result = {
        "player_time": pitstop.total_pit_time,
        "ai_time": 2.45,
        "beat_ai": True,
        "diff_time": 0.18,
        "score": score,
        "rank": rank,
        "rank_color": rank_col,
        "feedback": analysis,
        "reward_coins": 300,
        "ai_adapted": True,
        "adapt_msg": "Target updated to 2.15s"
    }

    for st in all_states:
        game.state = st
        game.update(0.016)
        game.draw()
    print("   All 22 states tested and rendered without any exceptions!")

    print("\n=======================================================")
    print("   ALL VERIFICATION TESTS PASSED SUCCESSFULLY! (100%)")
    print("=======================================================\n")

if __name__ == "__main__":
    test_subsystems()
