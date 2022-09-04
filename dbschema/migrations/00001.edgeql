CREATE MIGRATION m1mgsapt43fibeutomf7j46escoh7vhehqr5syav5g5l4iutilnuqq
    ONTO initial
{
  CREATE MODULE amq IF NOT EXISTS;
  CREATE MODULE anilist IF NOT EXISTS;
  CREATE MODULE histoire IF NOT EXISTS;
  CREATE MODULE poll IF NOT EXISTS;
  CREATE MODULE pot IF NOT EXISTS;
  CREATE MODULE presence IF NOT EXISTS;
  CREATE MODULE projection IF NOT EXISTS;
  CREATE MODULE quizz IF NOT EXISTS;
  CREATE MODULE reminder IF NOT EXISTS;
  CREATE MODULE role IF NOT EXISTS;
  CREATE MODULE user IF NOT EXISTS;
  CREATE MODULE waicolle IF NOT EXISTS;
  CREATE GLOBAL default::client_id -> std::uuid;
  CREATE TYPE default::Client {
      CREATE REQUIRED PROPERTY name -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE ABSTRACT TYPE default::ClientObject {
      CREATE REQUIRED LINK client -> default::Client;
      CREATE ACCESS POLICY client_access
          ALLOW ALL USING ((GLOBAL default::client_id ?= .client.id));
  };
  CREATE TYPE amq::Setting EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY key -> std::str;
      CREATE CONSTRAINT std::exclusive ON ((.client, .key));
      CREATE REQUIRED PROPERTY value -> std::str;
  };
  CREATE TYPE histoire::Histoire EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY title -> std::str;
      CREATE CONSTRAINT std::exclusive ON ((.client, .title));
      CREATE REQUIRED PROPERTY formatted -> std::bool {
          SET default := true;
      };
      CREATE REQUIRED PROPERTY text -> std::str;
  };
  CREATE TYPE poll::Option EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY rank -> std::int32;
      CREATE REQUIRED PROPERTY text -> std::str;
  };
  CREATE TYPE poll::Poll EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY message_id -> std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (.message_id);
      CREATE REQUIRED PROPERTY channel_id -> std::int64;
      CREATE REQUIRED PROPERTY question -> std::str;
  };
  CREATE TYPE poll::Vote EXTENDING default::ClientObject {
      CREATE REQUIRED LINK poll -> poll::Poll {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE REQUIRED LINK option -> poll::Option {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  CREATE TYPE pot::Pot EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY amount -> std::float32 {
          SET default := 0.0;
          CREATE CONSTRAINT std::min_value(0.0);
      };
      CREATE REQUIRED PROPERTY count -> std::int32 {
          SET default := 0;
      };
  };
  CREATE SCALAR TYPE presence::PresenceType EXTENDING enum<PLAYING, LISTENING, WATCHING>;
  CREATE TYPE presence::Presence EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY name -> std::str;
      CREATE REQUIRED PROPERTY type -> presence::PresenceType;
      CREATE CONSTRAINT std::exclusive ON ((.client, .type, .name));
  };
  CREATE ABSTRACT TYPE anilist::AniListData {
      CREATE REQUIRED PROPERTY favourites -> std::int32;
      CREATE REQUIRED PROPERTY id_al -> std::int32;
      CREATE REQUIRED PROPERTY site_url -> std::str;
      CREATE INDEX ON (.id_al);
  };
  CREATE TYPE projection::Event EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY date -> std::datetime;
      CREATE REQUIRED PROPERTY description -> std::str;
  };
  CREATE TYPE projection::ExternalMedia EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY title -> std::str;
  };
  CREATE SCALAR TYPE projection::Status EXTENDING enum<ONGOING, COMPLETED>;
  CREATE TYPE projection::Projection EXTENDING default::ClientObject {
      CREATE MULTI LINK external_medias -> projection::ExternalMedia {
          ON TARGET DELETE ALLOW;
      };
      CREATE REQUIRED PROPERTY channel_id -> std::int64;
      CREATE PROPERTY message_id -> std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY name -> std::str;
      CREATE REQUIRED PROPERTY status -> projection::Status {
          SET default := (projection::Status.ONGOING);
      };
  };
  CREATE SCALAR TYPE quizz::Status EXTENDING enum<STARTED, ENDED>;
  CREATE TYPE quizz::Game EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY message_id -> std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (.message_id);
      CREATE PROPERTY answer_bananed -> std::str;
      CREATE PROPERTY ended_at -> std::datetime;
      CREATE REQUIRED PROPERTY started_at -> std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY status -> quizz::Status {
          SET default := (quizz::Status.STARTED);
      };
  };
  CREATE TYPE quizz::Quizz EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY channel_id -> std::int64;
      CREATE INDEX ON (.channel_id);
      CREATE PROPERTY answer -> std::str;
      CREATE PROPERTY answer_source -> std::str;
      CREATE PROPERTY description -> std::str;
      CREATE PROPERTY url -> std::str;
      CREATE PROPERTY hikaried := ((.url ILIKE 'https://hikari.butaishoujo.moe%'));
      CREATE REQUIRED PROPERTY is_image -> std::bool {
          SET default := false;
      };
      CREATE REQUIRED PROPERTY submitted_at -> std::datetime {
          SET default := (std::datetime_current());
      };
  };
  CREATE TYPE reminder::Reminder EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY channel_id -> std::int64;
      CREATE REQUIRED PROPERTY message -> std::str;
      CREATE REQUIRED PROPERTY timestamp -> std::datetime;
  };
  CREATE TYPE role::Role EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY emoji -> std::str;
      CREATE CONSTRAINT std::exclusive ON ((.client, .emoji));
      CREATE REQUIRED PROPERTY role_id -> std::int64;
      CREATE CONSTRAINT std::exclusive ON ((.client, .role_id));
      CREATE INDEX ON (.role_id);
  };
  CREATE TYPE waicolle::Collection EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY name -> std::str;
  };
  CREATE TYPE waicolle::Coupon EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY code -> std::str;
      CREATE CONSTRAINT std::exclusive ON ((.client, .code));
      CREATE INDEX ON (.code);
  };
  CREATE SCALAR TYPE waicolle::GameMode EXTENDING enum<WAIFU, HUSBANDO, ALL>;
  CREATE TYPE waicolle::Player EXTENDING default::ClientObject {
      CREATE MULTI LINK tracked_collections -> waicolle::Collection {
          ON TARGET DELETE ALLOW;
      };
      CREATE REQUIRED PROPERTY blood_shards -> std::int32 {
          SET default := 0;
          CREATE CONSTRAINT std::min_value(0);
      };
      CREATE REQUIRED PROPERTY game_mode -> waicolle::GameMode;
      CREATE REQUIRED PROPERTY moecoins -> std::int32 {
          SET default := 0;
          CREATE CONSTRAINT std::min_value(0);
      };
  };
  CREATE TYPE waicolle::Trade EXTENDING default::ClientObject {
      CREATE REQUIRED LINK player_a -> waicolle::Player {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE REQUIRED LINK player_b -> waicolle::Player {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE REQUIRED PROPERTY blood_shards_a -> std::int32 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY blood_shards_b -> std::int32 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY moecoins_a -> std::int32 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY moecoins_b -> std::int32 {
          SET default := 0;
      };
  };
  CREATE SCALAR TYPE waicolle::CollagePosition EXTENDING enum<DEFAULT, LEFT_OF, RIGHT_OF>;
  CREATE TYPE waicolle::Waifu EXTENDING default::ClientObject {
      CREATE REQUIRED LINK owner -> waicolle::Player {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE LINK original_owner -> waicolle::Player {
          ON TARGET DELETE ALLOW;
      };
      CREATE LINK custom_position_waifu -> waicolle::Waifu {
          ON TARGET DELETE ALLOW;
      };
      CREATE REQUIRED PROPERTY blooded -> std::bool {
          SET default := false;
      };
      CREATE REQUIRED PROPERTY custom_collage -> std::bool {
          SET default := false;
      };
      CREATE PROPERTY custom_image -> std::str;
      CREATE PROPERTY custom_name -> std::str;
      CREATE REQUIRED PROPERTY custom_position -> waicolle::CollagePosition {
          SET default := (waicolle::CollagePosition.DEFAULT);
      };
      CREATE REQUIRED PROPERTY level -> std::int32 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY locked -> std::bool {
          SET default := false;
      };
      CREATE REQUIRED PROPERTY nanaed -> std::bool {
          SET default := false;
      };
      CREATE REQUIRED PROPERTY timestamp -> std::datetime {
          SET default := (std::datetime_current());
      };
  };
  ALTER TYPE poll::Option {
      CREATE REQUIRED LINK poll -> poll::Poll {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE CONSTRAINT std::exclusive ON ((.rank, .poll));
      CREATE MULTI LINK votes := (.<option[IS poll::Vote]);
  };
  CREATE TYPE user::User {
      CREATE REQUIRED PROPERTY discord_id -> std::int64 {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (.discord_id);
  };
  ALTER TYPE poll::Vote {
      CREATE REQUIRED LINK user -> user::User {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE CONSTRAINT std::exclusive ON ((.poll, .user));
  };
  ALTER TYPE quizz::Game {
      CREATE REQUIRED LINK quizz -> quizz::Quizz {
          ON TARGET DELETE DELETE SOURCE;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE LINK winner -> user::User {
          ON TARGET DELETE ALLOW;
      };
  };
  ALTER TYPE waicolle::Collection {
      CREATE REQUIRED LINK author -> waicolle::Player {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE CONSTRAINT std::exclusive ON ((.name, .author));
  };
  ALTER TYPE poll::Poll {
      CREATE MULTI LINK options := (.<poll[IS poll::Option]);
  };
  ALTER TYPE projection::Event {
      CREATE REQUIRED LINK projection -> projection::Projection {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE projection::Projection {
      CREATE MULTI LINK events := (.<projection[IS projection::Event]);
  };
  ALTER TYPE quizz::Quizz {
      CREATE LINK game := (.<quizz[IS quizz::Game]);
      CREATE REQUIRED LINK author -> user::User {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  CREATE TYPE amq::Account {
      CREATE REQUIRED LINK user -> user::User {
          ON TARGET DELETE DELETE SOURCE;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY username -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (.username);
  };
  ALTER TYPE user::User {
      CREATE LINK amq := (.<user[IS amq::Account]);
  };
  CREATE SCALAR TYPE anilist::Service EXTENDING enum<ANILIST, MYANIMELIST>;
  CREATE TYPE anilist::Account {
      CREATE REQUIRED LINK user -> user::User {
          ON TARGET DELETE DELETE SOURCE;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY service -> anilist::Service;
      CREATE REQUIRED PROPERTY username -> std::str;
      CREATE CONSTRAINT std::exclusive ON ((.service, .username));
      CREATE INDEX ON ((.service, .username));
  };
  ALTER TYPE user::User {
      CREATE LINK anilist := (.<user[IS anilist::Account]);
  };
  ALTER TYPE pot::Pot {
      CREATE REQUIRED LINK user -> user::User {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE CONSTRAINT std::exclusive ON ((.client, .user));
  };
  ALTER TYPE user::User {
      CREATE MULTI LINK pots := (.<user[IS pot::Pot]);
  };
  CREATE TYPE user::Profile {
      CREATE REQUIRED LINK user -> user::User {
          ON TARGET DELETE DELETE SOURCE;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY full_name -> std::str;
      CREATE PROPERTY photo -> std::str;
      CREATE PROPERTY promotion -> std::str;
      CREATE PROPERTY telephone -> std::str;
  };
  ALTER TYPE user::User {
      CREATE LINK profile := (.<user[IS user::Profile]);
      CREATE MULTI LINK quizzes := (.<author[IS quizz::Quizz]);
  };
  ALTER TYPE reminder::Reminder {
      CREATE REQUIRED LINK user -> user::User {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE user::User {
      CREATE MULTI LINK reminders := (.<user[IS reminder::Reminder]);
  };
  ALTER TYPE waicolle::Player {
      CREATE REQUIRED LINK user -> user::User {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE MULTI LINK waifus := (.<owner[IS waicolle::Waifu]);
  };
  ALTER TYPE user::User {
      CREATE MULTI LINK waicolles := (.<user[IS waicolle::Player]);
  };
  ALTER TYPE waicolle::Trade {
      CREATE MULTI LINK waifus_a -> waicolle::Waifu {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE MULTI LINK waifus_b -> waicolle::Waifu {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE waicolle::Waifu {
      CREATE PROPERTY trade_locked := ((EXISTS (.<waifus_a[IS waicolle::Trade]) OR EXISTS (.<waifus_b[IS waicolle::Trade])));
  };
  CREATE SCALAR TYPE anilist::EntryStatus EXTENDING enum<CURRENT, COMPLETED, PAUSED, DROPPED, PLANNING, REPEATING>;
  CREATE TYPE anilist::Entry {
      CREATE REQUIRED LINK account -> anilist::Account {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE REQUIRED PROPERTY progress -> std::int32;
      CREATE REQUIRED PROPERTY score -> std::float32;
      CREATE REQUIRED PROPERTY status -> anilist::EntryStatus;
  };
  ALTER TYPE anilist::Account {
      CREATE MULTI LINK entries := (.<account[IS anilist::Entry]);
  };
  CREATE SCALAR TYPE waicolle::Rank EXTENDING enum<SS, S, A, B, C, D, E>;
  CREATE TYPE anilist::Character EXTENDING anilist::AniListData {
      ALTER PROPERTY id_al {
          SET OWNED;
          SET REQUIRED;
          SET TYPE std::int32;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY age -> std::str;
      CREATE PROPERTY date_of_birth_day -> std::int32;
      CREATE PROPERTY date_of_birth_month -> std::int32;
      CREATE PROPERTY date_of_birth_year -> std::int32;
      CREATE PROPERTY description -> std::str;
      CREATE PROPERTY gender -> std::str;
      CREATE PROPERTY fuzzy_gender := ((.gender IF EXISTS (.gender) ELSE ((WITH
          female := 
              std::re_match_all(r'(?i)\y(she|her)\y', .description)
          ,
          male := 
              std::re_match_all(r'(?i)\y(he|his)\y', .description)
      SELECT
          (('Female' IF (std::count(female) > std::count(male)) ELSE 'Male') IF ((std::count(female) != std::count(male)) AND (std::max({std::count(female), std::count(male)}) >= (3 * std::min({std::count(female), std::count(male)})))) ELSE <std::str>{})
      ) IF EXISTS (.description) ELSE <std::str>{})));
      CREATE PROPERTY rank := ((waicolle::Rank.SS IF (.favourites >= 10000) ELSE (waicolle::Rank.S IF (.favourites >= 3000) ELSE (waicolle::Rank.A IF (.favourites >= 1000) ELSE (waicolle::Rank.B IF (.favourites >= 200) ELSE (waicolle::Rank.C IF (.favourites >= 20) ELSE (waicolle::Rank.D IF (.favourites >= 1) ELSE waicolle::Rank.E)))))));
      CREATE REQUIRED PROPERTY image_large -> std::str;
      CREATE PROPERTY name_alternative -> array<std::str>;
      CREATE PROPERTY name_alternative_spoiler -> array<std::str>;
      CREATE PROPERTY name_native -> std::str;
      CREATE REQUIRED PROPERTY name_user_preferred -> std::str;
  };
  CREATE SCALAR TYPE anilist::MediaStatus EXTENDING enum<FINISHED, RELEASING, NOT_YET_RELEASED, CANCELLED, HIATUS>;
  CREATE SCALAR TYPE anilist::MediaType EXTENDING enum<ANIME, MANGA>;
  CREATE TYPE anilist::Media EXTENDING anilist::AniListData {
      ALTER PROPERTY id_al {
          SET OWNED;
          SET REQUIRED;
          SET TYPE std::int32;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY chapters -> std::int32;
      CREATE PROPERTY cover_image_color -> std::str;
      CREATE REQUIRED PROPERTY cover_image_extra_large -> std::str;
      CREATE PROPERTY description -> std::str;
      CREATE PROPERTY duration -> std::int32;
      CREATE PROPERTY episodes -> std::int32;
      CREATE PROPERTY id_mal -> std::int32;
      CREATE REQUIRED PROPERTY popularity -> std::int32;
      CREATE PROPERTY status -> anilist::MediaStatus;
      CREATE REQUIRED PROPERTY title_user_preferred -> std::str;
      CREATE REQUIRED PROPERTY type -> anilist::MediaType;
  };
  CREATE TYPE anilist::Staff EXTENDING anilist::AniListData {
      ALTER PROPERTY id_al {
          SET OWNED;
          SET REQUIRED;
          SET TYPE std::int32;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE PROPERTY age -> std::int32;
      CREATE PROPERTY date_of_birth_day -> std::int32;
      CREATE PROPERTY date_of_birth_month -> std::int32;
      CREATE PROPERTY date_of_birth_year -> std::int32;
      CREATE PROPERTY date_of_death_day -> std::int32;
      CREATE PROPERTY date_of_death_month -> std::int32;
      CREATE PROPERTY date_of_death_year -> std::int32;
      CREATE PROPERTY description -> std::str;
      CREATE PROPERTY gender -> std::str;
      CREATE REQUIRED PROPERTY image_large -> std::str;
      CREATE PROPERTY name_native -> std::str;
      CREATE REQUIRED PROPERTY name_user_preferred -> std::str;
  };
  CREATE SCALAR TYPE anilist::CharacterRole EXTENDING enum<MAIN, SUPPORTING, BACKGROUND>;
  CREATE TYPE anilist::CharacterEdge {
      CREATE REQUIRED LINK character -> anilist::Character {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE REQUIRED LINK media -> anilist::Media {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE CONSTRAINT std::exclusive ON ((.character, .media));
      CREATE MULTI LINK voice_actors -> anilist::Staff {
          ON TARGET DELETE ALLOW;
      };
      CREATE REQUIRED PROPERTY character_role -> anilist::CharacterRole;
  };
  ALTER TYPE anilist::Character {
      CREATE MULTI LINK edges := (.<character[IS anilist::CharacterEdge]);
  };
  ALTER TYPE waicolle::Waifu {
      CREATE REQUIRED LINK character -> anilist::Character {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE anilist::Media {
      CREATE MULTI LINK character_edges := (.<media[IS anilist::CharacterEdge]);
  };
  ALTER TYPE anilist::Staff {
      CREATE MULTI LINK character_edges := (.<voice_actors[IS anilist::CharacterEdge]);
  };
  ALTER TYPE anilist::Entry {
      CREATE REQUIRED LINK media -> anilist::Media {
          ON TARGET DELETE DELETE SOURCE;
      };
  };
  ALTER TYPE anilist::Media {
      CREATE MULTI LINK entries := (.<media[IS anilist::Entry]);
  };
  CREATE TYPE anilist::Image {
      CREATE REQUIRED PROPERTY url -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (.url);
      CREATE REQUIRED PROPERTY data -> std::str;
  };
  ALTER TYPE projection::Projection {
      CREATE MULTI LINK medias -> anilist::Media {
          ON TARGET DELETE ALLOW;
      };
  };
  ALTER TYPE waicolle::Collection {
      CREATE MULTI LINK medias -> anilist::Media {
          ON TARGET DELETE ALLOW;
      };
  };
  ALTER TYPE waicolle::Player {
      CREATE MULTI LINK tracked_medias -> anilist::Media {
          ON TARGET DELETE ALLOW;
      };
      CREATE CONSTRAINT std::exclusive ON ((.client, .user));
  };
  ALTER TYPE waicolle::Coupon {
      CREATE MULTI LINK claimed_by -> waicolle::Player {
          ON TARGET DELETE ALLOW;
      };
  };
};
