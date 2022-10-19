from cdp_data import CDPInstances
from cdp_data.utils import connect_to_infrastructure
from fireo.models import Model
from google.cloud.firestore_v1.transaction import Transaction
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from cdp_backend.database import models as db_models
from cdp_backend.database import sqlite_models
from cdp_backend.database.constants import (
    BODY,
    EVENT,
    EVENT_MINUTES_ITEM,
    EVENT_MINUTES_ITEM_FILE,
    FILE,
    MATTER,
    MATTER_FILE,
    MATTER_SPONSOR,
    MATTER_STATUS,
    MINUTES_ITEM,
    PERSON,
    ROLE,
    SEAT,
    SESSION,
    TRANSCRIPT,
    VOTE,
)

# Init transaction and auth
# fireo.connection(from_file=".keys/cdp-albuquerque-1d29496e.json")
# Connect to the database
connect_to_infrastructure(CDPInstances.Albuquerque)
engine = create_engine("sqlite:///test.db", echo=True, future=True)

# Create tables!
sqlite_models.Base.metadata.create_all(engine, tables=None, checkfirst=True)

model_list = [
    {BODY: db_models.Body},
    {EVENT: db_models.Event},
    {EVENT_MINUTES_ITEM: db_models.EventMinutesItem},
    {EVENT_MINUTES_ITEM_FILE: db_models.EventMinutesItemFile},
    {FILE: db_models.File},
    {MATTER: db_models.Matter},
    {MATTER_FILE: db_models.MatterFile},
    {MATTER_SPONSOR: db_models.MatterSponsor},
    {MATTER_STATUS: db_models.MatterStatus},
    {MINUTES_ITEM: db_models.MinutesItem},
    {PERSON: db_models.Person},
    {ROLE: db_models.Role},
    {SESSION: db_models.Session},
    {SEAT: db_models.Seat},
    {TRANSCRIPT: db_models.Transcript},
    {VOTE: db_models.Vote},
]


def get_sql_schema(model_name: str) -> Model:
    if model_name == BODY:
        return sqlite_models.Body()
    elif model_name == EVENT:
        return sqlite_models.Event()
    elif model_name == EVENT_MINUTES_ITEM:
        return sqlite_models.EventMinutesItem()
    elif model_name == EVENT_MINUTES_ITEM_FILE:
        return sqlite_models.EventMinutesItemFile()
    elif model_name == FILE:
        return sqlite_models.File()
    elif model_name == MATTER:
        return sqlite_models.Matter()
    elif model_name == MATTER_FILE:
        return sqlite_models.MatterFile()
    elif model_name == MATTER_SPONSOR:
        return sqlite_models.MatterSponsor()
    elif model_name == MATTER_STATUS:
        return sqlite_models.MatterStatus()
    elif model_name == MINUTES_ITEM:
        return sqlite_models.MinutesItem()
    elif model_name == PERSON:
        return sqlite_models.Person()
    elif model_name == ROLE:
        return sqlite_models.Role()
    elif model_name == SESSION:
        return sqlite_models.Session()
    elif model_name == SEAT:
        return sqlite_models.Seat()
    elif model_name == TRANSCRIPT:
        return sqlite_models.Transcript()
    elif model_name == VOTE:
        return sqlite_models.Vote()
    else:
        return


