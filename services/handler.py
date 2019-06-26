from main import app
from .repository import ServiceRepository
from .model import ServiceDTO, Service
from .errors import ServiceListError, ErrorMessages, ErrorCodes, ServiceDeletionError
from infrastructure.dispatching import dispatch
from infrastructure.model import create_dto, create_mapping, update_from
from http import HTTPStatus
from infrastructure.extensions import serialize, odata, get_header_cache_key
from infrastructure.extensions import get_request_timezone
from infrastructure.utils import get_current_time


@app.route('/services', methods=['GET'])
@dispatch(query_string_arg='qs')
def list_services(qs: str = ''):
    with ServiceRepository() as repo:
        result, count = repo.get_service_list(qs)

        if result:
            mapping = create_mapping(result[0], ServiceDTO)

            return serialize(odata(
                count,
                [create_dto(service, ServiceDTO, mapping) for service in result])), HTTPStatus.OK

        else:
            raise ServiceListError(ErrorMessages.NoServicesFound, ErrorCodes.NoService,
                                   http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/services/<string:slug>', methods=['GET'])
@dispatch()
def get_service_info(slug: str):
    with ServiceRepository() as repo:
        service: Service = repo.filter_one(Service.slug == slug)
        if service:
            mapping = create_mapping(service, ServiceDTO)

            return serialize(create_dto(service, ServiceDTO, mapping)), HTTPStatus.OK

        else:
            raise ServiceListError(ErrorMessages.NoServicesFound, ErrorCodes.NoService,
                                   http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/services', methods=['POST'])
@dispatch(no_validation={'created_at'})
def register_service(service: Service):
    with ServiceRepository() as repo:
        current_time = get_current_time(get_request_timezone())
        service.created_at = current_time
        service_id = repo.add(service)

        return serialize({"service_id": service_id}), HTTPStatus.CREATED


@app.route('/services/<string:slug>', methods=['PUT'])
@dispatch(no_validation={'created_at','slug'}, ignore_fields={'created_at','slug'})
def modify_service(slug: str, **kwargs):
    with ServiceRepository() as repo:
        service: Service = repo.filter_one(Service.slug == slug)
        if service:

            update_time = get_current_time(get_request_timezone())
            update_from(service, **kwargs)
            service.updated_at = update_time

            return '', HTTPStatus.NO_CONTENT
        else:
            raise ServiceListError(ErrorMessages.NoServicesFound, ErrorCodes.NoService,
                                   http_status_code=HTTPStatus.NOT_FOUND)



@app.route('/services/<string:slug>', methods=['DELETE'])
@dispatch()
def disable_service(slug: str):
    with ServiceRepository() as repo:
        service: Service = repo.filter_one(Service.slug == slug)
        if service:
            service.is_active = False

            return '', HTTPStatus.NO_CONTENT

        else:
            raise ServiceListError(ErrorMessages.NoServicesFound, ErrorCodes.NoService,
                                   http_status_code=HTTPStatus.NOT_FOUND)
