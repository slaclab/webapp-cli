import datetime
import csv
import io
import logging

from typing import Union, List
from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse

from lcls.events import LCLSEventClient, Event, Line, Machine, TimetableRow
from facet.events import FACETEventClient, Event as FACETEvent, TimetableRow as FACETTimetableRow
from spear.events import SPEAREventClient, Event as SPEAREvent, TimetableRow as SPEARTimetableRow

logger = logging.getLogger('uvicorn.error')
lcls_calendar_client = LCLSEventClient()
app = FastAPI(root_path=lcls_calendar_client.config.get("rootPath", ""))

@app.get("/events/", response_model=List[Event])
@app.get("/lcls/events/", response_model=List[Event])
@app.get("/events.json", response_model=List[Event])
@app.get("/lcls/events.json", response_model=List[Event])
def read_events(response: Response, line: Union[Line, None] = None, machine: Union[Machine, None] = None, non_program_events: bool = False, start_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None, limit: Union[int, None] = None):
    """
    Retrieve program calendar events.
    
    - **line**: Optional, filters requests by undulator line. Can be "HXR" or "SXR".
    - **machine**: Optional, filters requests by source accelerator.  Can be "NC" or "SC".
    - **non_program_events**: Optional, boolean.  "True" will include other calendar events
                              that are not scheduled user or MD programs.
    - **start_time**: Optional, datetime.  Only show events after this date.
    - **end_time**: Optional, datetime.  Only show events before this date.
    - **limit**: Optional, int.  Only return this many items.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    return lcls_calendar_client.fetch_events(line=line, machine=machine, non_program_events=non_program_events, start_time=start_time, end_time=end_time, limit=limit)
    
@app.get("/events.csv")
@app.get("/lcls/events.csv")
def read_events_csv(response: Response, line: Union[Line, None] = None, machine: Union[Machine, None] = None, non_program_events: bool = False, start_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None, limit: Union[int, None] = None):
    """
    Retrieve program calendar events as a CSV file.
    
    - **line**: Optional, filters requests by undulator line. Can be "HXR" or "SXR".
    - **machine**: Optional, filters requests by source accelerator.  Can be "NC" or "SC".
    - **non_program_events**: Optional, boolean.  "True" will include other calendar events
                              that are not scheduled user or MD programs.
    - **start_time**: Optional, datetime.  Only show events after this date.
    - **end_time**: Optional, datetime.  Only show events before this date.
    - **limit**: Optional, int.  Only return this many items.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    events = lcls_calendar_client.fetch_events(line=line, machine=machine, non_program_events=non_program_events, start_time=start_time, end_time=end_time, limit=limit)
    fieldnames = ["start", "end", "description", "note", "details"]
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction='ignore', dialect='excel-tab')
    writer.writeheader()
    for event in events:
        writer.writerow(event.model_dump())

    return StreamingResponse(io.StringIO(stream.getvalue()), headers={"Access-Control-Allow-Origin": "*", "Content-Disposition": "attachment; filename=events.csv"}, media_type="text/csv")
    
        
        
    

@app.get("/timetable/", response_model=List[TimetableRow])
@app.get("/lcls/timetable/", response_model=List[TimetableRow])
@app.get("/timetable.json", response_model=List[TimetableRow])
@app.get("/lcls/timetable.json", response_model=List[TimetableRow])
def read_timetable(response: Response, line: Union[Line, None] = None, machine: Union[Machine, None] = None, non_program_events: bool = False, start_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None, limit: Union[int, None] = None):
    """
    Retrieve program calendar events in a "timetable" format.
    This format returns a list of timespans.  Each timespan has a start and end,
    and a list of events that fall within that timespan.  This method is more convenient for
    some display uses.
    
    - **line**: Optional, filters requests by undulator line. Can be "HXR" or "SXR".
    - **machine**: Optional, filters requests by source accelerator.  Can be "NC" or "SC".
    - **non_program_events**: Optional, boolean.  "True" will include other calendar events
                              that are not scheduled user or MD programs.
    - **start_time**: Optional, datetime.  Only show events after this date.
    - **end_time**: Optional, datetime.  Only show events before this date.
    - **limit**: Optional, int.  Only return this many items.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    return lcls_calendar_client.make_event_timetable(lcls_calendar_client.fetch_events(line=line, machine=machine, non_program_events=non_program_events, start_time=start_time, end_time=end_time), limit=limit)

facet_calendar_client = FACETEventClient()

@app.get("/facet/events/", response_model=List[FACETEvent])
@app.get("/facet/events.json", response_model=List[FACETEvent])
def read_facet_events(response: Response, start_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None, limit: Union[int, None] = None):
    """
    Retrieve FACET program calendar events.
    
    - **start_time**: Optional, datetime.  Only show events after this date.
    - **end_time**: Optional, datetime.  Only show events before this date.
    - **limit**: Optional, int.  Only return this many items.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    return facet_calendar_client.fetch_events(start_time=start_time, end_time=end_time, limit=limit)
    
