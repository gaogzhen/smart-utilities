{
	"job": {
		"content": [
		{
			"reader": {
				"name": "mysqlreader",
				"parameter": {
					"column": ["*"],
					"where": "id>=3",
					"connection": [
					{
						"jdbcUrl": [
							"jdbc:mysql://node1:3306/gmall?useUnicode=true&allowKeyRetrieval=tru&characterEncoding=utf-8"
						],
						"table": ["$table_name"]
					}
					],
					"password": "123456",
					"splitPk": "",
					"username": "root"
				}
			},
			"writer": {
				"name": "hdfswriter",
				"parameter": {
					"column": ["*"],
					"compress": "gzip",
					"defaultFS": "hdfs://node1:8020",
					"fieldDelimiter": "\t",
					"fileName": "$table_name",
					"fileType": "text",
					"path": "/$table_name",
					"writeMode": "append"
				}
			}
		}
		],
		"setting": {
			"speed": {
				"channel": 1
			}
		}
	}
}