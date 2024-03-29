{
	"job": {
		"content": [
		{
			"reader": {
				"name": "mysqlreader",
				"parameter": {
					"column": ["*"],
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
					"column": [$COLUMN],
					"compress": "gzip",
					"defaultFS": "hdfs://node1:8020",
					"fieldDelimiter": "\t",
					"fileName": "$table_name",
					"fileType": "text",
					"path": "/origin_data/gmall/db/$DIRNAME",
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