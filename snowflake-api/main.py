import os
from fastapi import FastAPI, HTTPException
import snowflake.connector
from dotenv import load_dotenv
from snowflake.connector import DictCursor
from mangum import Mangum
import traceback

# Load environment variables
load_dotenv()

app = FastAPI()

def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

@app.get("/snowflake-version")
def get_snowflake_version():
    """
    Retrieve the current version of the Snowflake instance.
    Example Response: {"version": "8.5.1"}
    """
    try:
        #return {"message": "Disabling snowflake, should be returned!"}
        
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        
        # Execute the specific Snowflake version function
        cursor.execute("SELECT CURRENT_VERSION()")
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return {"version": result[0]}
        raise HTTPException(status_code=404, detail="Version not found")
        
    except Exception as e:
        #raise HTTPException(status_code=500, detail=str(e))
        # Capture the full stack trace as a string
        stack_trace = traceback.format_exc()
        
        # Include it in the detail field
        raise HTTPException(
            status_code=500, 
            detail={
                "error": str(e),
                "traceback": stack_trace
            }
        )


@app.get("/query")
def run_query(sql: str = "SELECT CURRENT_VERSION()"):
    try:
        conn = get_snowflake_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/test")
def test():
    return {"message": "If you see this, CURL and Mangum are working!"}

@app.get("/menu-items")
def get_menu_items(limit: int = 10):
    """
    Retrieve menu items from the Tasty Bytes RAW_POS schema.
    """
    try:
        conn = get_snowflake_connection()
        # Use DictCursor so results are returned as dictionaries
        cursor = conn.cursor(DictCursor)
        
        query = f"SELECT truck_brand_name, menu_item_name, item_category FROM MENU LIMIT {limit}"
        
        
        cursor.execute(query)
        result = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {"items": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

handler = Mangum(app)

