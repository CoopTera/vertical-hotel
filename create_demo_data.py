
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def create_demo_data(env):
    print("START: Creating Hotel Demo Data...")
    _logger.info("START: Creating Hotel Demo Data...")
    
    # 1. Room Types
    RoomType = env['hotel.room.type']
    if not RoomType.search_count([('name', '=', 'Estándar')]):
        rt_standard = RoomType.create({'name': 'Estándar'})
        print("Created Estándar")
    else:
        rt_standard = RoomType.search([('name', '=', 'Estándar')], limit=1)

    if not RoomType.search_count([('name', '=', 'Deluxe')]):
        rt_deluxe = RoomType.create({'name': 'Deluxe'})
        print("Created Deluxe")
    else:
        rt_deluxe = RoomType.search([('name', '=', 'Deluxe')], limit=1)

    if not RoomType.search_count([('name', '=', 'Suite')]):
        rt_suite = RoomType.create({'name': 'Suite'})
        print("Created Suite")
    else:
        rt_suite = RoomType.search([('name', '=', 'Suite')], limit=1)

    # 2. Amenities Categories
    AmenitiesType = env['hotel.room.amenities.type']
    cats = {'Baño': 'Baño', 'Entretenimiento': 'Entretenimiento', 'Confort': 'Confort'}
    cat_objs = {}
    for key, val in cats.items():
        if not AmenitiesType.search_count([('name', '=', val)]):
            cat_objs[key] = AmenitiesType.create({'name': val})
            print(f"Created Amenity Type {val}")
        else:
            cat_objs[key] = AmenitiesType.search([('name', '=', val)], limit=1)

    # 3. Amenities
    Amenities = env['hotel.room.amenities']
    def create_amenity(name, categ_obj):
        if not Amenities.search_count([('name', '=', name)]):
            Amenities.create({
                'name': name,
                'amenities_categ_id': categ_obj.id,
                'list_price': 0.0,
                'type': 'service',
                'base_unit_count': 1.0,
            })
            print(f"Created Amenity {name}")
        else:
            print(f"Amenity {name} already exists")

    create_amenity('WiFi Gratis', cat_objs['Entretenimiento'])
    create_amenity('TV LED 42"', cat_objs['Entretenimiento'])
    create_amenity('Aire Acondicionado', cat_objs['Confort'])
    create_amenity('Minibar', cat_objs['Confort'])
    create_amenity('Ducha', cat_objs['Baño'])
    create_amenity('Bañera', cat_objs['Baño'])

    # 4. Rooms
    Room = env['hotel.room']
    # Helper to get all amenities
    all_amenities = Amenities.search([])
    
    def create_room(name, r_type, price, cap_a, cap_c):
        if not Room.search_count([('name', '=', name)]):
            Room.create({
                'name': name,
                'room_categ_id': r_type.id,
                'list_price': price,
                'max_adult': cap_a,
                'max_child': cap_c,
                'room_amenities': [(6, 0, all_amenities.ids)],
                'isroom': True,
                'type': 'service',
                'base_unit_count': 1.0,
            })
            print(f"Created Room {name}")
        else:
            print(f"Room {name} already exists")

    create_room('Habitación 101', rt_standard, 1500.0, 2, 1)
    create_room('Habitación 102', rt_standard, 1500.0, 2, 1)
    create_room('Habitación 201 Deluxe', rt_deluxe, 2500.0, 2, 2)
    create_room('Suite 301', rt_suite, 4000.0, 4, 2)

    # 5. Services
    ServiceType = env['hotel.service.type']
    s_types = {'Spa': 'Spa y Bienestar', 'Lau': 'Lavandería', 'Trans': 'Transporte'}
    st_objs = {}
    for k, v in s_types.items():
        if not ServiceType.search_count([('name', '=', v)]):
            st_objs[k] = ServiceType.create({'name': v})
            print(f"Created Service Type {v}")
        else:
            st_objs[k] = ServiceType.search([('name', '=', v)], limit=1)

    Services = env['hotel.services']
    def create_service(name, st_obj, price):
        if not Services.search_count([('name', '=', name)]):
            Services.create({
                'name': name,
                'service_categ_id': st_obj.id,
                'list_price': price,
                'type': 'service',
                'isservice': True,
                'base_unit_count': 1.0,
            })
            print(f"Created Service {name}")

    create_service('Masaje Relajante', st_objs['Spa'], 800.0)
    create_service('Servicio de Lavandería', st_objs['Lau'], 300.0)
    create_service('Traslado Aeropuerto', st_objs['Trans'], 500.0)

    env.cr.commit()
    print("FINISHED: All demo data created successfully!")

if __name__ == '__main__':
    try:
        create_demo_data(env)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        env.cr.rollback()
