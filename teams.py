"""Team model for Form-a-word.

Requirement: 4 teams, each with 6 members.
"""

from dataclasses import dataclass, field
import random
from typing import List, Optional


@dataclass
class Member:
    username: str
    password: str  # In production code, store hashes not plaintext


@dataclass
class Team:
    name: str
    members: List[Member] = field(default_factory=list)


FREE_FIRE_TEAM_NAMES = [
    "Phoenix Brigade",
    "Shadow Battalion",
    "Royale Hunters",
    "Crimson Squadron",
]

WARSHIP_TEAM_NAMES = [
    "Ironclad Armada",
    "Tempest Fleet",
    "Leviathan Squadron",
    "Kraken Division",
]

FREE_FIRE_WEAPONS = [
    "M4A1", "SCAR", "AK47", "FAMAS", "FNFAL", "AUG", "QBZ", "G36",
    "Vector", "MP5", "UMP45", "UMP9", "Micro UZI", "UMP", "P90", "MP40",
    "M14", "M79", "AWM", "M82B", "Dragunov", "Kar98", "VSS", "SVD",
    "S686", "S1897", "SPAS12", "M1014", "M870", "RGS50", "C4", "Grenade",
    "Pistol", "Desert Eagle", "Glock", "P92", "P99", "P1911", "Dual Berettas",
    "Uzi", "Mini Uzi", "Tommy Gun", "Revolver", "Tactical Shotgun", "M9",
    "R870", "SAW", "Minigun", "Crossbow", "Hand Cannon", "M500", "Razor",
    "Tactical Rifle", "LMG", "DMR", "Sniper", "SMG", "AR", "SR", "Assault",
    "Karabiner", "Scout", "MK14", "VSS", "MG36", "M249", "Bizon",
    "PP-90", "Type 95", "Type 59", "QBZ-95", "FAMAS", "SCAR-L", "M16A4",
    "AUG A3", "HK416", "FN SCAR", "BFG", "M24", "M40A5", "SSG-69",
    "Tactical Pistol", "Magnum", "Rifle", "SMG X", "AR X", "SR X", "Classic",
    "Legendary AR", "Legendary SMG", "Legendary SR", "Epic Rifle", "Rare Shotgun",
    "Epic Sniper", "Meteor Hammer", "Plasma Gun", "Laser Rifle", "Railgun",
    "Thunderbolt", "Wind Cutter", "Frostbite", "Inferno", "Demi-god Blade",
    "Dragon Shooter", "Phoenix Blaster", "Shadow Reaper", "Serpent Stinger",
    "Cyclone", "Vaporizer", "Annihilator", "Nova", "Titan", "Specter", "Oblivion",
    "Harbinger", "Warden", "Juggernaut", "Cyclops", "Cerberus", "Nightingale", "Ares",
    "Zeus", "Hades", "Apollo", "Athena", "Hermes", "Poseidon", "Artemis", "Hephaestus"
]

WARSHIP_WEAPONS = [
    "Cannons", "Torpedoes", "Depth Charges", "Missile Launchers", "Railguns", "Laser Batteries",
    "Anti-Air Guns", "AA Missiles", "Defensive Drones", "EMP Pulse", "Smoke Screen", "Ram",
    "Boarding Parties", "Net Launchers", "Sonar Mines", "Railcannon Salvo", "Marker Buoy"
]


def get_available_weapon_count(level: int) -> int:
    """Return how many weapons are unlocked for a given level for new users."""
    if level <= 0:
        return 1
    if level <= 10:
        return 5
    if level <= 20:
        return 10
    if level <= 40:
        return 20
    if level <= 60:
        return 40
    if level <= 80:
        return 60
    if level <= 100:
        return 80
    return len(FREE_FIRE_WEAPONS)


def get_random_weapon(level: int, mode: str = "freefire") -> str:
    """Return a random weapon based on mode and level unlock progression."""
    if mode == "warship":
        source = WARSHIP_WEAPONS
    else:
        source = FREE_FIRE_WEAPONS

    max_index = min(len(source), get_available_weapon_count(level))
    available = source[:max_index]
    if not available:
        return "Bare Hands"
    return random.choice(available)


def create_member(team_name: str, index: int) -> Member:
    username = f"{team_name.lower().replace(' ', '_')}_member_{index}"
    password = f"pass{index:04d}"
    return Member(username=username, password=password)


def create_teams(num_teams: int = 4, members_per_team: int = 6) -> List[Team]:
    if num_teams < 1:
        raise ValueError("There must be at least one team")
    if members_per_team < 1:
        raise ValueError("There must be at least one member per team")

    teams = []
    for t in range(1, num_teams + 1):
        team_name = f"Team {t}"
        members = [create_member(team_name, m) for m in range(1, members_per_team + 1)]
        teams.append(Team(name=team_name, members=members))
    return teams


def create_free_fire_teams(members_per_team: int = 6) -> List[Team]:
    if members_per_team < 1:
        raise ValueError("There must be at least one member per team")

    teams = []
    for team_name in FREE_FIRE_TEAM_NAMES:
        members = [create_member(team_name, m) for m in range(1, members_per_team + 1)]
        teams.append(Team(name=team_name, members=members))
    return teams


