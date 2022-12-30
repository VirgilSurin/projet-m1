import argparse
import datetime
import json
import logging
import pathlib
import sys
import pandas as pd

import bcrypt
import pytz
import tzlocal

from pyjudge.model import (
    JudgeSettings,
    User,
    UserRole,
    Team,
    TeamCategory,
    Affiliation,
    Contest,
    ContestProblem,
)
from pyjudge.model.settings import (
    JudgeInstance,
    ClarificationSettings,
    DisplaySettings,
    ScoringSettings,
    JudgingSettings,
)
from pyjudge.repository.kattis import Repository
from pyjudge.scripts.upload import UsersDescription


def make_settings():
    judge_settings = JudgeSettings(
        judging=JudgingSettings(),
        scoring=ScoringSettings(),
        display=DisplaySettings(),
        clarification=ClarificationSettings(),
    )
    return JudgeInstance(identifier="local", settings=judge_settings, base_time=1.5, user_whitelist=set()).serialize()


def make_contest():
    repository = Repository(pathlib.Path("repository"))
    problem = repository.problems.load_problem("validate_cliques")
    contest_problem = ContestProblem(name="validate_cliques", points=1, color="blue", problem=problem)

    base_time = datetime.datetime.now(tzlocal.get_localzone()).replace(minute=0, second=0, microsecond=0)
    return Contest(
        key="projet-m1",
        name="Projet M1 - maximal cliques",
        activation_time=base_time,
        start_time=base_time,
        freeze_time=None,
        end_time=base_time + datetime.timedelta(days=14),
        deactivation_time=base_time + datetime.timedelta(days=15),
        problems=[contest_problem],
        access=None,
        public_scoreboard=False,
    ).serialize(repository.problems)


def make_users():
    salt = bcrypt.gensalt()
    affiliation = Affiliation(short_name="Umons", name="Umons", country=None)

    user = User(
        login_name="virgil",
        display_name="Virgil",
        email="virgil.surin@student.umons.ac.be",
        password_hash=bcrypt.hashpw(b"virgil", salt).decode(),
        role=UserRole.Participant,
    )
    admin = User(
        login_name="admin",
        display_name="Admin",
        email="admin@localhost",
        password_hash=bcrypt.hashpw(b"admin", salt).decode(),
        role=UserRole.Admin,
    )
    user_team = Team(
        "Virgil",
        display_name="Virgil",
        members=[user],
        category=TeamCategory.Participants,
        affiliation=affiliation,
    )
    admin_team = Team("admin_team", display_name="Admin", members=[admin], category=TeamCategory.Jury, affiliation=None)

    return UsersDescription(users=[user, admin], affiliations=[affiliation], teams=[user_team, admin_team]).serialize()

def create_user_from_file(file_path):
    """
    Return a list of user from the moodle group export
    Creditentials are set to :
        - login_name = SURNAME.Firstname
        - password = SURNAME
    """
    salt = bcrypt.gensalt()
    users = []
    users_team = []
    umons = Affiliation(short_name="umons", name="Université de Mons", country=None)
    salt = bcrypt.gensalt()
    read_file = pd.read_excel(file_path)
    read_file.to_csv("users.csv", index=False, header=False, sep=",")
    with open("users.csv", 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = line.strip().split(",")
            firstname, name, email = line[0], line[1], line[2]
            usr = User(
                login_name=f"{email.lower()}",
                display_name=f"{firstname.lower()}",
                email=email.lower(),
                password_hash=bcrypt.hashpw(name.lower().encode(), salt).decode(),
                role=UserRole.Participant,
            )
            users.append(usr)
            usr_team = Team(
                "team_"+name.lower(),
                display_name=firstname,
                members=[usr],
                category=TeamCategory.Participants,
                affiliation=umons,
            )
            users_team.append(usr_team)
            print(usr_team)
            
    admin = User(
        login_name="admin",
        display_name="Admin",
        email="admin@localhost",
        password_hash=bcrypt.hashpw(b"cpumons42", salt).decode(),
        role=UserRole.Admin,
    )
    admin_team = Team("admin_team", display_name="Admin", members=[admin], category=TeamCategory.Jury, affiliation=None)
    users.append(admin)
    users_team.append(admin_team)
    print(users_team)
    return UsersDescription(users=users, affiliations=[umons], teams=users_team).serialize()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # call with --input <path_to_xlsx_file> to call make_user_from_xlsx
    parser = argparse.ArgumentParser()
        
    parser.add_argument("-O", "--output", type=argparse.FileType('w'), default=sys.stdout, help="File output")
    parser.add_argument("--pretty", action='store_true', help="Pretty-print JSON")

    subparsers = parser.add_subparsers(help="Help for commands")
    settings = subparsers.add_parser("settings", help="Create settings")
    settings.set_defaults(func=make_settings)

    users = subparsers.add_parser("users", help="Create users")
    users.set_defaults(func=make_users)
    
    contest = subparsers.add_parser("contest", help="Create contest")
    contest.set_defaults(func=make_contest)

    args = parser.parse_args()
    with args.output as f:
        json.dump(args.func(), f, indent=2 if args.pretty else None, ensure_ascii=False)






