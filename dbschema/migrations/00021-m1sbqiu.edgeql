CREATE MIGRATION m1sbqiuyd3lhky4vdepxxacsxe4p7t4l5yeeyu3uaeedaf323shwha
    ONTO m1sbe5j6b6udweu2ah6uftugisxdyebbxlkpqugupnburuvapqakda
{
  ALTER TYPE projection::Projection {
      CREATE MULTI LINK guild_events: calendar::GuildEvent {
          ON TARGET DELETE ALLOW;
          CREATE CONSTRAINT std::exclusive;
      };
  };
  ALTER TYPE calendar::GuildEvent {
      CREATE LINK projection := (.<guild_events[IS projection::Projection]);
  };
  ALTER TYPE projection::Event RENAME TO projection::LegacyEvent;
  ALTER TYPE projection::Projection {
      ALTER LINK events {
          RENAME TO legacy_events;
      };
  };
  ALTER TYPE user::User {
      ALTER LINK events {
          RENAME TO guild_events;
      };
  };
};
