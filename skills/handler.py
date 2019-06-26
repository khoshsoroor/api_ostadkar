from http import HTTPStatus

from infrastructure.dispatching import dispatch
from infrastructure.extensions import (get_header_cache_key,
                                       get_request_timezone, odata, serialize)
from infrastructure.model import create_dto, create_mapping, update_from
from infrastructure.utils import get_current_time
from main import app

from .errors import ErrorCodes, ErrorMessages, SkillFoundError
from .model import Skill, SkillDTO
from .repository import SkillRepository


@app.route('/skills', methods=['GET'])
@dispatch(query_string_arg='qs')
def list_skill(qs: str = ''):
    with SkillRepository() as repo:
        result, count = repo.get_skill_list(qs)
        if result:
            mapping = create_mapping(result[0], SkillDTO)
            return serialize(odata(
                count,
                [create_dto(skill, SkillDTO, mapping) for skill in result])), HTTPStatus.OK
        else:
            raise SkillFoundError(ErrorMessages.NoSkillsFound, ErrorCodes.NoSkillsFound,
                                  http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/skills/<string:slug>', methods=['GET'])
@dispatch()
def fetch_skill(slug: str):
    with SkillRepository() as repo:
        skill: Skill = repo.filter_one(Skill.slug == slug)
        if skill:
            mapping = create_mapping(skill, SkillDTO)
            return serialize(create_dto(skill, SkillDTO, mapping)), HTTPStatus.OK
        else:
            raise SkillFoundError(ErrorMessages.NoSkillsFound, ErrorCodes.NoSkillsFound,
                                  http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/skills', methods=['POST'])
@dispatch(no_validation={'created_at', 'updated_at'}, ignore_fields={'created_at', 'updated_at'})
def create_skill(skill: Skill):
    with SkillRepository() as repo:
        skill.created_at = get_current_time(get_request_timezone())
        skill_id = repo.add(skill)
        return serialize({"skill_id": skill_id}), HTTPStatus.CREATED


@app.route('/skills/<string:slug>', methods=['PUT'])
@dispatch(no_validation={'created_at', 'updated_at', 'slug'}, ignore_fields={'created_at', 'updated_at', 'slug'})
def update_skill(slug: str, **kwargs):
    with SkillRepository() as repo:
        skill: Skill = repo.filter_one(Skill.slug == slug)
        if skill:
            update_from(skill, **kwargs)
            skill.updated_at = get_current_time(get_request_timezone())
            return '', HTTPStatus.NO_CONTENT
        else:
            raise SkillFoundError(ErrorMessages.NoSkillsFound, ErrorCodes.NoSkillsFound,
                                  http_status_code=HTTPStatus.NOT_FOUND)


@app.route('/skills/<string:slug>', methods=['DELETE'])
@dispatch()
def delete_skill(slug: str):
    with SkillRepository() as repo:
        skill: Skill = repo.filter_one(Skill.slug == slug)
        if skill:
            skill.is_active = False
            return '', HTTPStatus.NO_CONTENT
        else:
            raise SkillFoundError(ErrorMessages.NoSkillsFound, ErrorCodes.NoSkillsFound,
                                  http_status_code=HTTPStatus.NOT_FOUND)
