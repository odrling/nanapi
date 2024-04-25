CREATE MIGRATION m1kcicmm33tphhg355yyt2azjsijzp3hwk63oxfj2qsz22iyi2hhcq
    ONTO m1mgsapt43fibeutomf7j46escoh7vhehqr5syav5g5l4iutilnuqq
{
  ALTER TYPE default::Client {
      CREATE REQUIRED PROPERTY password_hash -> std::str {
          SET REQUIRED USING ('');
      };
  };
};
