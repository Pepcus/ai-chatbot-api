db_schema = '''

Table Definition
table_name|column_name  |data_type                  |table_schema|
----------+-------------+---------------------------+------------+
chat      |created_at   |timestamp without time zone|public      |
chat      |user_id      |integer                    |public      |
chat      |title        |character varying          |public      |
chat      |path         |character varying          |public      |
chat      |id           |character varying          |public      |
chat      |messages     |ARRAY                      |public      |
chat      |share_path   |character varying          |public      |
employee  |employee_id  |integer                    |public      |
employee  |designation  |character varying          |public      |
employee  |email        |character varying          |public      |
employee  |department   |character varying          |public      |
employee  |phone_number |character varying          |public      |
employee  |name         |character varying          |public      |
employee  |address      |text                       |public      |
leave     |employee_id  |integer                    |public      |
leave     |id           |integer                    |public      |
leave     |leave_type   |character varying          |public      |
leave     |status       |character varying          |public      |
leave     |end_date     |date                       |public      |
leave     |start_date   |date                       |public      |
salary    |to_date      |date                       |public      |
salary    |from_date    |date                       |public      |
salary    |id           |integer                    |public      |
salary    |employee_id  |integer                    |public      |
salary    |salary_amount|numeric                    |public      |
users     |id           |integer                    |public      |
users     |company      |character varying          |public      |
users     |password     |character varying          |public      |
users     |salt         |character varying          |public      |
users     |name         |character varying          |public      |
users     |email        |character varying          |public      |

Table Relationship
source_table|source_column|target_table|target_column|
------------+-------------+------------+-------------+
chat        |user_id      |users       |id           |
leave       |employee_id  |employee    |employee_id  |
salary      |employee_id  |employee    |employee_id  |

'''