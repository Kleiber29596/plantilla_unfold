from ninja_jwt.schema       import TokenObtainPairInputSchema
from ninja_jwt.controller   import TokenObtainPairController
from ninja_extra            import api_controller, route
from ninja                  import Schema


class UserSchema(Schema):
    first_name: str
    email: str


class MyTokenObtainPairOutSchema(Schema):
    refresh: str
    access: str
    user: UserSchema


class MyTokenObtainPairSchema(TokenObtainPairInputSchema):
    def output_schema(self):
        out_dict = self.get_response_schema_init_kwargs()
        out_dict.update(user=UserSchema.from_orm(self._user))
        return MyTokenObtainPairOutSchema(**out_dict)


@api_controller('/token', tags=['Auth'])
class MyTokenObtainPairController(TokenObtainPairController):
    @route.post("/pair", response=MyTokenObtainPairOutSchema, url_name="token_obtain_pair")
    def obtain_token(self, user_token: MyTokenObtainPairSchema):
        return user_token.output_schema()