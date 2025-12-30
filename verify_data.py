
from odoo import api, SUPERUSER_ID

def verify(env):
    count = env['hotel.room'].search_count([])
    with open('/mnt/extra-addons/vertical-hotel/verify_result.txt', 'w') as f:
        f.write(f"ROOM_COUNT:{count}")

if __name__ == '__main__':
    verify(env)