@app.get("/facet/events.csv")
def read_facet_events_csv(response: Response, start_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None, limit: Union[int, None] = None):
    """
    Retrieve FACET program calendar events as a CSV file.
    
    - **start_time**: Optional, datetime.  Only show events after this date.
    - **end_time**: Optional, datetime.  Only show events before this date.
    - **limit**: Optional, int.  Only return this many items.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    events = facet_calendar_client.fetch_events(start_time=start_time, end_time=end_time, limit=limit)
    fieldnames = ["start", "end", "description", "note", "details"]
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction='ignore', dialect='excel-tab')
    writer.writeheader()
    for event in events:
        writer.writerow(event.model_dump())

    return StreamingResponse(io.StringIO(stream.getvalue()), headers={"Access-Control-Allow-Origin": "*", "Content-Disposition": "attachment; filename=events.csv"}, media_type="text/csv")
    
        
        
    

@app.get("/facet/timetable/", response_model=List[FACETTimetableRow])
@app.get("/facet/timetable.json", response_model=List[FACETTimetableRow])
def read_facet_timetable(response: Response, start_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None, limit: Union[int, None] = None):
    """
    Retrieve FACET program calendar events in a "timetable" format.
    This format returns a list of timespans.  Each timespan has a start and end,
    and a list of events that fall within that timespan.  This method is more convenient for
    some display uses.
    
    - **start_time**: Optional, datetime.  Only show events after this date.
    - **end_time**: Optional, datetime.  Only show events before this date.
    - **limit**: Optional, int.  Only return this many items.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    return facet_calendar_client.make_event_timetable(facet_calendar_client.fetch_events(start_time=start_time, end_time=end_time), limit=limit)

################
spear_calendar_client = SPEAREventClient()

@app.get("/spear/events/", response_model=List[SPEAREvent])
@app.get("/spear/events.json", response_model=List[SPEAREvent])
def read_spear_events(response: Response, start_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None, limit: Union[int, None] = None):
    """
    Retrieve SPEAR program calendar events.
    
    - **start_time**: Optional, datetime.  Only show events after this date.
    - **end_time**: Optional, datetime.  Only show events before this date.
    - **limit**: Optional, int.  Only return this many items.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    return spear_calendar_client.fetch_events(start_time=start_time, end_time=end_time, limit=limit)
    
@app.get("/spear/events.csv")
def read_spear_events_csv(response: Response, start_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None, limit: Union[int, None] = None):
    """
    Retrieve SPEAR program calendar events as a CSV file.
    
    - **start_time**: Optional, datetime.  Only show events after this date.
    - **end_time**: Optional, datetime.  Only show events before this date.
    - **limit**: Optional, int.  Only return this many items.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    events = spear_calendar_client.fetch_events(start_time=start_time, end_time=end_time, limit=limit)
    fieldnames = ["start", "end", "description", "note", "details"]
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=fieldnames, extrasaction='ignore', dialect='excel-tab')
    writer.writeheader()
    for event in events:
        writer.writerow(event.model_dump())

    return StreamingResponse(io.StringIO(stream.getvalue()), headers={"Access-Control-Allow-Origin": "*", "Content-Disposition": "attachment; filename=events.csv"}, media_type="text/csv")
    
        
        
    

@app.get("/spear/timetable/", response_model=List[SPEARTimetableRow])
@app.get("/spear/timetable.json", response_model=List[SPEARTimetableRow])
def read_spear_timetable(response: Response, start_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None, limit: Union[int, None] = None):
    """
    Retrieve SPEAR program calendar events in a "timetable" format.
    This format returns a list of timespans.  Each timespan has a start and end,
    and a list of events that fall within that timespan.  This method is more convenient for
    some display uses.
    
    - **start_time**: Optional, datetime.  Only show events after this date.
    - **end_time**: Optional, datetime.  Only show events before this date.
    - **limit**: Optional, int.  Only return this many items.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    return spear_calendar_client.make_event_timetable(spear_calendar_client.fetch_events(start_time=start_time, end_time=end_time), limit=limit)


if __name__=="__main__":
    lcls_calendar_client.fetch_events()