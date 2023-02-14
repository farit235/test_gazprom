from flask import Blueprint
import utils

wiki_blueprint = Blueprint("wiki_blueprint", __name__, template_folder="templates")


@wiki_blueprint.route("/<title>")
def search_title(title):
    """Вьющка на поиск по названию через get запрос"""
    return utils.find_data_by_name(title)