def create_warship_teams(members_per_team: int = 6) -> List[Team]:
    if members_per_team < 1:
        raise ValueError("There must be at least one member per team")

    teams = []
    for team_name in WARSHIP_TEAM_NAMES:
        members = [create_member(team_name, m) for m in range(1, members_per_team + 1)]
        teams.append(Team(name=team_name, members=members))
    return teams


def authenticate_member(team: Team, username: str, password: str) -> bool:
    for member in team.members:
        if member.username == username and member.password == password:
            return True
    return False


def find_member(teams: List[Team], username: str) -> Optional[Member]:
    """Return member by username searching all teams."""
    for team in teams:
        for member in team.members:
            if member.username == username:
                return member
    return None


def prompt_login(teams: List[Team], max_attempts: int = 3) -> Optional[Member]:
    """Ask user for username/password and authenticate against generated members."""
    print("\n--- User Login ---")
    for attempt in range(1, max_attempts + 1):
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        member = find_member(teams, username)
        if member and member.password == password:
            print(f"Login successful. Welcome, {username}!")
            return member

        print(f"Login failed (attempt {attempt}/{max_attempts}). Try again.")

    print("Maximum login attempts exceeded. Exiting.")
    return None


TRAINING_LEVEL = 0
MAX_FREE_FIRE_LEVELS = 30000


def simulate_free_fire_match(teams: List[Team], max_level: int = MAX_FREE_FIRE_LEVELS, seed: Optional[int] = None, mode: str = "freefire") -> Team:
    if max_level < TRAINING_LEVEL or max_level > MAX_FREE_FIRE_LEVELS:
        raise ValueError(f"max_level must be between {TRAINING_LEVEL} and {MAX_FREE_FIRE_LEVELS}")

    if seed is not None:
        random.seed(seed)

    alive_teams = [team for team in teams if team.members]
    eliminated_teams = []

    mode_name = "War Ships" if mode == "warship" else "Free Fire"
    limb = "cannons" if mode == "warship" else "weapons"
    source_pool = WARSHIP_WEAPONS if mode == "warship" else FREE_FIRE_WEAPONS

    print(f"=== {mode_name} Battle Royale Simulation ===")
    first_level_pool = get_available_weapon_count(1)
    print(f"Initial newbie pool: {first_level_pool} {limb} (full pool {len(source_pool)}).")
    print(f"Simulating training level {TRAINING_LEVEL} and up to level {max_level} with progressive unlock growth.")

    print(f"\n--- Training Level {TRAINING_LEVEL} ---")
    for team in alive_teams:
        for member in team.members:
            weapon = get_random_weapon(TRAINING_LEVEL, mode=mode)
            print(f"{team.name} {member.username} trains with {weapon}")

    if max_level == TRAINING_LEVEL:
        if not alive_teams:
            print("\nlobya: no team survived training")
            raise RuntimeError("No team survived training")
        winner = alive_teams[0]
        print(f"\nbhoyya: {winner.name} (training complete, no elimination levels)")
        return winner

    for level in range(1, max_level + 1):
        if len(alive_teams) <= 1:
            break

        print(f"\n--- Level {level} ---")

        # Assign a random weapon to each surviving squadmate at this level
        assigned = []
        for team in alive_teams:
            for member in team.members:
                weapon = get_random_weapon(level, mode=mode)
                assigned.append((team.name, member, weapon))
        sample_items = random.sample(assigned, min(3, len(assigned)))
        for team_name, member, weapon in sample_items:
            print(f"{team_name} {member} picks up {weapon}")

        # Elimination event
        attacker, defender = random.sample(alive_teams, 2)
        victim = random.choice(defender.members)
        defender.members.remove(victim)
        print(
            f"Level {level} fight: {attacker.name} eliminated {victim} from {defender.name}."
        )

        if not defender.members:
            print(f"{defender.name} has been knocked out!")
            eliminated_teams.append(defender.name)
            alive_teams = [team for team in alive_teams if team.members]

    if not alive_teams:
        # Required presentation: losing path should be announced as "lobya"
        print("\nlobya: no team survived the battle")
        raise RuntimeError("No team survived the battle")

    # Choose the strongest remaining team if multiple survive when max level hits.
    winner = max(alive_teams, key=lambda t: len(t.members))
    losers = [t.name for t in teams if t.name != winner.name]

    print(f"\nbhoyya: {winner.name} with {len(winner.members)} survivor(s) after {level} levels")
    print(f"lobya: lost team(s): {', '.join(losers)}")
    return winner


def main() -> None:
    print("Select mode:")
    print("1) Free Fire (default)")
    print("2) War Ships")
    selection = input("Enter 1 or 2: ").strip()
    mode = "warship" if selection == "2" else "freefire"

    teams = create_warship_teams(6) if mode == "warship" else create_free_fire_teams(6)

    print("=== Available Teams and Members ===")
    for team in teams:
        print(f"{team.name}: {len(team.members)} members")
        for member in team.members:
            print(f" - {member.username}")

    member = prompt_login(teams)
    if not member:
        return

    print()
    simulate_free_fire_match(teams, mode=mode)


if __name__ == "__main__":
    main()
