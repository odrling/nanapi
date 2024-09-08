CREATE MIGRATION m1feetbb32tka62czllwesfvtafxlxkt4idcqkwanjaptlhytvul4q
    ONTO m1ebtz4vac7ldmn7yyir3mzfq6efubespf6k5kzrr3eqslesj6grka
{
  CREATE MODULE calendar IF NOT EXISTS;
  CREATE TYPE calendar::GuildEvent EXTENDING default::ClientObject {
      CREATE REQUIRED PROPERTY discord_id: std::int64;
      CREATE CONSTRAINT std::exclusive ON ((.client, .discord_id));
      CREATE MULTI LINK participants: user::User {
          ON TARGET DELETE ALLOW;
      };
      CREATE REQUIRED LINK organizer: user::User {
          ON TARGET DELETE DELETE SOURCE;
      };
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY discord_id_str := (<std::str>.discord_id);
      CREATE REQUIRED PROPERTY end_time: std::datetime;
      CREATE PROPERTY image: std::str;
      CREATE PROPERTY location: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE REQUIRED PROPERTY start_time: std::datetime;
      CREATE PROPERTY url: std::str;
  };
  ALTER TYPE user::User {
      CREATE MULTI LINK events := (.<participants[IS calendar::GuildEvent]);
  };
  CREATE TYPE calendar::UserCalendar {
      CREATE REQUIRED LINK user: user::User {
          ON TARGET DELETE DELETE SOURCE;
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY ics: std::str;
  };
  ALTER TYPE user::User {
      CREATE LINK calendar := (.<user[IS calendar::UserCalendar]);
  };
};
