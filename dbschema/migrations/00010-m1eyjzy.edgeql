CREATE MIGRATION m1eyjzygebrxrqjnmi6nw52sp6wi2fuf42wb3oxqgmbnpmnzhefhva
    ONTO m1yvlmumz4lgdyae7v5xiy7bn4wgwqkocowg3jdacklvfhkfo5myxq
{
  ALTER TYPE poll::Poll {
      CREATE REQUIRED PROPERTY channel_id_str := (<std::str>.channel_id);
      CREATE REQUIRED PROPERTY message_id_str := (<std::str>.message_id);
  };
  ALTER TYPE projection::Projection {
      CREATE REQUIRED PROPERTY channel_id_str := (<std::str>.channel_id);
      CREATE PROPERTY message_id_str := (<std::str>.message_id);
  };
  ALTER TYPE quizz::Game {
      CREATE REQUIRED PROPERTY message_id_str := (<std::str>.message_id);
  };
  ALTER TYPE quizz::Quizz {
      CREATE REQUIRED PROPERTY channel_id_str := (<std::str>.channel_id);
  };
  ALTER TYPE reminder::Reminder {
      CREATE REQUIRED PROPERTY channel_id_str := (<std::str>.channel_id);
  };
  ALTER TYPE role::Role {
      CREATE REQUIRED PROPERTY role_id_str := (<std::str>.role_id);
  };
  ALTER TYPE user::User {
      CREATE REQUIRED PROPERTY discord_id_str := (<std::str>.discord_id);
  };
};
