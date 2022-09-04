import asyncio
import logging

from nanapi.database.anilist.account_replace_entries import account_replace_entries
from nanapi.database.anilist.account_select_all import account_select_all
from nanapi.database.anilist.media_select_all_ids import media_select_all_ids
from nanapi.models.anilist import ALMedia, AnilistService, MediaType
from nanapi.settings import LOG_LEVEL
from nanapi.utils.anilist import (
    SERVICE_USER_LIST,
    ALMultitons,
    Media,
    Userlist,
    malmapper,
    merge_lock,
)
from nanapi.utils.clients import get_edgedb
from nanapi.utils.logs import webhook_exceptions

logger = logging.getLogger(__name__)
refresh_multitons = ALMultitons(name='refresh_multitons')


@webhook_exceptions
async def refresh_lists():
    async with merge_lock:
        refresh_multitons.clear_all()

        logger.info('refresh_lists: reloading MALMapper')
        media_ids = await media_select_all_ids(get_edgedb())
        malmapper.load(list(media_ids))

        anilists = await account_select_all(get_edgedb())
        almedias: set[ALMedia] = set()
        logger.info(f"refresh_lists: refreshing {len(anilists)} users")

        for al in anilists:
            service = AnilistService(al.service)
            userlist = SERVICE_USER_LIST[service](al.username)
            for media_type in MediaType:
                try:
                    user_almedias = await refresh_list(userlist, media_type)
                    almedias.update(user_almedias)
                except Exception as e:
                    logger.exception(e)

        logger.info(
            f"refresh_lists: fetched page 1 for {len(almedias)} medias in total"
        )

        medias = []
        for almedia in almedias:
            media = Media.get(refresh_multitons, almedia.id)
            media.feed_page(almedia)
            medias.append(media)


async def refresh_list(userlist: Userlist, media_type: MediaType):
    logger_list = f"{userlist.service}/{userlist.username}/{media_type}"
    logger.info(f"refresh_list: fetching {logger_list}")
    entries, user_almedias = await userlist.refresh(media_type,
                                                    al_low_priority=True)
    logger.info(f"refresh_list: {logger_list} fetched "
                f"with {len(entries)} entries and {len(user_almedias)} medias")
    if len(entries) > 0:
        edgedb_data = userlist.to_edgedb(media_type, entries, user_almedias)
        await account_replace_entries(get_edgedb(), **edgedb_data)
    return user_almedias


async def main():
    await refresh_lists()


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL)
    asyncio.run(main())
