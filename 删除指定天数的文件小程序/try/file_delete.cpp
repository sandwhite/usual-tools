#include"file_delete.h"

using namespace std;

namespace DJ
{
	file_delete::file_delete()
	{
	}

	file_delete::~file_delete()
	{
	}

	SYSTEMTIME file_delete::GetFolderCreateTime(CString sFolder)
	{
		SYSTEMTIME screatetime;
		HANDLE hDir;
		hDir = CreateFile(sFolder, GENERIC_READ, FILE_SHARE_READ | FILE_SHARE_DELETE, NULL,
			OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, NULL);//打开现存目录 只读方式打开即可

		FILETIME lpCreateTime, lpAccessTime, lpWriteTime;//创建时间，访问时间，修改时间
		if (GetFileTime(hDir, &lpCreateTime, &lpAccessTime, &lpWriteTime))
		{
			FILETIME fcreatetime;
			FileTimeToLocalFileTime(&lpCreateTime, &fcreatetime);//转换为本地时间
			FileTimeToSystemTime(&fcreatetime, &screatetime);//转换为系统时间
		}

		CloseHandle(hDir);//关闭文件句柄

		return screatetime;
	}

	//获取文件最后修改日期
	bool file_delete::GetFileModifyDate(CString filePathName, SYSTEMTIME &modDate)
	{
		HANDLE   hFile;
		WIN32_FIND_DATA   wfd;
		SYSTEMTIME   systime;
		FILETIME   localtime;

		memset(&wfd, 0, sizeof(wfd));
		if ((hFile = FindFirstFile(filePathName, &wfd)) == INVALID_HANDLE_VALUE)
			return false;
		//转换时间  
		FileTimeToLocalFileTime(&wfd.ftLastWriteTime, &localtime);
		FileTimeToSystemTime(&localtime, &systime);

		modDate = systime;
		return true;
	}

	//转换时间秒数
	time_t file_delete::TimeConvertToSec(int year, int month, int day)
	{
		tm info = { 0 };
		info.tm_year = year - 1900;
		info.tm_mon = month - 1;
		info.tm_mday = day;
		return mktime(&info);
	}

	//计算两个日期相差天数
	int file_delete::DaysOffset(int fYear, int fMonth, int fDay, int tYear, int tMonth, int tDay)
	{
		int fromSecond = (int)TimeConvertToSec(fYear, fMonth, fDay);
		int toSecond = (int)TimeConvertToSec(tYear, tMonth, tDay);
		return (toSecond - fromSecond) / 24 / 3600;
	}

	//删除目录下的文件、文件夹
	bool file_delete::DeleteDirectory(CString directory_path)
	{
		CFileFind finder;
		CString path;
		path.Format(_T("%s\\*.*"), directory_path);
		BOOL bWorking = finder.FindFile(path);
		while (bWorking)
		{
			bWorking = finder.FindNextFile();
			if (finder.IsDirectory() && !finder.IsDots())//处理文件夹
			{
				//递归删除文件夹
				DeleteDirectory(finder.GetFilePath());
				RemoveDirectory(finder.GetFilePath());

			}
			else//删除文件
			{
				DeleteFile(finder.GetFilePath());
			}
		}
		RemoveDirectory(directory_path);

		return true;
	}

	//删除指定文件夹目录中全部过时文件 

	void file_delete::DeleteAllFile(CString strDir, int days)
	{

		if (days < 0)
			days = 30;
		SYSTEMTIME curDate;
		GetLocalTime(&curDate); //获取当前时间
		CFileFind   finder;
		BOOL   bFound = finder.FindFile(strDir + L"\\*", 0);
		while (bFound)
		{
			bFound = finder.FindNextFile();
			if (finder.GetFileName() == "." || finder.GetFileName() == "..")
				continue;
			//   去掉文件(夹)只读等属性
			SetFileAttributes(finder.GetFilePath(), FILE_ATTRIBUTE_NORMAL);
			if (finder.IsDirectory())
			{
				SYSTEMTIME fDate = GetFolderCreateTime(finder.GetFilePath());  //获取文件最后修改时间
				int dayOffset = DaysOffset(fDate.wYear, fDate.wMonth, fDate.wDay,
					curDate.wYear, curDate.wMonth, curDate.wDay);
				if (dayOffset > days)
				{
					DeleteDirectory(finder.GetFilePath());
				}
			}
			else
			{
				SYSTEMTIME fDate;
				if (GetFileModifyDate(finder.GetFilePath(), fDate))  //获取文件最后修改时间
				{
					int dayOffset = DaysOffset(fDate.wYear, fDate.wMonth, fDate.wDay,
						curDate.wYear, curDate.wMonth, curDate.wDay);
					if (dayOffset > days)
						DeleteFile(finder.GetFilePath());
				}
			}
		}
		finder.Close();
		//  然后删除该文件夹
	   // RemoveDirectory(strDir);
	}
}

//int main()
//
//{
//	
//	CString file_path = "C:/Users/Administrator/Desktop/pic";
//	int beforedays = 0;
//
//	//删除绝对目录下5天前所有文件（包含目录）
//	DeleteAllFile(file_path, beforedays);
//	
//	return 0;
//}



