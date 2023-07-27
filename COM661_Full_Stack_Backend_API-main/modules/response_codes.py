response_codes = {
    'No Keyword' : {
        'Status Code' : 204,
        'Message' : 'No Keywords Found.'
    },
    'No Review' : {
        'Status Code' : 204,
        'Message' : 'No Reviews Found For User.'
    },
    'No Results' : {
        'Status Code' : 204,
        'Message' : 'No Results Found.'
    },
    'Server Online' : {
        'Status Code' : 200,
        'Message' : 'Server Online'
    },
    'Server Down' : {
        'Status Code' : 503,
        'Message' : 'Database Server Not Available'
    },
    'Invalid Operator' : {
        'Status Code' : 400,
        'Message' : 'Bad Request',
        'Error' : 'Invalid Operator.'
    },
    'Bad Password' : {
        'Status Code' : 401,
        'Message' : 'Invalid Password'
    },
    'Bad Username' : {
        'Status Code' : 401,
        'Message' : 'Invalid Username'
    },
    'Auth Required' : {
        'Status Code' : 401,
        'Message' : 'Authentication Required'
    },
    'Invalid Title' : {
        'Status Code' : 404,
        'Invalid Title' : 'Try another title',
        'Message' : 'Movie has not been found.'
    },
    'No Update' : {
        'Status Code' : 404,
        'Message' : 'Could not update movie'
    },
    'Review Already Exists' : {
        'Status Code' : 403,
        'Message' : 'Conflic',
        'Error' : 'Review already exists for user'
    },
    'Invalid Date Format' : {
        'Status Code' : 422,
        'Message' : 'Date is not formated correctly',
        'Error' : 'Should be YYYY-MM-DD'
    },
    'Review Deleted' : {
        'Status Code' : 201,
        'Message' : 'Review has been deleted.'
    },
    'Movie Deleted' : {
        'Status Code' : 201,
        'Message' : 'Movie has been deleted.'
    }
}

class CustomCodes():

    def __init__(self) -> None:
        self.response_codes = response_codes
        self.response_codes_custom = {
            'Valid Token' : {
                'Status Code' : 200,
                'Token' : 'placeholder'
            },
            'Result Url' : {
                'Status Code' : 201,
                'URL' : 'placeholder'
            },
            'Result Poster' : {
                'Status Code' : 200,
                'URL' : 'placeholder'
            },
            'Result' : {
                'Status Code' : 200,
                'Result' : 'placeholder'
            },
            'Invalid Operator' : {
                'Status Code' : 400,
                'Message' : 'Invalid operator value',
                'Valid Operators' : 'placeholder'
            },
            'Invalid User' : {
                'Status Code' : 404,
                'User' : 'placeholder',
                'Title' : 'placeholder',
                'Message' : 'No reviews have been found.'
            },
            'Unprocessable Entity' : {
                'Status Code' : 422,
                'Message' : 'Make sure that the data sent in the request is accurate.',
                'Missing Fields' : 'Placeholder',
            }
        }

    def valid_token(self, token, admin, user_id):
        self.response_codes_custom['Valid Token']['Token'] = token
        self.response_codes_custom['Valid Token']['Admin'] = admin
        self.response_codes_custom['Valid Token']['User ID'] = user_id
        return self.response_codes_custom['Valid Token']

    def result_url(self, results, message=""):
        self.response_codes_custom['Result Url']['URL'] = results
        self.response_codes_custom['Result Url']['Message'] = message
        return self.response_codes_custom['Result Url']

    def result_poster(self, results):
        self.response_codes_custom['Result Poster']['URL'] = results
        return self.response_codes_custom['Result Poster']

    def result(self, results):
        self.response_codes_custom['Result']['Result'] = results
        return self.response_codes_custom['Result']

    def invalid_op(self, valid_op):
        self.response_codes_custom['Invalid Operator']['Valid Operators'] = valid_op

        return self.response_codes_custom['Invalid Operator']

    def invalid_user(self, user_id, title):
        self.response_codes_custom['Invalid User']['User'] = user_id
        self.response_codes_custom['Invalid User']['Title'] = title

        return self.response_codes_custom['Invalid User']

    def invalid_entity(self, missing_fields):
        self.response_codes_custom['Unprocessable Entity']['Missing Fields'] = missing_fields

        return self.response_codes_custom['Unprocessable Entity']