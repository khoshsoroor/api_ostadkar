from http import HTTPStatus

from cities.model import City
from cities.repository import CityRepository
from infrastructure.dispatching import dispatch
from infrastructure.extensions import (get_request_timezone, odata, serialize)
from infrastructure.model import create_dto, create_mapping, update_from
from infrastructure.utils import get_current_time
from main import app
from services.model import Service
from services.repository import ServiceRepository
from .errors import ErrorCodes, ErrorMessages, ProvideFoundError
from .model import Provide, ProvideDTO
from .repository import ProvideRepository


@app.route('/provides', methods=['GET'])
@dispatch(query_string_arg='qs')
def list_provide(qs: str = ''):
    with ProvideRepository() as repo:
        result, count = repo.get_provide_list(qs)
        if result:
            mapping = create_mapping(result[0], ProvideDTO)
            return serialize(odata(
                count,
                [create_dto(provide, ProvideDTO, mapping) for provide in result])), HTTPStatus.OK
        else:
            raise ProvideFoundError(ErrorMessages.NoProvidesFound, ErrorCodes.NoProvidesFound,
                                    http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/provides/<string:slug>', methods=['GET'])
@dispatch()
def fetch_provide(slug: str):
    with ProvideRepository() as repo:
        provide: Provide = repo.filter_one_with_lazy(Provide.slug == slug)
        if provide:
            mapping = create_mapping(provide, ProvideDTO)
            return serialize(create_dto(provide, ProvideDTO, mapping)), HTTPStatus.OK
        else:
            raise ProvideFoundError(ErrorMessages.NoProvidesFound, ErrorCodes.NoProvidesFound,
                                    http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/provides', methods=['POST'])
@dispatch(no_validation={'created_at', 'updated_at'}, ignore_fields={'created_at', 'updated_at'})
def create_provide(provide: Provide, city_slug: str, service_slug: str):
    print(type(provide.start_at))
    with ProvideRepository() as repo:
        provide.created_at = get_current_time(get_request_timezone())

        with CityRepository() as cityRepository:
            provide.city = cityRepository.filter_one(City.slug == city_slug)
            provide.city_id = provide.city.city_id
        with ServiceRepository() as serviceRepository:
            provide.service = serviceRepository.filter_one(Service.slug == service_slug)
            provide.service_id = provide.service.service_id

        provide_id = repo.add(provide)
        return serialize({"provide_id": provide_id}), HTTPStatus.CREATED


@app.route('/provides/<string:slug>', methods=['PUT'])
@dispatch(no_validation={'created_at', 'updated_at', 'slug'}, ignore_fields={'created_at', 'updated_at', 'slug'})
def update_provide(slug: str, city_slug: str, service_slug: str, **kwargs):
    with ProvideRepository() as repo:
        provide: Provide = repo.filter_one(Provide.slug == slug)
        if provide:
            update_from(provide, **kwargs)
            provide.updated_at = get_current_time(get_request_timezone())

            with CityRepository() as cityRepository:
                provide.city = cityRepository.filter_one(City.slug == city_slug)
                provide.city_id = provide.city.city_id
            with ServiceRepository() as serviceRepository:
                provide.service = serviceRepository.filter_one(Service.slug == service_slug)
                provide.service_id = provide.service.service_id

            return '', HTTPStatus.NO_CONTENT
        else:
            raise ProvideFoundError(ErrorMessages.NoProvidesFound, ErrorCodes.NoProvidesFound,
                                    http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/provides/<string:slug>', methods=['DELETE'])
@dispatch()
def delete_provide(slug: str):
    with ProvideRepository() as repo:
        provide: Provide = repo.filter_one(Provide.slug == slug)
        if provide:
            provide.is_active = False
            return '', HTTPStatus.NO_CONTENT
        else:
            raise ProvideFoundError(ErrorMessages.NoProvidesFound, ErrorCodes.NoProvidesFound,
                                    http_status_code=HTTPStatus.NOT_FOUND)
