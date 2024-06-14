from pony.orm import db_session
from app.db.db import *


if __name__ == "__main__":
    add_room(1, 'Самурай', 'Зал в стиле японского милитаризма', 'https://gcdnb.pbrd.co/images/lIemefZGSwZo.png')
    add_room(2, "Дзен", "Светлый зал для спокойных чаепитий", "https://gcdnb.pbrd.co/images/J0ilUDPZNAsI.webp")
    add_table(1, 1, 4, 200)
    add_table(1, 2, 4, 200)
    add_table(1, 3, 4, 200)
    add_table(1, 4, 6, 350)
    add_table(2, 1, 4, 200)
    add_table(2, 2, 4, 200)
    add_table(2, 3, 4, 200)