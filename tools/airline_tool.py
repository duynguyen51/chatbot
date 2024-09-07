import httpx
from llama_index.core.query_engine import JSONalyzeQueryEngine
from llama_index.core.tools import BaseTool, FunctionTool
from typing import List, Dict
from datetime import datetime
from llm import LLM_MODEL

URL_FLIGHTS_RECORD = "https://flightrecordapi.airlegit.com/api/airlegit/records/{}"


def preprocess_flight_record(record):
    content = record['payload']
    flight_stats = content['AirlineStats']
    delay_stats = content['DelayRatings']

    historical_stats = []

    for history in flight_stats:
        # print(history)
        stat = history['flightstatus']
        duration = str(stat['duration'] / 3600) + " hours"
        scheduled_departure = datetime.fromtimestamp(stat['scheduled']['departure'])
        scheduled_arrive = datetime.fromtimestamp(stat['scheduled']['arrival'])

        real_departure = datetime.fromtimestamp(stat['real']['departure'])
        real_arrive = datetime.fromtimestamp(stat['real']['arrival'])

        destination_info = history['destination']
        depart_country = destination_info['country']
        depart_city = destination_info['city']
        depart_airport = destination_info['airportcode']
        depart_airport_name = destination_info['airportname']

        origin_info = history['origin']
        origin_country = origin_info['country']
        origin_city = origin_info['city']
        origin_airport = origin_info['airportcode']
        origin_airport_name = origin_info['airportname']

        historical_stats.append({

            "airline_code": history['airlinecode'],
            "duration": duration,
            "scheduled_departure": scheduled_departure,
            "scheduled_arrive": scheduled_arrive,
            "real_departure": real_departure,
            "real_arrive": real_arrive,
            "depart_country": depart_country,
            "depart_city": depart_city,
            "depart_airport": depart_airport,
            "depart_airport_name": depart_airport_name,
            "origin_country": origin_country,
            "origin_city": origin_city,
            "origin_airport": origin_airport,
            "origin_airport_name": origin_airport_name,
        })

    return historical_stats, delay_stats


def get_flight_record(flight_id: str):
    response = httpx.get(URL_FLIGHTS_RECORD.format(flight_id))

    if response.status_code == 200:
        return response.json()
    else:
        return None


def parsing_airline_records(flight_id: str):
    record = get_flight_record(flight_id)
    if record is None:
        return None

    historical_stats, delay_stats = preprocess_flight_record(record)

    return {
        "summary_information": historical_stats,
        # "delay_stats": delay_stats
    }


def get_airline_stat_tool(question: str, airline_historical_stat: List[Dict]):
    tools = JSONalyzeQueryEngine(
        list_of_dict=airline_historical_stat,
        llm=LLM_MODEL,
    )
    return tools.query(question)


def get_analyzer_delay_tool(question: str, airline_delay_stat: Dict):
    tools = JSONalyzeQueryEngine(
        list_of_dict=[airline_delay_stat],
        llm=LLM_MODEL,
    )
    return tools.query(question)


airline_delay_analyzer = FunctionTool.from_defaults(
    name="airline_delay_analyzer",
    description="Analyze the delay data from delay stats of the flight",
    fn=get_analyzer_delay_tool
)

airline_historical_tools = FunctionTool.from_defaults(
    name="airline_historical_tools",
    description="Answer and analyze the airline summary information about the flight",
    fn=get_airline_stat_tool
)

airline_history_retrieve = FunctionTool.from_defaults(
    name="airline_history_retrieve",
    description="First retrieve the airline historical data from airline code provided by user",
    fn=parsing_airline_records
)

