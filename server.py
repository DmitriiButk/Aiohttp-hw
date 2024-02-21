from aiohttp import web
from models import Session, Announcement, engine, init_orm
import json
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from schema import CreateAnnouncement, UpdateAnnouncement


app = web.Application()


@web.middleware
async def session_middleware(request, handler):
    """The function adds a session object to the request object."""
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


async def orm_context(app):
    """The function initialize the SQLAlchemy ORM and yield the session object."""
    await init_orm()
    yield
    await engine.dispose()


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_error(error_class, message):
    """The function receives the error class and message."""
    return error_class(text=json.dumps(
        {'error': message}), content_type='application/json')


async def validate_json(schema_class, json_data):
    """The function checks json data."""
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as er:
        error = er.errors()[0]
        error.pop('ctx', None)
        raise get_error(web.HTTPBadRequest, error)


async def get_ann_by_id(session, ann_id: int):
    """The function get an announcement by its ID."""
    announcement = await session.get(Announcement, ann_id)
    if announcement is None:
        raise get_error(web.HTTPNotFound, message=f'Announcement with id {ann_id} not found')
    return announcement


async def add_announcement(session, announcement: Announcement):
    """The function adds a new announcement to the database."""
    try:
        session.add(announcement)
        await session.commit()
    except IntegrityError:
        raise get_error(web.HTTPConflict, message="Announcement already exists")


class AnnouncementView(web.View):
    """
    The AnnouncementView class provides the HTTP handlers for the /announcements/{ann_id} route.
    """

    @property
    def ann_id(self):
        """The ann_id property returns the announcement ID from the request URL."""
        return int(self.request.match_info['ann_id'])

    @property
    def session(self) -> Session:
        """The session property returns the SQLAlchemy session object."""
        return self.request.session

    async def get_announcement(self):
        """The method retrieves an announcement by its ID."""
        announcement = await get_ann_by_id(self.session, self.ann_id)
        return announcement

    async def get(self):
        """The method returns information about the announcement."""
        announcement = await self.get_announcement()
        return web.json_response(announcement.dict)

    async def post(self):
        """The method creates a new announcement."""
        json_data = await validate_json(CreateAnnouncement, await self.request.json())
        announcement = Announcement(**json_data)
        await add_announcement(self.session, announcement)
        return web.json_response({'id': announcement.id})

    async def patch(self):
        """The method updates an announcement."""
        json_data = await validate_json(UpdateAnnouncement, await self.request.json())
        announcement = await self.get_announcement()
        for field, value in json_data.items():
            setattr(announcement, field, value)
        await add_announcement(self.session, announcement)
        return web.json_response({'id': announcement.id})

    async def delete(self):
        """The method deletes an announcement."""
        announcement = await self.get_announcement()
        await self.session.delete(announcement)
        await self.session.commit()
        return web.json_response({'status': 'Deleted'})


url_app = '/announcements/{ann_id:\d+}/'

app.add_routes(
    [
        web.get(url_app, AnnouncementView),
        web.patch(url_app, AnnouncementView),
        web.delete(url_app, AnnouncementView),
        web.post('/announcements/', AnnouncementView)
    ]
)

if __name__ == '__main__':
    web.run_app(app)
