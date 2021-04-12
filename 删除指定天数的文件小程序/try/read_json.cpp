#define _CRT_SECURE_NO_WARNINGS  //±ØÐëÌí¼Ó
#include "read_json.h"
#include <string>


namespace DJ
{
	myjson::myjson()
	{
	}

	myjson::~myjson()
	{
	}

	void myjson::read_json(paramlist &param)
	{
		std::string json_path = "./try.json";
		std::cerr << "Read Parameters" << std::endl;
		FILE* fp = fopen(json_path.c_str(), "r");
		if (fp == NULL)
		{
			std::cerr << "File does not exists!" << std::endl;
			return;
		}
		char readBuffer[65536];
		rapidjson::FileReadStream is(fp, readBuffer, sizeof(readBuffer));
		rapidjson::Document doc;
		doc.ParseStream(is);
		fclose(fp);

		param.file_path = doc["file_path"].GetString();
		param.beforedays = doc["beforedays"].GetInt();
	}

}

