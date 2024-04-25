CREATE MIGRATION m15w66cnnzfjq2wszuqirj2f3i52ra64omk2v6knxbctm3skdyyusq
    ONTO m17r4sy23vrv4mvvuarlrduao6uslw3e2oaacgmzm5k66qcyslwh4q
{
  ALTER TYPE user::User {
      CREATE REQUIRED PROPERTY discord_username -> std::str {
          SET REQUIRED USING ('');
      };
  };
};
