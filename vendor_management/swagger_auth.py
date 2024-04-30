from drf_yasg.inspectors import SwaggerAutoSchema

class SwaggerAutoSchemaWithJWT(SwaggerAutoSchema):
    def get_security_definitions(self, security_requirements):
        security_definitions = super().get_security_definitions(security_requirements)
        security_definitions['Bearer'] = {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Enter the token in the format: Bearer &lt;token&gt;',
            'prefix': 'Bearer',
        }
        return security_definitions

    def get_security_requirements(self, security_requirements):
        security_requirements = super().get_security_requirements(security_requirements)
        security_requirements.append({'Bearer': []})
        return security_requirements