# Ostadkar-api

Python REST API for Ostadkar back-end

1. Add swagger endpoints plus definitions. Keep in mind that you must include the following items within definitions:
 
    - title
    - description (if needed)
 
2. Generate SqlAlchemy model from swagger using the project
 [SwaggerSqlalchemyGen](https://github.com/kamyar1979/swaggersqlagen)

3. Add the output to the code and create directory structure if needed.

4. Create a repository class if required or add methods to existing repository class.

5. Create handler module or add handler functions to the existing module.

6. Add required function arguments with type annotations 

7. Add route and dispatching decorators to the handler function

8. Add errors and localized messages

9. Use serialize and HTTP status for response
