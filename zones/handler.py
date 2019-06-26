from http import HTTPStatus

from cities.model import City
from cities.repository import CityRepository
from infrastructure.dispatching import dispatch
from infrastructure.extensions import (get_request_timezone, odata, serialize)
from infrastructure.model import create_dto, create_mapping, update_from
from infrastructure.utils import get_current_time
from main import app
from .errors import ErrorCodes, ErrorMessages, ZoneFoundError
from .model import Zone, ZoneDTO
from .repository import ZoneRepository


@app.route('/zones', methods=['GET'])
@dispatch(query_string_arg='qs')
def list_zone(qs: str = ''):
    with ZoneRepository() as repo:
        result, count = repo.get_zone_list(qs)
        if result:
            mapping = create_mapping(result[0], ZoneDTO)
            return serialize(odata(
                count,
                [create_dto(zone, ZoneDTO, mapping) for zone in result])), HTTPStatus.OK
        else:
            raise ZoneFoundError(ErrorMessages.NoZonesFound, ErrorCodes.NoZonesFound,
                                 http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/zones/<string:slug>', methods=['GET'])
@dispatch()
def fetch_zone(slug: str):
    with ZoneRepository() as repo:
        zone: Zone = repo.filter_one_with_lazy(Zone.slug == slug)
        if zone:
            mapping = create_mapping(zone, ZoneDTO)
            return serialize(create_dto(zone, ZoneDTO, mapping)), HTTPStatus.OK
        else:
            raise ZoneFoundError(ErrorMessages.NoZonesFound, ErrorCodes.NoZonesFound,
                                 http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/zones', methods=['POST'])
@dispatch(no_validation={'created_at', 'updated_at'}, ignore_fields={'created_at', 'updated_at'})
def create_zone(zone: Zone, city_slug: str):
    with ZoneRepository() as repo:
        with CityRepository() as city_repo:
            city: City = city_repo.filter_one(City.slug == city_slug)
            zone.city_id = city.city_id
            zone.created_at = get_current_time(get_request_timezone())
            zone_id = repo.add(zone)
            return serialize({"zone_id": zone_id}), HTTPStatus.CREATED


@app.route('/zones/<string:slug>', methods=['PUT'])
@dispatch(no_validation={'created_at', 'updated_at', 'slug'}, ignore_fields={'created_at', 'updated_at', 'slug'})
def update_zone(slug: str, city_slug: str, **kwargs):
    with ZoneRepository() as repo:
        with CityRepository() as city_repo:
            zone: Zone = repo.filter_one(Zone.slug == slug)
            if zone:
                update_from(zone, **kwargs)
                zone.city = city_repo.filter_one(City.slug == city_slug)
                zone.city_id = zone.city.city_id
                zone.updated_at = get_current_time(get_request_timezone())
                return '', HTTPStatus.NO_CONTENT
            else:
                raise ZoneFoundError(ErrorMessages.NoZonesFound, ErrorCodes.NoZonesFound,
                                     http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/zones/<string:slug>', methods=['DELETE'])
@dispatch()
def delete_zone(slug: str):
    with ZoneRepository() as repo:
        zone: Zone = repo.filter_one(Zone.slug == slug)
        if zone:
            zone.is_active = False
            return '', HTTPStatus.NO_CONTENT
        else:
            raise ZoneFoundError(ErrorMessages.NoZonesFound, ErrorCodes.NoZonesFound,
                                 http_status_code=HTTPStatus.NOT_FOUND)
