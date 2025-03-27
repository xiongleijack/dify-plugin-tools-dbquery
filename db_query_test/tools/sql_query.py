from typing import Any, Generator
import logging
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from db_query_test.utils.db_util import DbUtil

class SqlQueryTool(Tool):
    def _invoke(
            self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        try:
            db = DbUtil(db_type="mysql",
                        username="root", password="xL123456",
                        host="rm-uf6m77zfj1wdlp2cu3o.mysql.rds.aliyuncs.com", port=3306,
                        properties="")
            
            # 查询所有可用的数据库
            records = db.run_query("select SCHEMA_NAME from information_schema.SCHEMATA where SCHEMA_NAME not in ('mysql', 'information_schema', 'performance_schema', '__recycle_bin__', 'sys');")
            
            # 转换为选项格式
            options = []
            for record in records:
                schema_name = record['SCHEMA_NAME']
                options.append({
                    "value": schema_name,
                    "label": schema_name
                })
            
            # 返回下拉选择消息
            yield self.create_select_message(
                options=options,
                placeholder="请选择数据库"
            )

        except Exception as e:
            message = "获取数据库列表失败"
            logging.exception(message)
            yield self.create_text_message(f"错误: {str(e)}")