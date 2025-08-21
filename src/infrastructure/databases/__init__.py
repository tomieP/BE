from infrastructure.databases.mssql import init_mssql
from infrastructure.models import admin,apprasal_model,appraser_model,buyer_model,feedback_model,listing_model,support_agent_model,seller_model,support_ticket_model,transaction_model,user_model,watch_model
def init_db(app):
    init_mssql(app)
    
from infrastructure.databases.mssql import Base
from .mssql import init_mssql as init_db, db