CREATE MIGRATION m1lyp3h2y47mktrtmxcvv2quinwm3ur6bb3zttsg7rjzgz53lr6a4a
    ONTO m1foqeni64zy7clxk3jbqdxm4ozesieofvuldxx3qg3azwfwxglcqa
{
  ALTER TYPE waicolle::RollOperation {
      ALTER PROPERTY roll_id {
          RENAME TO reason;
      };
  };
};
