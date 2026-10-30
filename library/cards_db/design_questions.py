"""Kaptain's design questions, asked of every game, with their real answers: one file per question in
library/design_questions/, and its index README.md. Rerun after every rebuild; read the answers like a designer would:
a wrong or thin answer is a data or question error to fix by cause.
Usage: design_questions.py"""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'design_questions')
QUESTIONS = [  # (file, Kaptain's question, ask.py arguments)
    ('01-mechanic-in-games', 'How does this mechanic work in each game? (sacrifice)', 'all compare sacrifice'),
    ('02-disable-enemies', 'How can a faction stop enemy units from acting?', 'all compare suppress'),
    ('03-combos-of-combos', 'Which combos chain into other combos? (from revive)', 'all chains revive'),
    ('04-family-viable', 'Is a family of features viable for a faction? (sacrifice and card draw)', 'all kit sacrifice draw'),
    ('05-card-ideas', 'Ideas for cards that do X and Y (sacrifice and draw; heal and damage)', 'all both sacrifice draw', 'all both heal damage'),
    ('06-works-with', 'What works well with this mechanic? (damage over time)', 'all feeds damage_over_time', 'all together damage_over_time'),
    ('07-staying-power', 'How to make a faction with staying power?', 'all kit protection heal cheat_death'),
    ('08-disruptive', 'How to make a disruptive faction?', 'all kit disruption suppress'),
    ('09-map-control', 'How to make a faction that controls spots on the map?', 'all kit zone_control movement'),
    ('10-spell-centric', 'How to make a spell-centric faction?', 'all kit spells_played_condition spell_power'),
    ('11-go-wide-tribe', 'How to make a go-wide faction around one unit type?', 'all kit tribal summon'),
    ('12-death-and-return', 'How to make a faction whose units die and come back?', 'all kit sacrifice revive'),
    ('13-positional', 'How to make a faction that pushes and pulls enemies?', 'all kit forced_movement movement'),
    ('14-card-flow', 'How to make a faction that out-draws the enemy?', 'all kit card_advantage cost_reduction'),
    ('15-tricks', 'How to make a faction of hidden tricks and traps?', 'all kit stealth trap_secret'),
    ('16-what-feeds-revive', 'What sets off revive cards?', 'all fed revive'),
]


def ask(args):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'ask.py')] + split(args), capture_output=True, text=True, cwd=HERE)
    return (r.stdout + r.stderr).strip()


def split(a):
    import shlex
    return shlex.split(a)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    index = ['# Design questions and their answers', '',
             'Made by `cards_db/design_questions.py` from the card database; every question asked of every game. A concept also',
             'finds the concepts under it. Cards are shown with their texts when a game has 10 or fewer.', '']
    for f, title, *cmds in QUESTIONS:
        body = [f'# {title}', '']
        for a in cmds:
            body += [f'`ask.py {a}`', '', '```', ask(a), '```', '']
        open(os.path.join(OUT, f + '.md'), 'w', encoding='utf-8').write('\n'.join(body))
        index.append(f'- [{title}]({f}.md): ' + ', '.join(f'`{a}`' for a in cmds))
    open(os.path.join(OUT, 'README.md'), 'w', encoding='utf-8').write('\n'.join(index) + '\n')
    print(len(QUESTIONS), 'questions written to', os.path.relpath(OUT, HERE))
