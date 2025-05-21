import json
from pathlib import Path
from db.models import Player, Race, Skill, Guild
from django.db import transaction


def main():
    file_path = Path(__file__).resolve().parent / "players.json"

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for player_name, details in data.items():
        with transaction.atomic():
            skill_objs = []
            for skill_data in details["race"]["skills"]:
                skill, _ = Skill.objects.get_or_create(
                    name=skill_data["name"],
                    defaults={"bonus": skill_data["bonus"], "race_id": None}
                )
                skill_objs.append(skill)

            race, _ = Race.objects.get_or_create(
                name=details["race"]["name"],
                defaults={"description": details["race"]["description"]}
            )
            if race.skills.count() == 0:
                race.skills.set(skill_objs)

            guild_data = details.get("guild")
            guild = None
            if guild_data:
                guild, _ = Guild.objects.get_or_create(
                    name=guild_data["name"],
                    defaults={"description": guild_data["description"]}
                )

            Player.objects.get_or_create(
                nickname=player_name,
                email=details["email"],
                defaults={
                    "bio": details["bio"],
                    "race": race,
                    "guild": guild,
                }
            )


if __name__ == "__main__":
    main()
