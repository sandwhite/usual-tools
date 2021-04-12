#define _CRT_SECURE_NO_WARNINGS  //±ØÐëÌí¼Ó
#include <iostream>
#include <string>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include "rapidjson/filewritestream.h"
#include "rapidjson/prettywriter.h"
#include "rapidjson/filereadstream.h"

namespace DJ 
{
	typedef struct
	{
		std::string file_path;
		int beforedays;
	}paramlist;

	class myjson
	{
	public:
		myjson();
		~myjson();
		void read_json(paramlist &param);

	private:

	};


}

