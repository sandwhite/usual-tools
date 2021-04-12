#include<afx.h>
#include <string>
#include <stdio.h>
#include <io.h>
#include<sys/stat.h>
#include<time.h>
#include<iostream>
#include<windows.h>
#include<fstream>


namespace DJ
{
	class file_delete
	{
	public:
		file_delete();
		~file_delete();
		SYSTEMTIME GetFolderCreateTime(CString sFolder);
		bool GetFileModifyDate(CString filePathName, SYSTEMTIME &modDate);
		time_t TimeConvertToSec(int year, int month, int day);
		int DaysOffset(int fYear, int fMonth, int fDay, int tYear, int tMonth, int tDay);
		bool DeleteDirectory(CString directory_path);
		void DeleteAllFile(CString strDir, int days);


	private:

	};


}