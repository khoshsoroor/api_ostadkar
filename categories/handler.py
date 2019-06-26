from main import app
from .repository import CategoryRepository
from .model import CategoryDTO, Category
from .errors import CategoryListError, ErrorMessages, ErrorCodes, CategoryDeletionError
from infrastructure.dispatching import dispatch
from infrastructure.model import create_dto, create_mapping, update_from
from http import HTTPStatus
from infrastructure.extensions import serialize, odata, get_header_cache_key
from infrastructure.extensions import get_request_timezone
from infrastructure.utils import get_current_time


@app.route('/categories', methods=['GET'])
@dispatch(query_string_arg='qs')
def list_categories(qs: str = ''):
    with CategoryRepository() as repo:
        result, count = repo.get_category_list(qs)

        if result:
            mapping = create_mapping(result[0], CategoryDTO)

            return serialize(odata(
                count,
                [create_dto(category, CategoryDTO, mapping) for category in result])), HTTPStatus.OK

        else:
            raise CategoryListError(ErrorMessages.NoCategoryFound, ErrorCodes.NoService,
                                    http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/categories/<string:slug>', methods=['GET'])
@dispatch()
def get_category_info(slug: str):
    with CategoryRepository() as repo:
        category: Category = repo.filter_one(Category.slug == slug)
        if category:
            mapping = create_mapping(category, CategoryDTO)

            return serialize(create_dto(category, CategoryDTO, mapping)), HTTPStatus.OK

        else:
            raise CategoryListError(ErrorMessages.NoCategoryFound, ErrorCodes.NoService,
                                    http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/categories', methods=['POST'])
@dispatch(no_validation={'created_at'})
def register_category(service: Category):
    with CategoryRepository() as repo:
        current_time = get_current_time(get_request_timezone())
        service.created_at = current_time
        category_id = repo.add(service)

        return serialize({"service_id": category_id}), HTTPStatus.CREATED


@app.route('/categories/<string:slug>', methods=['PUT'])
@dispatch(no_validation={'created_at', 'slug'}, ignore_fields={'created_at', 'slug'})
def modify_category(slug: str, **kwargs):
    with CategoryRepository() as repo:
        category: Category = repo.filter_one(Category.slug == slug)
        if category:

            update_time = get_current_time(get_request_timezone())
            update_from(category, **kwargs)
            category.updated_at = update_time

            return '', HTTPStatus.NO_CONTENT
        else:
            raise CategoryListError(ErrorMessages.NoCategoryFound, ErrorCodes.NoService,
                                    http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/categories/<string:slug>', methods=['DELETE'])
@dispatch()
def disable_category(slug: str):
    with CategoryRepository() as repo:
        category: Category = repo.filter_one(Category.slug == slug)
        if category:
            category.is_active = False

            return '', HTTPStatus.NO_CONTENT

        else:
            raise CategoryDeletionError(ErrorMessages.NoCategoryFound, ErrorCodes.NoService,
                                        http_status_code=HTTPStatus.NOT_FOUND)
