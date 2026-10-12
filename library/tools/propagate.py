"""Units an entry creates bring their role along: an entry that summons or generates a card marked as an empty body, slot filler,
fodder or junk gets that concept too (method via_link). Usage: propagate.py <db>"""
import sqlite3, sys
c = sqlite3.connect(sys.argv[1])
ROLES = ('null_body', 'slot_filler', 'fodder', 'junk_cards', 'board_clog')
c.execute("delete from entity_concepts where method='via_link'")
n = 0
for src, dst, rel in c.execute("select src,dst,rel from entity_links where rel in ('summons','generates','transforms_into')").fetchall():
    for (con,) in c.execute(f"select concept from entity_concepts where entity=? and role='does' and concept in ({','.join('?'*len(ROLES))})", (dst, *ROLES)).fetchall():
        if con == 'board_clog': continue   # whose side it lands on is in the creator's own text
        c.execute("insert or ignore into entity_concepts values(?,?,?,?,?)", (src, con, 'does', 'via_link', f'{rel} a card that is {con}')); n += c.total_changes and 1
c.commit()
print('propagated', c.execute("select count(*) from entity_concepts where method='via_link'").fetchone()[0])
