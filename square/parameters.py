from drf_yasg import openapi

square_type_param = openapi.Parameter('square_type',
                                      openapi.IN_QUERY,
                                      description='The Square Type that is going to be in this position',
                                      type=openapi.TYPE_STRING,
                                      required=True)
