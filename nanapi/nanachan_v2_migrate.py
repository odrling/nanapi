#!/usr/bin/env python3

import asyncio
import base64
import logging
import sqlite3
from argparse import ArgumentParser
from datetime import datetime
from typing import cast

import edgedb
import orjson

from nanapi.database.amq.account_merge import \
    account_merge as amq_account_merge
from nanapi.database.amq.settings_merge import settings_merge
from nanapi.database.anilist.account_merge import \
    account_merge as al_account_merge
from nanapi.database.anilist.chara_select_all_ids import chara_select_all_ids
from nanapi.database.anilist.media_select_all_ids import media_select_all_ids
from nanapi.database.histoire.histoire_insert import histoire_insert
from nanapi.database.poll.poll_insert import poll_insert
from nanapi.database.poll.vote_merge import vote_merge
from nanapi.database.presence.presence_insert import presence_insert
from nanapi.database.projection.projo_add_event import projo_add_event
from nanapi.database.projection.projo_add_external_media import \
    projo_add_external_media
from nanapi.database.projection.projo_add_media import projo_add_media
from nanapi.database.reminder.reminder_insert_select import \
    reminder_insert_select
from nanapi.database.role.role_insert_select import role_insert_select
from nanapi.database.user.profile_merge_select import profile_merge_select
from nanapi.database.waicolle.collection_add_media import collection_add_media
from nanapi.database.waicolle.collection_insert import collection_insert
from nanapi.database.waicolle.player_add_collection import \
    player_add_collection
from nanapi.database.waicolle.player_add_media import player_add_media
from nanapi.database.waicolle.waifu_replace_custom_position import \
    waifu_replace_custom_position
