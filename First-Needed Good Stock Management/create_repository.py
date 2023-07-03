import oracledb
import database_connection

# Establish a connection

with oracledb.connect(user = database_connection.USERNAME, password = database_connection.PASSWORD, 
                      encoding = "UTF-8", dsn = database_connection.dsn) as connection:
    with connection.cursor() as cursor:
        
        def create_expirable_groceries_table():
            # Execute the query
            try:
                cursor.execute("""BEGIN
                    EXECUTE IMMEDIATE 'CREATE TABLE expirable_groceries (
                        id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        name VARCHAR2(100),
                        category VARCHAR2(100),
                        quantity NUMBER,
                        product_creation_date timestamp,
                        expiration_date timestamp,
                        created_at timestamp,
                        updated_at timestamp                     
                    )';
                        EXCEPTION
                            WHEN OTHERS THEN
                                IF SQLCODE = -955 THEN  -- ORA-00955: table already exists
                                    NULL;  -- Ignore the error
                                ELSE
                                    RAISE;  -- Reraise the exception
                                END IF;
                        END;
                """)

                connection.commit()
            except oracledb.DatabaseError as db_error:
                print(db_error)

        create_expirable_groceries_table()
        
        def create_unexpirable_groceries_table():
            # Execute the query
            try:
                cursor.execute("""BEGIN
                    EXECUTE IMMEDIATE 'CREATE TABLE unexpirable_groceries (
                        id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                        name VARCHAR2(100),
                        category VARCHAR2(100),
                        quantity NUMBER,
                        created_at timestamp,
                        updated_at timestamp
                    )';
                        EXCEPTION
                            WHEN OTHERS THEN
                                IF SQLCODE = -955 THEN  -- ORA-00955: table already exists
                                    NULL;  -- Ignore the error
                                ELSE
                                    RAISE;  -- Reraise the exception
                                END IF;
                        END;
                """)

                connection.commit()
            except oracledb.DatabaseError as db_error:
                print(db_error)

        create_unexpirable_groceries_table()

    
 




