CREATE MIGRATION m1jl3kjlaascxqdr4qfw7tx445vzfewn4gmf6clvwyv4eom4ogvrwq
    ONTO m15w66cnnzfjq2wszuqirj2f3i52ra64omk2v6knxbctm3skdyyusq
{
  ALTER TYPE anilist::Character {
      ALTER PROPERTY name_alternative {
          SET REQUIRED USING (<array<std::str>>[]);
      };
  };
  ALTER TYPE anilist::Character {
      ALTER PROPERTY name_alternative_spoiler {
          SET REQUIRED USING (<array<std::str>>[]);
      };
  };
  CREATE TYPE anilist::Tag {
      CREATE REQUIRED PROPERTY id_al -> std::int32 {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE INDEX ON (.id_al);
      CREATE REQUIRED PROPERTY category -> std::str;
      CREATE REQUIRED PROPERTY description -> std::str;
      CREATE REQUIRED PROPERTY is_adult -> std::bool;
      CREATE REQUIRED PROPERTY name -> std::str;
  };
  ALTER TYPE anilist::Media {
      CREATE MULTI LINK tags -> anilist::Tag {
          CREATE PROPERTY rank -> std::int32;
      };
      CREATE REQUIRED PROPERTY genres -> array<std::str> {
          SET REQUIRED USING (<array<std::str>>[]);
      };
      CREATE REQUIRED PROPERTY is_adult -> std::bool {
          SET REQUIRED USING (false);
      };
  };
  ALTER TYPE anilist::Tag {
      CREATE MULTI LINK medias := (.<tags[IS anilist::Media]);
  };
};
