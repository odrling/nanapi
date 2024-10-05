import asyncio
import logging
from itertools import batched

from nanapi.database.anilist.chara_select_all_ids import chara_select_all_ids
from nanapi.database.anilist.media_select_all_ids import media_select_all_ids
from nanapi.database.anilist.staff_select_all_ids import staff_select_all_ids
from nanapi.database.anilist.tag_merge_multiple import tag_merge_multiple
from nanapi.settings import LOG_LEVEL
from nanapi.tasks.userlists import refresh_lists, refresh_multitons
from nanapi.utils.anilist import Chara, Media, Staff, get_tags
from nanapi.utils.clients import get_edgedb
from nanapi.utils.logs import webhook_exceptions

logger = logging.getLogger(__name__)


@webhook_exceptions
async def refresh_tags():
    tags = await get_tags(al_low_priority=True)
    await tag_merge_multiple(get_edgedb(),
                             tags=[tag.to_edgedb() for tag in tags])


@webhook_exceptions
async def refresh_medias():
    in_db = await media_select_all_ids(get_edgedb())
    ids_al_in_db = set(m.id_al for m in in_db)
    orphan_ids = ids_al_in_db - set(refresh_multitons.medias.keys())

    orphan_medias = set(Media.get(refresh_multitons, id) for id in orphan_ids)

    if len(orphan_medias) == 0:
        return

    parts = list(batched(orphan_medias, 50))
    logger.info(
        f"refresh_medias: fetching page 1 for {len(orphan_medias)} orphans medias "
        f"in {len(parts)} requests")
    tasks = (Media.fetch_page(set(p), 1, low_priority=True) for p in parts)
    await asyncio.gather(*tasks)
    logger.info(
        f"refresh_medias: page 1 fetched for {len(orphan_medias)} orphans medias"
    )

    await refresh_multitons.edgedb_merge_medias(get_edgedb(), full=True)
    refresh_multitons.medias.clear()


@webhook_exceptions
async def refresh_charas():
    in_db = await chara_select_all_ids(get_edgedb())
    ids_al_in_db = set(c.id_al for c in in_db)
    orphan_ids = ids_al_in_db - set(refresh_multitons.charas.keys())

    charas = set(refresh_multitons.charas.values())
    charas.update(Chara.get(refresh_multitons, id) for id in orphan_ids)

    await refresh_multitons.edgedb_merge_charas(get_edgedb(), full=True)
    refresh_multitons.charas.clear()


@webhook_exceptions
async def refresh_staffs():
    in_db = await staff_select_all_ids(get_edgedb())
    ids_al_in_db = set(s.id_al for s in in_db)
    orphan_ids = ids_al_in_db - set(refresh_multitons.staffs.keys())

    staffs = set(refresh_multitons.staffs.values())
    staffs.update(Staff.get(refresh_multitons, id) for id in orphan_ids)

    await refresh_multitons.edgedb_merge_staffs(get_edgedb(), full=True)
    refresh_multitons.staffs.clear()


async def main():
    logger.info("refreshing tags")
    await refresh_tags()
    logger.info("refreshing lists")
    await refresh_lists()
    logger.info("refreshing medias")
    await refresh_medias()
    logger.info("refreshing charas")
    await refresh_charas()
    logger.info("refreshing staffs")
    await refresh_staffs()


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL)
    asyncio.run(main())
