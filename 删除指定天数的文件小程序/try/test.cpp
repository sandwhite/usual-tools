#include"read_json.h"
#include"file_delete.h"
#include <iostream>

using namespace DJ;
using namespace std;



int main()
{
	std::cout << "Hello World!\n";
	myjson m;
	paramlist P;
	m.read_json(P);//读取配置文件后再进行删除

	file_delete fd;
	fd.DeleteAllFile(P.file_path.c_str(), P.beforedays);
	cout << "successfully delete!" << endl;
	system("pause");


}
