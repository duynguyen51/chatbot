from sqlalchemy import create_engine, Engine

from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine, SQLTableRetrieverQueryEngine, PGVectorSQLQueryEngine
from llama_index.core.tools import QueryEngineTool

from llm import LLM_MODEL

from config import config

DB_ENGINE_NAME = config["football_db"]["db_name"]
DB_TABLES = config["football_db"]["db_tables"]


def get_db_engine(db_engine_name: str = 'duckdb') -> Engine:
    return create_engine(db_engine_name)


def get_football_sql_tool() -> QueryEngineTool:
    engine = get_db_engine(DB_ENGINE_NAME)

    sql_database = SQLDatabase(
        engine,
        include_tables=DB_TABLES,
        schema='dev'
    )

    query_engine = PGVectorSQLQueryEngine(sql_database, llm=LLM_MODEL, verbose=True)

    sql_tool = QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name='football_sql_tool',
        description='SQL tool for looking up information from football database',
    )

    return sql_tool


football_sql_tool = get_football_sql_tool()
