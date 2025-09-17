#
# Copyright 2025 Amazon.com, Inc. and its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#   http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
#

from typing import Annotated, Union
from pydantic import Field
from mcp_server import mcp_server
import logging
from . import knowledge_base_lookup
from . import user_profile_by_booking_reference
from . import user_profile_by_ffn
from . import create_support_ticket
from . import request_for_special_meal
from . import flifo
from . import air_shopping
from datetime import date

logger = logging.getLogger(__name__)

# Knowledge Base Lookup Tool
@mcp_server.tool(
    name="lookup",
    description="Runs query against a knowledge base to retrieve information."
)
async def lookup_tool(
    query: Annotated[str, Field(description="the query to search")]
) -> dict:
    """Look up information in the knowledge base"""
    try:
        logger.info(f"Knowledge base lookup query: {query}")
        results = knowledge_base_lookup.main(query)
        return results  
    except Exception as e:
        logger.error(f"Error in knowledge base lookup: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}


# User Profile Search Tool by Booking Reference
@mcp_server.tool(
    name="userProfileByBookingReference",
    description="Search for a user's flight booking information using their booking reference"
)
async def user_profile_by_booking_reference_tool(
    booking_reference: Annotated[Union[int, str], Field(description="the user's booking reference in format GCI7NE")]
) -> dict:
    """Search for user flight booking information by booking reference"""
    try:
        logger.info(f"User profile search by booking reference: {booking_reference}")
        results = user_profile_by_booking_reference.main(booking_reference)
        return results  
    except Exception as e:
        logger.error(f"Error in user profile search by booking reference: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}

# User Profile Search Tool by Frequent Flyer Number 
@mcp_server.tool(
    name="userProfileByFrequentFlyerNumber",
    description="Search for a user's flight booking information using their frequent flyer number"
)
async def user_profile_by_frequent_flyer_number_tool(
    frequentFlyerNumber: Annotated[Union[int, str], Field(description="the user's frequent flyer number")]
) -> dict:
    """Search for user flight booking information by frequent flyer number"""
    try:
        logger.info(f"User profile search by frequent flyer number: {frequentFlyerNumber}")
        results = user_profile_by_ffn.main(frequentFlyerNumber)
        return results  
    except Exception as e:
        logger.error(f"Error in user profile search by frequent flyer number: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}

# Create a support ticket
@mcp_server.tool(
    name="createSupportTicket",
    description="Creates a support ticket by logging the details of the customer issue"
)
async def create_support_ticket_tool(
    issue_summary: Annotated[Union[str], Field(description="A summary of the issue raised by the user")],
    booking_reference: Annotated[Union[str], Field(description="The booking reference to associate with the support ticket in format KYH7BH")]
) -> dict:
    """create a support ticket for for a specific flight with provided booking ref"""
    try:
        logger.info(f"User profile search by booking ref: {booking_reference}")
        results = create_support_ticket.main(issue_summary, booking_reference)
        return results  
    except Exception as e:
        logger.error(f"Error locating records with provided booking reference: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}

# Take a request for a special meal
@mcp_server.tool(
    name="requestForSpecialMeal",
    description="Use this tool when a user wants to request a special meal for their flight or request for a change in the meal already ordered."
)
async def request_for_special_meal_tool(
    booking_reference: Annotated[Union[str], Field(description="The booking reference to associate with the support ticket in format KYH7BH")],
    meal_type: Annotated[Union[str], Field(description="The type of special meal requested. Options are vegetarian, halal, fruit salad.")],
    
) -> dict:
    """Use this tool when a user wants to request a special meal for their flight or request for a change in the meal already ordered."""
    try:
        logger.info(f"Creating special meal request for booking reference number : {booking_reference}")
        results = request_for_special_meal.main(booking_reference, meal_type)
        return results  
    except Exception as e:
        logger.error(f"Error locating records with provided booking reference: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}




# Air inspiration shopping
@mcp_server.tool(
    name="getAirDestinationsAndRespectiveCheapestPrices",
    description="Use this tool when a user asks for inspirational destinations. Insist on the fact that prices vary and users need to look for detailed flight options next."
)
async def get_air_destinations_and_respective_cheapest_prices(
   origin_airport: Annotated[Union[str], Field(description="Origin IATA airport code where the customer will be departing from. Always use an IATA airport code.")]    
) -> dict:
    """Provides an array of available destinations and respective cheapest price per roundtrip passenger from an origin airport."""
    try:
        logger.info(f"get_air_destinations_and_respective_cheapest_prices({origin_airport})")
        results = air_shopping.get_air_destinations_and_respective_cheapest_prices(origin_airport)
        logger.info(f"get_air_destinations_and_respective_cheapest_prices({origin_airport})={results}")
        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Error: get_air_destinations_and_respective_cheapest_prices()", exc_info=True)
        return {"status": "error", "error": str(e)}

# Flight status
@mcp_server.tool(
    name="getAirlineFlightDateStatus",
    description="Use this tool when a user asks about flight status. Remind the user of the departure date and flight number before answering the question, and specifically highlight a delay on arrival if any."
)
async def get_airline_flight_date_status(
   flight_number: Annotated[Union[str], Field(description="Flight number the customer asked for")],
   departure_date: Annotated[Union[date], Field(description="Departure date of the flight the customer asked about. If the customer asks about today or tomorrow, convert it to the right format before calling the tool.")]    
) -> dict:
    """Returns the status of a flight date including scheduled and actual times, progress, etc."""
    try:
        logger.info(f"get_airline_flight_date_status({flight_number}, {departure_date})")
        results = flifo.get_airline_flight_date_status(flight_number, departure_date)
        logger.info(f"get_airline_flight_date_status({flight_number}, {departure_date})={results}")
        return {"status": "success", "results": results}
    except Exception as e:
        logger.error(f"Error: get_airline_flight_date_status()", exc_info=True)
        return {"status": "error", "error": str(e)}





