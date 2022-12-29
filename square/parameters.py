from drf_yasg import openapi

square_type_param = openapi.Parameter('square_type',
                                      openapi.IN_QUERY,
                                      description='The square type that is going to be in this position',
                                      type=openapi.TYPE_STRING,
                                      required=True)

destination_param = openapi.Parameter('destination',
                                      openapi.IN_QUERY,
                                      description='The destination of your move',
                                      type=openapi.TYPE_INTEGER,
                                      required=True)