def get_schema_properties(sql_schema: Model, doc: Transaction) -> Model:
    model = sql_schema
    model.id = doc.id
    if model.get_class_by_tablename() == type(sqlite_models.Body()):
        print("it works!!")
        model.name = doc.name
        model.description = doc.description
        model.start_datetime = doc.start_datetime
        model.is_active = doc.is_active
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.Event()):
        print("modifying events!!")
        model.body_id = doc.body_ref.getPath()
        model.static_thumbnail_id = doc.static_thumbnail_ref.getPath()
        model.hover_thumbnail_id = doc.hover_thumbnail_ref.getPath()
        model.agenda_uri = doc.agenda_uri
        model.minutes_uri = doc.minutes_uri
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.EventMinutesItem()):
        model.event_id = doc.event_ref
        model.minutes_item_id = doc.minutes_item_ref
        model.index = doc.index
        model.decision = doc.decision
    elif model.get_class_by_tablename() == type(sqlite_models.EventMinutesItemFile()):
        model.event_minutes_item_id = doc.event_minutes_item_ref
        model.name = doc.name
        model.uri = doc.uri
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.File()):
        model.uri = doc.uri
        model.name = doc.name
        model.description = doc.description
        model.media_type = doc.media_type
    elif model.get_class_by_tablename() == type(sqlite_models.Matter()):
        model.name = doc.name
        model.matter_type = doc.matter_type
        model.title = doc.title
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.MatterFile()):
        model.matter_id = doc.matter_ref
        model.name = doc.name
        model.uri = doc.uri
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.MatterSponsor()):
        model.matter_id = doc.matter_ref
        model.person_id = doc.person_ref
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.MatterStatus()):
        model.matter_id = doc.matter_ref
        model.event_minutes_item_id = doc.event_minutes_item_ref
        model.status = doc.status
        model.update_datetime = doc.update_datetime
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.MinutesItem()):
        model.name = doc.name
        model.description = doc.description
        model.matter_id = doc.matter_ref
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.Person()):
        model.name = doc.name
        model.router_string = doc.router_string
        model.email = doc.email
        model.phone = doc.phone
        model.website = doc.website
        model.picture_id = doc.picture_ref
        model.is_active = doc.is_active
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.Role()):
        model.title = doc.title
        model.person_id = doc.person_ref
        model.body_id = doc.body_ref
        model.seat_id = doc.seat_ref
        model.start_datetime = doc.start_datetime
        model.end_datetime = doc.end_datetime
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.Session()):
        model.event_id = doc.event_ref
        model.session_datetime = doc.session_datetime
        model.session_index = doc.session_index
        model.session_content_hash = doc.session_content_hash
        model.video_uri = doc.video_uri
        model.caption_uri = doc.caption_uri
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.Seat()):
        model.name = doc.name
        model.electoral_area = doc.electoral_area
        model.electoral_type = doc.electoral_type
        model.image_id = doc.image_ref
        model.external_source_id = doc.external_source_id
    elif model.get_class_by_tablename() == type(sqlite_models.Transcript()):
        model.session_id = doc.session_ref
        model.file_id = doc.file_ref
        model.generator = doc.generator
        model.confidence = doc.confidence
        model.created = doc.created
    elif model.get_class_by_tablename() == type(sqlite_models.Vote()):
        model.matter_id = doc.matter_ref
        model.event_id = doc.event_ref
        model.event_minutes_item_ref = doc.event_minutes_item_ref
        model.person_id = doc.person_ref
        model.decision = doc.decision
        model.in_majority = doc.in_majority
        model.external_source_id = doc.external_source_id
    return model


with Session(engine) as session:
    for model in model_list:
        # print(f"model : {model}, keys: {list(model.keys())}, keyname: {list(model.keys())[0]}")
        model_name = list(model.keys())[0]
        collection_iter = model.get(
            model_name
        ).collection.fetch()  # data source to transfer

        print(f"STARTING INSERTS on modelname: {model_name}")

        sql_schema = None
        doc_idx = 0
        for doc in collection_iter:
            # print(f'{doc.id} => {doc.to_dict()}')
            # if element in doc is first
            sql_schema = get_sql_schema(model_name)
            # print(f'sql_schema => {sql_schema}')
            sql_model = get_schema_properties(sql_schema, doc)
            # print(f'sql_model => {sql_model}')
            session.add(sql_model)

            doc_idx += 1

        print("COMMITTING INSERTS")
        session.commit()


from sqlalchemy import select
print("SELECTING ALL DATA")
with Session(engine) as session:
    stmt = select(sqlite_models.Matter)
    for matter in session.scalars(stmt):
        print(matter)