from nanapi.settings import INSTANCE_NAME, TZ
from nanapi.utils.anilist import ALMultitons, Chara, Media
from nanapi.utils.clients import _get_edgedb, get_meilisearch

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def migrate_amq(cur: sqlite3.Cursor, executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate amq')
    for row in cur.execute('select * from amq_a_m_q_players').fetchall():
        discord_id, username = row
        await amq_account_merge(executor=executor,
                                discord_id=discord_id,
                                discord_username=str(discord_id),
                                username=username)
    _, _, settings_str = cur.execute('select * from amq_data').fetchone()
    settings = orjson.loads(settings_str)
    await settings_merge(executor=executor, settings=settings)


async def migrate_anilist(cur: sqlite3.Cursor,
                          executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate anilist')
    SERVICE_MAP = {
        'al': 'ANILIST',
        'mal': 'MYANIMELIST',
    }
    for row in cur.execute('select * from anilists_anilist').fetchall():
        discord_id, service_slug, username = row
        await al_account_merge(
            executor,
            discord_id=discord_id,
            service=SERVICE_MAP[service_slug],  # type: ignore
            username=username)


async def migrate_histoire(cur: sqlite3.Cursor,
                           executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate histoire')
    for row in cur.execute('select * from histoire_story_model').fetchall():
        _, title, text, _ = row
        await histoire_insert(executor, title=title, text=text)


async def migrate_poll(cur: sqlite3.Cursor, executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate poll')
    for poll_row in cur.execute('select * from polls_poll').fetchall():
        poll_id, message_id, channel_id, question = poll_row
        options = cur.execute('select * from polls_option where poll_id = ?',
                              (poll_id,)).fetchall()
        await poll_insert(
            executor,
            message_id=message_id,
            channel_id=channel_id,
            question=question,
            options=[
                dict(rank=rank, text=text) for _, _, rank, text in options
            ])
        options_map = {option_id: rank for option_id, _, rank, _ in options}
        for vote_row in cur.execute(
                'select * from polls_vote where poll_id = ?',
            (poll_id,)).fetchall():  # noqa
            _, discord_id, option_id, _ = vote_row
            await vote_merge(executor,
                             discord_id=discord_id,
                             discord_username=str(discord_id),
                             message_id=message_id,
                             rank=options_map[option_id])


async def migrate_pot(cur: sqlite3.Cursor, executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate pot')
    QUERY = r"""
    with
        discord_id := <int64>$discord_id,
        discord_username := <str>$discord_username,
        amount := <float32>$amount,
        count := <int32>$count,
        user := (
            insert user::User {
                discord_id := discord_id,
                discord_username := discord_username,
            }
            unless conflict on .discord_id
            else (select user::User)
        ),
    insert pot::Pot {
        client := global client,
        amount := amount,
        count := count,
        user := user,
    }
    unless conflict on ((.client, .user))
    else (
        update pot::Pot set {
            amount := amount,
            count := count,
        }
    )
    """
    for row in cur.execute('select * from pot_pot_model').fetchall():
        _, discord_id, amount, count = row
        await executor.execute(QUERY,
                               discord_id=discord_id,
                               discord_username=str(discord_id),
                               amount=amount,
                               count=count)


async def migrate_presence(cur: sqlite3.Cursor,
                           executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate presence')
    TYPE_MAP = {
        'playing': 'PLAYING',
        'listening': 'LISTENING',
        'watching': 'WATCHING',
    }
    for row in cur.execute('select * from presence_presence_model').fetchall():
        _, type_str, name = row
        await presence_insert(
            executor,
            type=TYPE_MAP[type_str],  # type: ignore
            name=name)


async def migrate_projection(cur: sqlite3.Cursor,
                             executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate projection')
    PROJECTION_QUERY = r"""
    with
        name := <str>$name,
        status := <projection::Status>$status,
        channel_id := <optional int64>$channel_id,
        message_id := <optional int64>$message_id,
    insert projection::Projection {
        client := global client,
        name := name,
        status := status,
        channel_id := channel_id ?? 0,
        message_id := message_id,
    }
    """
    medias_in_db = await media_select_all_ids(executor)
    medias_ids_in_db = set(m.id_al for m in medias_in_db)
    all_al_medias = cur.execute(
        'select * from projection_anime where anime_id > 0').fetchall()
    all_al_ids = {anime_id for anime_id, _ in all_al_medias}
    multitons = ALMultitons()
    async for m in Media.load({
            Media.get(multitons, id_al)
            for id_al in all_al_ids
            if id_al not in medias_ids_in_db
    }):
        await m.edgedb_merge(executor)
    for projo_row in cur.execute(
            'select * from projection_projection').fetchall():
        old_projo_id, status_str, name, message_id, channel_id, _ = projo_row
        status = 'ONGOING' if status_str == 'SELECTED' else 'COMPLETED'
        projo = await executor.query_required_single(PROJECTION_QUERY,
                                                     name=name,
                                                     status=status,
                                                     channel_id=channel_id,
                                                     message_id=message_id)
        medias = cur.execute(
            'select * from projection_projected_anime where projection_id = ?',
            (old_projo_id,)).fetchall()
        al_ids = (anime_id for _, anime_id, _ in medias if anime_id > 0)
        for al_id in al_ids:
            await projo_add_media(executor, id=projo.id, id_al=al_id)
        external_ids = (anime_id for _, anime_id, _ in medias if anime_id < 0)
        for external_id in external_ids:
            _, title = cur.execute(
                'select * from projection_anime where anime_id = ?',
                (external_id,)).fetchone()
            await projo_add_external_media(executor, id=projo.id, title=title)
        for row in cur.execute(
                'select * from projection_event where projection_id = ?',
            (old_projo_id,)).fetchall():  # noqa
            _, date_str, _, description = row
            date = datetime.fromisoformat(date_str)
            date = date.replace(tzinfo=TZ)
            await projo_add_event(executor,
                                  id=projo.id,
                                  date=date,
                                  description=description)


async def migrate_quizz(cur: sqlite3.Cursor, executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate quizz')
    QUIZZ_QUERY = r"""
    with
        channel_id := <int64>$channel_id,
        description := <optional str>$description,
        url := <optional str>$url,
        is_image := <bool>$is_image,
        author_discord_id := <int64>$author_discord_id,
        author_discord_username := <str>$author_discord_username,
        author := (
            insert user::User {
                discord_id := author_discord_id,
                discord_username := author_discord_username,
            }
            unless conflict on .discord_id
            else (select user::User)
        ),
        answer := <optional str>$answer,
        answer_source := <optional str>$answer_source,
        submitted_at := <optional datetime>$submitted_at,
    insert quizz::Quizz {
        client := global client,
        channel_id := channel_id,
        description := description,
        url := url,
        is_image := is_image,
        author := author,
        answer := answer,
        answer_source := answer_source,
        submitted_at := submitted_at ?? datetime_of_statement(),
    }
    """
    CURRENT_GAME_QUERY = r"""
    with
        message_id := <int64>$message_id,
        answer_bananed := <optional str>$answer_bananed,
        quizz_id := <uuid>$quizz_id,
        quizz := (select quizz::Quizz filter .id = quizz_id),
        started_at := <optional datetime>$started_at,
    insert quizz::Game {
        client := global client,
        message_id := message_id,
        answer_bananed := answer_bananed,
        quizz := quizz,
        started_at := started_at ?? datetime_of_statement(),
    }
    """
    ENDED_GAME_QUERY = r"""
    with
        message_id := <int64>$message_id,
        answer_bananed := <optional str>$answer_bananed,
        quizz_id := <uuid>$quizz_id,
        quizz := (select quizz::Quizz filter .id = quizz_id),
        started_at := <optional datetime>$started_at,
        ended_at := <optional datetime>$ended_at,
        winner_discord_id := <int64>$winner_discord_id,
        winner_discord_username := <str>$winner_discord_username,
        winner := (
            insert user::User {
                discord_id := winner_discord_id,
                discord_username := winner_discord_username,
            }
            unless conflict on .discord_id
            else (select user::User)
        ),
    insert quizz::Game {
        client := global client,
        message_id := message_id,
        answer_bananed := answer_bananed,
        quizz := quizz,
        started_at := started_at ?? datetime_of_statement(),
        status := quizz::Status.ENDED,
        ended_at := ended_at ?? datetime_of_statement(),
        winner := winner,
    }
    """
    for quizz_row in cur.execute('select * from quizz_stock').fetchall():
        (_, _, status, author_id, url, is_image, description, answer,
         answer_bananed, answer_source, channel_id, message_id, winner_id,
         created_at_str, ended_at_str) = quizz_row
        created_at = None
        if created_at_str:
            created_at = datetime.fromisoformat(created_at_str)
            created_at = created_at.replace(tzinfo=TZ)
        quizz = await executor.query_required_single(
            QUIZZ_QUERY,
            channel_id=channel_id,
            description=description,
            is_image=bool(is_image),
            author_discord_id=author_id,
            author_discord_username=str(author_id),
            url=url,
            answer=answer,
            answer_source=answer_source,
            submitted_at=created_at)
        if status == 0:
            continue
        elif status == 1:
            await executor.execute(CURRENT_GAME_QUERY,
                                   message_id=message_id,
                                   answer_bananed=answer_bananed,
                                   quizz_id=quizz.id,
                                   started_at=created_at)
        elif status == 2:
            ended_at = None
            if ended_at_str:
                ended_at = datetime.fromisoformat(ended_at_str)
                ended_at = ended_at.replace(tzinfo=TZ)
            await executor.execute(ENDED_GAME_QUERY,
                                   message_id=message_id,
                                   answer_bananed=answer_bananed,
                                   quizz_id=quizz.id,
                                   started_at=created_at,
                                   ended_at=ended_at,
                                   winner_discord_id=winner_id,
                                   winner_discord_username=str(winner_id))
        else:
            raise ValueError(status)


async def migrate_reminder(cur: sqlite3.Cursor,
                           executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate reminder')
    for row in cur.execute('select * from remindme_reminder').fetchall():
        _, discord_id, channel_id, unix_timestamp, message = row
        timestamp = datetime.fromtimestamp(unix_timestamp, tz=TZ)
        await reminder_insert_select(executor,
                                     discord_id=discord_id,
                                     discord_username=str(discord_id),
                                     channel_id=channel_id,
                                     message=message,
                                     timestamp=timestamp)


async def migrate_role(cur: sqlite3.Cursor, executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate role')
    for row in cur.execute(
            'select * from roles_auto_assignable_roles').fetchall():
        role_id, emoji = row
        await role_insert_select(executor, role_id=role_id, emoji=emoji)


async def migrate_user(cur: sqlite3.Cursor, executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate user')
    for row in cur.execute('select * from profiles_profile').fetchall():
        _, discord_id, full_name, photo, promotion, telephone = row
        await profile_merge_select(executor,
                                   discord_id=discord_id,
                                   discord_username=str(discord_id),
                                   full_name=full_name,
                                   photo=photo,
                                   promotion=promotion,
                                   telephone=telephone)


async def migrate_waicolle(cur: sqlite3.Cursor,
                           executor: edgedb.AsyncIOExecutor):
    logger.info('Migrate waicolle')
    PLAYER_QUERY = r"""
    with
        discord_id := <int64>$discord_id,
        discord_username := <str>$discord_username,
        game_mode := <waicolle::GameMode>$game_mode,
        moecoins := <int32>$moecoins,
        blood_shards := <int32>$blood_shards,
        user := (
            insert user::User {
                discord_id := discord_id,
                discord_username := discord_username,
            }
            unless conflict on .discord_id
            else (select user::User)
        ),
    insert waicolle::Player {
        client := global client,
        game_mode := game_mode,
        user := user,
        moecoins := moecoins,
        blood_shards := blood_shards,
    }
    unless conflict on ((.client, .user))
    else (
        update waicolle::Player set {
            game_mode := game_mode,
            moecoins := moecoins,
            blood_shards := blood_shards,
        }
    )
    """
    WAIFU_QUERY = r"""
    with
        timestamp := <datetime>$timestamp,
        level := <int32>$level,
        locked := <bool>$locked,
        blooded := <bool>$blooded,
        nanaed := <bool>$nanaed,
        custom_image := <optional str>$custom_image,
        custom_name := <optional str>$custom_name,
        character_id_al := <int32>$character_id_al,
        owner_id := <int64>$owner_id,
        original_owner_id := <int64>$original_owner_id,
        custom_collage := <bool>$custom_collage,
    insert waicolle::Waifu {
        client := global client,
        timestamp := timestamp,
        level := level,
        locked := locked,
        blooded := blooded,
        nanaed := nanaed,
        custom_image := custom_image,
        custom_name := custom_name,
        character := (select anilist::Character filter .id_al = character_id_al),
        owner := (select waicolle::Player filter .user.discord_id = owner_id and .client = global client),  # noqa
        original_owner := (select waicolle::Player
            filter .user.discord_id = original_owner_id and .client = global client),
        custom_collage := custom_collage,
    }
    """
    media_ids = set()

    all_tracks = cur.execute('select * from waifu_w_c_tracker').fetchall()
    media_ids.update(media_id for _, media_id in all_tracks)

    all_collection_medias = cur.execute(
        'select * from waifu_w_c_tracker_collection_media').fetchall()
    media_ids.update(media_id for _, _, media_id in all_collection_medias)

    medias_in_db = await media_select_all_ids(executor)
    medias_ids_in_db = set(m.id_al for m in medias_in_db)

    multitons = ALMultitons()
    async for c in Media.load({
            Media.get(multitons, id_al)
            for id_al in media_ids
            if id_al not in medias_ids_in_db
    }):
        await c.edgedb_merge(executor)

    all_waifus = cur.execute('select * from waifu_w_c_waifu').fetchall()
    chara_ids = {w[1] for w in all_waifus}

    charas_in_db = await chara_select_all_ids(executor)
    charas_ids_in_db = set(m.id_al for m in charas_in_db)

    multitons = ALMultitons()
    async for c in Chara.load({
            Chara.get(multitons, id_al)
            for id_al in chara_ids
            if id_al not in charas_ids_in_db
    }):
        await c.edgedb_merge(executor)

    for player_row in cur.execute('select * from waifu_w_c_player').fetchall():
        user_id, game_mode, moecoins, blood_shards, _ = player_row
        await executor.execute(PLAYER_QUERY,
                               discord_id=user_id,
                               discord_username=str(user_id),
                               game_mode=game_mode,
                               moecoins=moecoins,
                               blood_shards=blood_shards)

        tracked_medias = [
            media_id for player_id, media_id in all_tracks
            if player_id == user_id
        ]
        for media_id in tracked_medias:
            await player_add_media(executor, discord_id=user_id, id_al=media_id)

        for row in cur.execute(
                'select * from waifu_w_c_tracker_collection where player_id = ?',
            (user_id,)).fetchall():  # noqa
            collection_id, _, name = row
            collection = await collection_insert(executor,
                                                 discord_id=user_id,
                                                 name=name)
            medias_ids = [
                media_id
                for _, _collection_id, media_id in all_collection_medias
                if _collection_id == collection_id
            ]
            for media_id in medias_ids:
                await collection_add_media(executor,
                                           id=collection.id,
                                           id_al=media_id)
            async with get_meilisearch() as client:
                index = client.index(
                    f"{INSTANCE_NAME}_collections_{args.client_id}")
                doc = dict(id=str(collection.id),
                           name=collection.name,
                           author_discord_id=collection.author.user.discord_id)
                await index.add_documents([doc], primary_key="id")
            await player_add_collection(executor,
                                        discord_id=user_id,
                                        id=collection.id)

    waifu_map = dict()
    CUSTOM_POSITIONS = {
        'Default': 'DEFAULT',
        'Left of': 'LEFT_OF',
        'Right of': 'RIGHT_OF',
    }
    with_custom_pos = []
    for i, waifu_row in enumerate(all_waifus):
        logger.info(f"waifu: {i}/{len(all_waifus)}")
        (old_id, chara_id, owner_id, original_owner_id, timestamp_str, level,
         locked, blooded, nanaed, custom_image, custom_name,
         custom_position_str, custom_position_waifu_id,
         custom_collage) = waifu_row
        timestamp = datetime.fromisoformat(timestamp_str)
        timestamp = timestamp.replace(tzinfo=TZ)
        resp = await executor.query_required_single(
            WAIFU_QUERY,
            timestamp=timestamp,
            level=level,
            locked=bool(locked),
            blooded=bool(blooded),
            nanaed=bool(nanaed),
            custom_image=(base64.b64encode(custom_image).decode()
                          if custom_image else None),
            custom_name=custom_name,
            character_id_al=chara_id,
            owner_id=owner_id,
            original_owner_id=original_owner_id,
            custom_collage=bool(custom_collage))
        waifu_map[old_id] = resp.id
        if custom_position_str != 'Default':
            with_custom_pos.append(
                (resp.id, CUSTOM_POSITIONS[custom_position_str],
                 custom_position_waifu_id))

    for waifu_id, custom_pos, other_old_id in with_custom_pos:
        other_id = waifu_map[other_old_id]
        await waifu_replace_custom_position(executor,
                                            id=waifu_id,
                                            custom_position=custom_pos,
                                            other_waifu_id=other_id)


async def main(con: sqlite3.Connection):
    logger.info('Starting migration')
    cur = con.cursor()
    client = cast(edgedb.AsyncIOClient,
                  _get_edgedb().with_globals({'client_id': args.client_id}))
    async for tx in client.transaction():
        async with tx:
            await migrate_amq(cur, tx)
            await migrate_anilist(cur, tx)
            await migrate_histoire(cur, tx)
            await migrate_poll(cur, tx)
            await migrate_pot(cur, tx)
            await migrate_presence(cur, tx)
            await migrate_projection(cur, tx)
            await migrate_quizz(cur, tx)
            await migrate_reminder(cur, tx)
            await migrate_role(cur, tx)
            await migrate_user(cur, tx)
            await migrate_waicolle(cur, tx)
    logger.info('All good :FubukiGO:')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('db_path')
    parser.add_argument('client_id')
    args = parser.parse_args()
    con = sqlite3.connect(args.db_path)
    try:
        asyncio.run(main(con))
    finally:
        con.close()
