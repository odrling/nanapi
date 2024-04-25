CREATE MIGRATION m134f3eja3e4h67lcrqcs2ogwteeebnbvy5xadcrczobmsoqpbpowa
    ONTO m1jl3kjlaascxqdr4qfw7tx445vzfewn4gmf6clvwyv4eom4ogvrwq
{
  ALTER TYPE anilist::Media {
      CREATE REQUIRED PROPERTY synonyms -> array<std::str> {
          SET REQUIRED USING (<array<std::str>>[]);
      };
      CREATE PROPERTY title_english -> std::str;
      CREATE PROPERTY title_native -> std::str;
  };
  ALTER TYPE anilist::Staff {
      CREATE REQUIRED PROPERTY name_alternative -> array<std::str> {
          SET REQUIRED USING (<array<std::str>>[]);
      };
  };
  ALTER TYPE anilist::Tag {
      ALTER PROPERTY name {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
