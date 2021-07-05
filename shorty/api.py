from flask_restful import Resource, abort
from flask import request
from shorty.utils import get_short_link
from shorty.validators import ShortifyRequest
from pydantic import ValidationError
from flasgger import swag_from


class ShortifyView(Resource):

    @swag_from('swagger_config/shortify_specs.yml')
    def post(self):
        """
        Gets the link from request and returns its abbreviated version
        :return:
        """

        try:
            text = request.data
            # creating full request object
            data = ShortifyRequest.parse_raw(text)
        except ValidationError as e:
            abort(400, error='Wrong data', error_list=e.json())

        # calculating short_link and error handler
        short_link, error = get_short_link(
            data.url,
            data.provider
        )
        # try to escape error
        loop_counter = 0

        # while error handler is setted we trying to find short url
        while error:
            # but if loop_counter is bigger than 2 the loop is breaking
            if loop_counter >= 3:
                break
            # resolving new data
            short_link, error = get_short_link(
                data.url,
                data.provider
            )
            # increase counter
            loop_counter += 1

        if not error:
            # if there is no error return values
            response_data = dict(
                url=data.url,
                link=short_link
            )
            return response_data
        else:
            # aborting if couldn't get short url
            return abort(502, error='Error with processing url')
