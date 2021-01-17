from aiohttp import web
from context import ViewWithContext
from modules import Users, UserModel
import json


class AccountView(web.View, ViewWithContext):
    async def get(self):
        """
        ---
        description: Gets current user if authorized
        tags:
          - Auth
        produces:
         - application/json
        responses:
          "200":
            description: Successful operation. Return user json object
          "401":
            description: Unauthorized access error. Returns error object
          "500":
            description: Unexpected server error. Returns error object
        """
        print(await Users.user_by_id(self.ctx(), 1))
        return web.Response(text=json.dumps({"name": 'lol'}), content_type="application/json")

    async def post(self):
        """
        ---
        description: Creates user
        tags:
          - Auth
        produces:
          - application/json
        parameters:
        - in: body
          name: body
          description: User object
          required: true
          schema:
            type: object
            properties:
              email:
                type: string
              password:
                type: string
              name:
                type: string
        responses:
          "200":
            description: Successful operation. Return user json object
          "401":
            description: Unauthorized access error. Returns error object
          "500":
            description: Unexpected server error. Returns error object
        """

        inp = await self.request.json()
        await Users.create_user(self.ctx(), UserModel(**inp))
        return web.Response(text=json.dumps({"name": "kek"}), content_type="application/json")
