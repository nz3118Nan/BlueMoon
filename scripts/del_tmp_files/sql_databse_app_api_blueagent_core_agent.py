#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: sql_database_app_api_blueagent_core_agent_management.py
Author: Zhou Nan
Date: 2025-03-26
Description: Data Access Object for BlueAgent Core Agent Management API
"""
################################################################################
# system settings
import os
import sys
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
os.chdir(root_dir)
sys.path.append(root_dir)

# built-in modules
from typing import Dict, Any
from sqlalchemy import select, and_
import json
# developed modules
from app.core.logging_setting import logger
from app.data_access_object.sql_database_app_general_CRUD_operation import GeneralCRUD
from app.models.database_sql_service_core_model import ServiceAgentRegistry
################################################################################
'''
Log Format:
0️⃣ Cell[ ✅ ] - Subject <<param1>> <<param2>> verb successfully.
0️⃣ Cell[ ❌ ] - Subject <<param1>> <<param2>> verb failed with error: <error message>
1️⃣ Infra[ ✅ ] - Subject <<param1>> <<param2>> verb successfully.
1️⃣ Infra[ ❌ ] - Subject <<param1>> <<param2>> verb failed with error: <error message>
2️⃣ DAO[ ✅ ] - Subject <<param1>> <<param2>> verb successfully.
2️⃣ DAO[ ❌ ] - Subject <<param1>> <<param2>> verb failed with error: <error message>
3️⃣ Middle[ ✅ ] - Subject <<param1>> <<param2>> verb successfully.
3️⃣ Middle[ ❌ ] - Subject <<param1>> <<param2>> verb failed with error: <error message>
4️⃣ Service[ ✅ ] - Subject <<param1>> <<param2>> verb successfully.
4️⃣ Service[ ❌ ] - Subject <<param1>> <<param2>> verb failed with error: <error message>
5️⃣ API[ ✅ ] - Subject <<param1>> <<param2>> verb successfully.
5️⃣ API[ ❌ ] - Subject <<param1>> <<param2>> verb failed with error: <error message>
⚠️ notice it it error, which will not block the main process
Level Here: DAO
'''
################################################################################
class BlueAgentCoreAgentDAO:
    def __init__(self):
        self.crud = GeneralCRUD(model=ServiceAgentRegistry, db_name="blueprint_service")
        
    async def get_agent_protocol(self, agent_id: int) -> Dict[str, Any]:
        # get the agent protocol from the database
        try:
            # check existence of the agent
            if not await self.crud._exists(agent_id, is_active_check=True):
                logger.critical(f"2️⃣ DAO[ ❌ ] agent protocol <<agent id: {agent_id}>> fetched failed with error: not found in database")
                return None
            
            async with self.crud.db.session_scope() as session:
                statement = select(ServiceAgentRegistry).where(
                    and_(
                        ServiceAgentRegistry.id == agent_id,
                        ServiceAgentRegistry.is_active == True
                    )
                )
                result = await session.execute(statement)
                agent = result.scalar()
            
            # output json
            result = agent.model_dump(exclude={"created_time", 
                                                "updated_time", 
                                                "is_active",
                                                'last_interaction_time',
                                                'total_interactions'})
            logger.debug(f"2️⃣ DAO[ ✅ ] agent protocol <<agent id: {agent_id}>> fetched successfully")
            return result
        except Exception as e:
            logger.error(f"2️⃣ DAO[ ❌ ] agent protocol <<agent id: {agent_id}>> fetched failed with error: {str(e)}")
            return None

################################################################################
# main
if __name__ == "__main__":
    import asyncio
    agent_dao = BlueAgentCoreAgentDAO()
    print(asyncio.run(agent_dao.get_agent_protocol(1)))