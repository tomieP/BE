from infrastructure.databases.mssql import init_mssql
from infrastructure.models import course_register_model, todo_model, user_model, course_model, consultant_model, appointment_model,program_model, feedback_model,survey_model,admin_model,appointment_model,apprasal_model,appraser_model,buyer_model,listing_model,seller_model,watch_model,support_agent_model,support_ticket_model,transaction_model

def init_db(app):
    init_mssql(app)
    
from infrastructure.databases.mssql import Base